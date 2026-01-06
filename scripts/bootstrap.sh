#!/bin/bash
# Bootstrap script to set up the development environment

set -e

echo "🚀 Bootstrapping AI System Security Automation..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Please install it from https://github.com/astral-sh/uv"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
uv pip install -e ".[dev]"

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env from .env.example..."
    cp .env.example .env
fi

echo "✅ Bootstrap complete!"
echo ""
echo "Next steps:"
echo "  1. Update .env with your settings"
echo "  2. Run tests: make test"
echo "  3. Start development: python -m security_automation.main"
