#!/bin/bash

echo "Setting up Document Processing Backend..."

# Create directories
mkdir -p logs migrations/versions ssl

# Copy environment file
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file. Please update with your actual values."
fi

# Generate secret key
SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(32))')
sed -i "s/your-super-secret-key-here-use-something-random/$SECRET_KEY/g" .env

# Initialize Alembic
alembic init migrations 2>/dev/null || echo "Alembic already initialized"

# Create first migration
echo "Creating initial migration..."
alembic revision --autogenerate -m "Initial migration"

echo "Setup complete!"
echo "Next steps:"
echo "1. Update .env with your GROQ_API_KEY"
echo "2. Run: docker-compose up -d"
echo "3. Run migrations: docker-compose exec api alembic upgrade head" 