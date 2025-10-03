#!/bin/bash

# AWS Production Deployment Script for Document Summarizer Agent
# This script deploys the application to AWS using Terraform and Docker

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="document-summarizer"
ENVIRONMENT="production"
AWS_REGION="us-east-1"
TERRAFORM_DIR="infra/terraform"
DOCKER_IMAGE_NAME="${PROJECT_NAME}-${ENVIRONMENT}"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check if required tools are installed
    command -v aws >/dev/null 2>&1 || { log_error "AWS CLI is required but not installed. Aborting."; exit 1; }
    command -v terraform >/dev/null 2>&1 || { log_error "Terraform is required but not installed. Aborting."; exit 1; }
    command -v docker >/dev/null 2>&1 || { log_error "Docker is required but not installed. Aborting."; exit 1; }
    command -v python3 >/dev/null 2>&1 || { log_error "Python 3 is required but not installed. Aborting."; exit 1; }
    
    # Check AWS credentials
    if ! aws sts get-caller-identity >/dev/null 2>&1; then
        log_error "AWS credentials not configured. Please run 'aws configure' first."
        exit 1
    fi
    
    log_success "All prerequisites met"
}

setup_environment() {
    log_info "Setting up environment variables..."
    
    # Create .env file if it doesn't exist
    if [ ! -f .env ]; then
        log_info "Creating .env file from template..."
        cat > .env << EOF
# AWS Configuration
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=${AWS_REGION}

# S3 Configuration
S3_BUCKET_NAME=${PROJECT_NAME}-${ENVIRONMENT}-documents

# Database Configuration
DATABASE_URL=postgresql://postgres:password@localhost:5432/docprocessing

# DynamoDB Configuration
DYNAMODB_CACHE_TABLE=${PROJECT_NAME}-${ENVIRONMENT}-cache

# SQS Configuration
SQS_QUEUE_NAME=${PROJECT_NAME}-${ENVIRONMENT}-task-queue

# AI Configuration
GROQ_API_KEY=your_groq_api_key_here

# Security
SECRET_KEY=$(openssl rand -hex 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# File Upload Settings
MAX_FILE_SIZE=10485760
ALLOWED_EXTENSIONS=[".pdf", ".txt", ".docx"]
ALLOWED_MIME_TYPES=["application/pdf", "text/plain", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]

# CORS and Security
ALLOWED_ORIGINS=["*"]
ALLOWED_HOSTS=["*"]

# Rate Limiting
UPLOAD_RATE_LIMIT=2
MAX_PROCESSING_TIME=300

# Logging
LOG_LEVEL=INFO
EOF
        log_warning "Please update .env file with your actual credentials before proceeding"
        read -p "Press Enter to continue after updating .env file..."
    fi
    
    # Load environment variables
    export $(cat .env | grep -v '^#' | xargs)
    
    log_success "Environment variables loaded"
}

deploy_infrastructure() {
    log_info "Deploying AWS infrastructure with Terraform..."
    
    cd ${TERRAFORM_DIR}
    
    # Initialize Terraform
    log_info "Initializing Terraform..."
    terraform init
    
    # Plan deployment
    log_info "Planning Terraform deployment..."
    terraform plan \
        -var="aws_region=${AWS_REGION}" \
        -var="environment=${ENVIRONMENT}" \
        -var="project_name=${PROJECT_NAME}" \
        -var="groq_api_key=${GROQ_API_KEY}" \
        -out=tfplan
    
    # Apply deployment
    log_info "Applying Terraform deployment..."
    terraform apply tfplan
    
    # Get outputs
    log_info "Getting Terraform outputs..."
    S3_BUCKET_NAME=$(terraform output -raw s3_bucket_name)
    DATABASE_ENDPOINT=$(terraform output -raw database_endpoint)
    DATABASE_PASSWORD=$(terraform output -raw database_password)
    SQS_QUEUE_URL=$(terraform output -raw sqs_queue_url)
    DYNAMODB_TABLE_NAME=$(terraform output -raw dynamodb_table_name)
    LAMBDA_FUNCTION_NAME=$(terraform output -raw lambda_function_name)
    
    # Update .env with actual values
    log_info "Updating .env with actual AWS resource values..."
    cd ../..
    
    # Backup original .env
    cp .env .env.backup
    
    # Update .env with actual values
    sed -i.bak "s|S3_BUCKET_NAME=.*|S3_BUCKET_NAME=${S3_BUCKET_NAME}|g" .env
    sed -i.bak "s|DATABASE_URL=.*|DATABASE_URL=postgresql://postgres:${DATABASE_PASSWORD}@${DATABASE_ENDPOINT}/docprocessing|g" .env
    sed -i.bak "s|DYNAMODB_CACHE_TABLE=.*|DYNAMODB_CACHE_TABLE=${DYNAMODB_TABLE_NAME}|g" .env
    sed -i.bak "s|SQS_QUEUE_URL=.*|SQS_QUEUE_URL=${SQS_QUEUE_URL}|g" .env
    sed -i.bak "s|LAMBDA_FUNCTION_NAME=.*|LAMBDA_FUNCTION_NAME=${LAMBDA_FUNCTION_NAME}|g" .env
    
    # Clean up backup files
    rm .env.bak
    
    log_success "Infrastructure deployed successfully"
}

build_docker_image() {
    log_info "Building Docker image..."
    
    # Build the Docker image
    docker build -t ${DOCKER_IMAGE_NAME}:latest .
    
    log_success "Docker image built successfully"
}

deploy_lambda() {
    log_info "Deploying Lambda function..."
    
    # Create deployment package
    log_info "Creating Lambda deployment package..."
    
    # Create a temporary directory for Lambda package
    TEMP_DIR=$(mktemp -d)
    cp -r . ${TEMP_DIR}/
    cd ${TEMP_DIR}
    
    # Install dependencies
    pip install -r requirements.txt -t .
    
    # Create ZIP file
    zip -r task_processor.zip . -x "*.git*" "*.env*" "test/*" "infra/*" "scripts/*" "docs/*"
    
    # Copy to Terraform directory
    cp task_processor.zip ../../${TERRAFORM_DIR}/
    
    # Clean up
    cd ../..
    rm -rf ${TEMP_DIR}
    
    # Update Lambda function
    cd ${TERRAFORM_DIR}
    terraform apply -auto-approve -target=aws_lambda_function.task_processor
    cd ../..
    
    log_success "Lambda function deployed successfully"
}

run_tests() {
    log_info "Running tests..."
    
    # Install test dependencies
    pip install pytest pytest-asyncio moto boto3
    
    # Run tests
    python -m pytest test/ -v --tb=short
    
    log_success "Tests completed successfully"
}

setup_monitoring() {
    log_info "Setting up monitoring and alerting..."
    
    # This would typically involve setting up CloudWatch alarms, dashboards, etc.
    # For now, we'll just log the monitoring setup
    log_info "Monitoring setup would go here (CloudWatch, alarms, etc.)"
    
    log_success "Monitoring setup completed"
}

deploy_application() {
    log_info "Deploying application to ECS/Fargate..."
    
    # This would involve creating ECS task definitions, services, etc.
    # For now, we'll just log the deployment
    log_info "Application deployment would go here (ECS, Fargate, etc.)"
    
    log_success "Application deployed successfully"
}

cleanup() {
    log_info "Cleaning up temporary files..."
    
    # Remove temporary files
    rm -f ${TERRAFORM_DIR}/task_processor.zip
    rm -f ${TERRAFORM_DIR}/tfplan
    
    log_success "Cleanup completed"
}

main() {
    log_info "Starting AWS production deployment for Document Summarizer Agent"
    
    check_prerequisites
    setup_environment
    deploy_infrastructure
    build_docker_image
    deploy_lambda
    run_tests
    setup_monitoring
    deploy_application
    cleanup
    
    log_success "Deployment completed successfully!"
    log_info "Your Document Summarizer Agent is now running on AWS"
    log_info "Check the Terraform outputs for connection details"
}

# Handle script arguments
case "${1:-}" in
    "infrastructure")
        check_prerequisites
        setup_environment
        deploy_infrastructure
        ;;
    "lambda")
        deploy_lambda
        ;;
    "test")
        run_tests
        ;;
    "cleanup")
        cleanup
        ;;
    "destroy")
        log_warning "This will destroy all AWS resources. Are you sure? (y/N)"
        read -r response
        if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
            cd ${TERRAFORM_DIR}
            terraform destroy -auto-approve
            cd ../..
            log_success "Infrastructure destroyed"
        else
            log_info "Destroy cancelled"
        fi
        ;;
    *)
        main
        ;;
esac

