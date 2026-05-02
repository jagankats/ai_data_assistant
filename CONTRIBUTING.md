# Contributing to AI Data Assistant

Thank you for your interest in contributing! Here's how to get started.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/rag_data_assistant.git
   cd rag_data_assistant
   ```

3. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python database_setup.py
```

## Making Changes

1. Make your changes in the feature branch
2. Test thoroughly:
   ```bash
   # Backend
   python backend/api.py
   
   # Frontend (separate terminal)
   cd frontend && npm start
   ```

3. Keep commits clean and descriptive:
   ```bash
   git add .
   git commit -m "feat: add intelligent query parsing"
   ```

## Submitting Changes

1. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request** on GitHub with:
   - Clear description of changes
   - Reference to any related issues
   - Screenshots if UI changes

## Code Standards

- **Python**: Follow PEP 8
- **JavaScript/React**: Use ES6+, follow existing patterns
- **Git messages**: Use conventional commits (feat:, fix:, docs:, etc.)

## Reporting Issues

- Use clear, descriptive titles
- Include steps to reproduce bugs
- Add screenshots/logs if applicable
- Mention your OS and Python version

## Questions?

- Open an issue for discussion
- Check existing issues first

Thank you for contributing! 🙏