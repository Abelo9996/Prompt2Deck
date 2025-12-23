# Contributing to Prompt2Deck

Thank you for your interest in contributing to Prompt2Deck! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/Prompt2Deck.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit: `git commit -m "Add your feature"`
7. Push: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- Git

### Setup

Run the setup script:
```bash
# macOS/Linux
chmod +x setup.sh
./setup.sh

# Windows
setup.bat
```

Or manually:
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env

# Frontend
cd frontend
npm install
cp .env.example .env.local
```

## Code Style

### Python

- Follow PEP 8
- Use type hints
- Write docstrings for all public functions
- Use async/await for I/O operations
- Format with `black`
- Sort imports with `isort`

Example:
```python
async def generate_content(text: str, options: Dict[str, Any]) -> List[SlideData]:
    """
    Generate slide content from text input.
    
    Args:
        text: Input text or outline
        options: Generation options
        
    Returns:
        List of slide data objects
    """
    # Implementation
    pass
```

### TypeScript/React

- Use TypeScript for type safety
- Functional components with hooks
- Props interface for all components
- Use Tailwind CSS for styling
- Format with Prettier

Example:
```typescript
interface ButtonProps {
  onClick: () => void
  disabled?: boolean
  children: React.ReactNode
}

export default function Button({ onClick, disabled, children }: ButtonProps) {
  return (
    <button onClick={onClick} disabled={disabled}>
      {children}
    </button>
  )
}
```

## Testing

### Backend Tests

```bash
cd backend
pytest
pytest --cov  # With coverage
```

### Frontend Tests

```bash
cd frontend
npm test
npm run test:watch  # Watch mode
```

## Areas for Contribution

### High Priority

- [ ] Unit tests for pipeline modules
- [ ] Integration tests for API endpoints
- [ ] Google Slides API integration
- [ ] Custom template support
- [ ] Improved error handling

### Medium Priority

- [ ] Advanced image placement
- [ ] More theme options
- [ ] Markdown export
- [ ] Batch processing
- [ ] Performance optimizations

### Good First Issues

- [ ] Add more example inputs
- [ ] Improve documentation
- [ ] Add more themes
- [ ] UI improvements
- [ ] Bug fixes

## Pull Request Guidelines

### Before Submitting

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages are clear

### PR Description

Include:
- What the PR does
- Why the change is needed
- How to test it
- Screenshots (for UI changes)
- Related issues

### Example PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Steps to test:
1. Step one
2. Step two

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Code reviewed
```

## Feature Requests

Open an issue with:
- Clear description of the feature
- Use cases
- Proposed implementation (optional)
- Examples or mockups (optional)

## Bug Reports

Open an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment (OS, Python version, etc.)
- Error messages or logs

## Code Review Process

1. Maintainer reviews PR
2. Feedback provided if needed
3. Changes requested or approved
4. Once approved, maintainer merges

## Community Guidelines

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Follow the code of conduct

## Questions?

- Open an issue for questions
- Check existing issues first
- Be patient and respectful

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Prompt2Deck! 🎯
