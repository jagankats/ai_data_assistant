from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import psycopg2
import logging
import os
import re
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, OLLAMA_API_URL, OLLAMA_MODEL

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Data Assistant API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DataQueryRequest(BaseModel):
    question: str

class DataQueryResponse(BaseModel):
    question: str
    sql_query: str
    results: list
    column_names: list
    answer: str


def get_database_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def execute_ollama_prompt(prompt: str, max_tokens: int = 300, temperature: float = 0.5) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "temperature": temperature,
    }
    try:
        # Increased timeout for model loading and processing
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=120)  # 2 minutes
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except requests.exceptions.Timeout:
        raise Exception(
            "Ollama request timed out. The model might be loading or the prompt is too complex. "
            "Try again in a few moments, or use a simpler question."
        )
    except requests.exceptions.ConnectionError:
        raise Exception(
            f"Cannot connect to Ollama at {OLLAMA_API_URL}. "
            "Make sure Ollama is running with: 'ollama serve'"
        )
    except requests.exceptions.HTTPError as http_error:
        if response.status_code == 404:
            raise Exception(
                f"Model '{OLLAMA_MODEL}' not found. "
                f"Make sure it's installed with: 'ollama pull {OLLAMA_MODEL}'"
            )
        elif response.status_code == 503:
            raise Exception(
                f"Model '{OLLAMA_MODEL}' is still loading. "
                "Please wait a moment and try again."
            )
        else:
            raise Exception(f"Ollama HTTP error {response.status_code}: {http_error}")
    except Exception as error:
        raise Exception(f"Ollama API error: {error}")


def load_database_schema_prompt() -> str:
    try:
        with get_database_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT c.table_name, c.column_name, COALESCE(d.description, '') AS description
                    FROM information_schema.columns c
                    LEFT JOIN pg_catalog.pg_description d
                        ON d.objoid = (
                            SELECT oid FROM pg_catalog.pg_class
                            WHERE relname = c.table_name
                            AND relnamespace = (
                                SELECT oid FROM pg_catalog.pg_namespace WHERE nspname = c.table_schema
                            )
                        )
                        AND d.objsubid = c.ordinal_position
                    WHERE c.table_schema = 'public'
                      AND c.table_name IN ('sales_orders', 'sfdc_leads')
                    ORDER BY c.table_name, c.ordinal_position;
                """)
                rows = cursor.fetchall()

        if not rows:
            return (
                "Database Schema:\n"
                "- sales_orders: id, order_id, order_date, customer_name, segment, country, region, product_name, category, sub_category, quantity, sales, discount, profit\n"
                "- sfdc_leads: id, lead_id, created_date, lead_source, lead_status, campaign_name, email, phone, company, industry, score, converted\n"
            )

        tables = {}
        for table_name, column_name, description in rows:
            tables.setdefault(table_name, []).append(
                f"{column_name} ({description})" if description else column_name
            )

        schema_text = "Database Schema:\n"
        for table_name, columns in tables.items():
            schema_text += f"- {table_name}: {', '.join(columns)}\n"

        schema_text += "\nKEY RULES:\n"
        schema_text += "1. GLOBAL queries (top N total): Use LIMIT N\n"
        schema_text += "2. PER-GROUP queries (top N per group): Use ROW_NUMBER() OVER (PARTITION BY group_field ORDER BY metric DESC) AS rn WHERE rn <= N\n"
        schema_text += "\nPer-group keywords: country-wise, region-wise, segment-wise, per country, per region, by country, for each\n"

        schema_text += "\nExamples:\n"
        schema_text += "- Top 2 products: SELECT product_name, SUM(sales) revenue FROM sales_orders GROUP BY product_name ORDER BY revenue DESC LIMIT 2;\n"
        schema_text += "- Country-wise top 2 products: SELECT country, product_name, revenue FROM (SELECT country, product_name, SUM(sales) revenue, ROW_NUMBER() OVER (PARTITION BY country ORDER BY SUM(sales) DESC) rn FROM sales_orders GROUP BY country, product_name) t WHERE rn <= 2 ORDER BY country, revenue DESC;\n"
        schema_text += "- Region-wise top 3: SELECT region, product_name, revenue FROM (SELECT region, product_name, SUM(sales) revenue, ROW_NUMBER() OVER (PARTITION BY region ORDER BY SUM(sales) DESC) rn FROM sales_orders GROUP BY region, product_name) t WHERE rn <= 3 ORDER BY region, revenue DESC;\n"
        return schema_text
    except Exception as error:
        logger.error("Error loading database schema prompt: %s", error)
        raise


SCHEMA_PROMPT = load_database_schema_prompt()


def build_sql_for_question(user_question: str) -> str:
    question_lower = user_question.lower()
    
    # Determine table to use: sales or marketing
    marketing_keywords = ["lead", "campaign", "email", "phone", "company", "industry", "converted", "source", "crm", "sfdc", "marketing"]
    is_marketing_question = any(kw in question_lower for kw in marketing_keywords)
    
    if is_marketing_question:
        # SFDC Leads queries
        prompt = f"""Analyze this question and generate ONLY the SQL query. No explanation.

