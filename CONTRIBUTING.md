# Contributing to KnowledgeCatalyst

Thank you for your interest in contributing to KnowledgeCatalyst! We welcome contributions from the community and are excited to collaborate with you.

## How to Contribute

### Reporting Issues

If you encounter a bug or have a feature request:

1. Check the [issue tracker](https://github.dxc.com/innovate/KnowledgeCatalyst/issues) to see if it has already been reported
2. If not, create a new issue with:
   - A clear, descriptive title
   - A detailed description of the problem or suggestion
   - Steps to reproduce (for bugs)
   - Expected vs. actual behavior
   - Your environment details (OS, Docker version, etc.)

### Submitting Changes

We follow a standard fork-and-pull-request workflow:

1. **Fork the Repository**
   - Fork the project to your own GitHub account
   - Clone your fork locally

   ```bash
   git clone https://github.dxc.com/YOUR-USERNAME/KnowledgeCatalyst.git
   cd KnowledgeCatalyst
   ```

2. **Create a Branch**
   - Create a new branch for your changes
   - Use a descriptive name

   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

3. **Make Your Changes**
   - Write clean, readable code
   - Follow the existing code style
   - Add comments where necessary
   - Update documentation as needed

4. **Test Your Changes**
   - Ensure all existing tests pass
   - Add new tests for new features
   - Test locally using Docker Compose

   ```bash
   docker compose build
   docker compose up -d
   # Run tests
   cd backend
   python -m pytest
   ```

5. **Commit Your Changes**
   - Write clear, concise commit messages
   - Reference related issues

   ```bash
   git add .
   git commit -m "Add feature: description of your changes (#issue-number)"
   ```

6. **Push and Create Pull Request**
   - Push your changes to your fork
   - Create a pull request to the main repository

   ```bash
   git push origin feature/your-feature-name
   ```

   - Go to the GitHub repository and click "New Pull Request"
   - Provide a clear description of your changes
   - Reference any related issues

### Pull Request Guidelines

- **Keep it focused**: Each PR should address a single concern
- **Update documentation**: Include relevant documentation updates
- **Add tests**: New features should include tests
- **Follow code style**: Maintain consistency with existing code
- **Be responsive**: Address review feedback promptly

## Development Guidelines

### Code Style

- **Python**: Follow PEP 8 guidelines
  - Use 4 spaces for indentation
  - Maximum line length: 100 characters
  - Use meaningful variable and function names

- **JavaScript/TypeScript**: Follow standard conventions
  - Use 2 spaces for indentation
  - Use camelCase for variables and functions

### Documentation

- Update the README.md if you change functionality
- Add docstrings to Python functions and classes
- Comment complex logic
- Update API documentation for endpoint changes

### Testing

- Write unit tests for new functions
- Write integration tests for new features
- Ensure all tests pass before submitting PR
- Aim for high test coverage

### Commit Messages

Follow the conventional commits specification:

- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `test:` for test additions or modifications
- `refactor:` for code refactoring
- `chore:` for maintenance tasks

Example:
```
feat: add support for PDF document processing

- Added PDF parser using PyPDF2
- Integrated with existing document ingestion pipeline
- Added tests for PDF processing

Closes #123
```

## Code Review Process

1. A maintainer will review your pull request
2. They may request changes or ask questions
3. Address feedback and push updates
4. Once approved, your PR will be merged

## Setting Up Development Environment

### Prerequisites

- Docker and Docker Compose
- Python 3.9+
- Git

### Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.dxc.com/innovate/KnowledgeCatalyst.git
   cd KnowledgeCatalyst
   ```

2. Copy and configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. Build and run with Docker:
   ```bash
   docker compose build
   docker compose up -d
   ```

4. For backend development:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn score:app --reload
   ```

5. For frontend development:
   ```bash
   cd frontend
   pip install -r requirements.txt
   streamlit run app.py
   ```

## Community Guidelines

- Be respectful and inclusive
- Help others when you can
- Provide constructive feedback
- Follow the project's code of conduct

## Questions?

If you have questions about contributing:
- Open an issue with the "question" label
- Contact the maintainers at guglielmo.piacentini@dxc.com

## License

By contributing to KnowledgeCatalyst, you agree that your contributions will be licensed under the Apache License 2.0.

---

Thank you for contributing to KnowledgeCatalyst! Your efforts help make this project better for everyone.