Question: {user_question}

Table: sfdc_leads (id, lead_id, created_date, lead_source, lead_status, campaign_name, email, phone, company, industry, score, converted)

Guidelines:
1. If question asks to group/compare by category (e.g., "by campaign", "by source", "per industry", "campaign-wise", etc), use GROUP BY
2. If asking for top N items per group/category (e.g., "top 2 leads per campaign", "leads by campaign", etc), use GROUP BY with aggregates
3. Always aggregate with COUNT(*) or SUM() as appropriate
4. Use ONLY sfdc_leads table - no joins

Examples:
- "leads by campaign": SELECT campaign_name, COUNT(*) as count FROM sfdc_leads GROUP BY campaign_name ORDER BY count DESC;
- "top 5 lead sources": SELECT lead_source, COUNT(*) as count FROM sfdc_leads GROUP BY lead_source ORDER BY count DESC LIMIT 5;
- "converted leads by campaign": SELECT campaign_name, SUM(CASE WHEN converted THEN 1 ELSE 0 END) as converted_count FROM sfdc_leads GROUP BY campaign_name ORDER BY converted_count DESC;

Write only the SQL query."""
    else:
        # Sales Orders queries
        prompt = f"""Analyze this question and generate ONLY the SQL query. No explanation.

Question: {user_question}

Table: sales_orders (country, region, product_name, category, sub_category, sales, quantity, profit)

Guidelines:
1. If question asks "top N items PER group/category" (e.g., "per country", "by country", "country-wise", "region wise", etc) -> use ROW_NUMBER() window function
2. If question asks "top N items OVERALL" (e.g., just "top 2 products", "top 5") -> use LIMIT

FOR PER-GROUP QUERIES - Use this EXACT structure:
SELECT country, product_name, revenue
FROM (
    SELECT 
        country, 
        product_name, 
        SUM(sales) AS revenue,
        ROW_NUMBER() OVER (
            PARTITION BY country 
            ORDER BY SUM(sales) DESC
        ) AS rn
    FROM sales_orders
    GROUP BY country, product_name
) t
WHERE rn <= 2
ORDER BY country, revenue DESC;

IMPORTANT: In the outer SELECT, use the alias "revenue" from subquery, NOT SUM(sales) again!

FOR GLOBAL QUERIES - Use:
SELECT product_name, SUM(sales) as revenue FROM sales_orders GROUP BY product_name ORDER BY revenue DESC LIMIT 2;

Use ONLY sales_orders table - no joins.

Analyze: Does "{user_question}" ask for results PER group/category or OVERALL results?

Write only the SQL query."""

    sql_query = execute_ollama_prompt(prompt, max_tokens=120, temperature=0)
    sql_query = sql_query.strip()

    # Extract SQL - remove any text before SELECT
    select_pos = sql_query.upper().find("SELECT")
    if select_pos > 0:
        sql_query = sql_query[select_pos:]

    # Remove text after semicolon
    semicolon_pos = sql_query.find(";")
    if semicolon_pos >= 0:
        sql_query = sql_query[:semicolon_pos + 1]

    # Remove markdown
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

    return sql_query


def execute_dataset_query(sql_query: str):
    try:
        with get_database_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql_query)
                results = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description]
        return column_names, results
    except Exception as error:
        logger.error("Error executing SQL query: %s", error)
        raise


def build_natural_language_response(user_question: str, sql_query: str, results: list) -> str:
    result_text = "\n".join([str(row) for row in results])
    prompt = f"""You are an AI Data Assistant. Answer the user's question based on the SQL query results.

User question: {user_question}
SQL query: {sql_query}
Results: {result_text}

Provide a natural language answer."""
    return execute_ollama_prompt(prompt, max_tokens=300, temperature=0.5)


@app.get("/")
async def health_root():
    return {"message": "AI Data Assistant API", "status": "running"}


@app.post("/query", response_model=DataQueryResponse)
async def query_data_assistant(request: DataQueryRequest):
    try:
        logger.info("Processing question: %s", request.question)

        sql_query = build_sql_for_question(request.question)
        logger.info("Generated SQL: %s", sql_query)

        column_names, results = execute_dataset_query(sql_query)
        logger.info("Query executed successfully, %d rows returned", len(results))

        answer = build_natural_language_response(request.question, sql_query, results)
        logger.info("Answer generated successfully")

        return DataQueryResponse(
            question=request.question,
            sql_query=sql_query,
            results=results,
            column_names=column_names,
            answer=answer,
        )
    except Exception as error:
        logger.error("Error processing data query: %s", error)
        raise HTTPException(status_code=500, detail=str(error))


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
