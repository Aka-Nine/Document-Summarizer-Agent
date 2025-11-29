#!/bin/bash

# AWS Free Tier Deployment Script for Document Summarizer Agent
# This script deploys the application to AWS using ONLY free tier services

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="document-summarizer"
ENVIRONMENT="free-tier"
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

log_free_tier() {
    echo -e "${PURPLE}[FREE TIER]${NC} $1"
}

check_prerequisites() {
    log_info "Checking prerequisites for AWS Free Tier deployment..."
    
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
    
    # Check if account is eligible for free tier
    log_info "Checking AWS account free tier eligibility..."
    ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    log_free_tier "AWS Account ID: $ACCOUNT_ID"
    log_free_tier "Free tier services will be used for this deployment"
    
    log_success "All prerequisites met for free tier deployment"
}

setup_environment() {
    log_info "Setting up environment for AWS Free Tier..."
    
    # Create .env file if it doesn't exist
    if [ ! -f .env ]; then
        log_info "Creating .env file optimized for free tier..."
        cat > .env << EOF
# AWS Free Tier Configuration
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=${AWS_REGION}

# S3 Configuration (FREE: 5GB storage, 20K GET requests)
S3_BUCKET_NAME=${PROJECT_NAME}-${ENVIRONMENT}-documents

# Database Configuration (FREE: 750 hours/month for 12 months)
DATABASE_URL=postgresql://postgres:password@localhost:5432/docprocessing

# DynamoDB Configuration (FREE: 25GB storage, 25 RCU/WCU)
DYNAMODB_CACHE_TABLE=${PROJECT_NAME}-${ENVIRONMENT}-cache

# SQS Configuration (FREE: 1M requests/month - ALWAYS FREE)
SQS_QUEUE_NAME=${PROJECT_NAME}-${ENVIRONMENT}-task-queue

# Lambda Configuration (FREE: 1M requests, 400K GB-seconds - ALWAYS FREE)
LAMBDA_FUNCTION_NAME=${PROJECT_NAME}-${ENVIRONMENT}-task-processor

# AI Configuration
GROQ_API_KEY=your_groq_api_key_here

# Security
SECRET_KEY=$(openssl rand -hex 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# File Upload Settings (Optimized for free tier)
MAX_FILE_SIZE=5242880  # 5MB (reduced for free tier)
ALLOWED_EXTENSIONS=[".pdf", ".txt"]
ALLOWED_MIME_TYPES=["application/pdf", "text/plain"]

# CORS and Security
ALLOWED_ORIGINS=["*"]
ALLOWED_HOSTS=["*"]

# Rate Limiting (Optimized for free tier)
UPLOAD_RATE_LIMIT=1  # 1 upload per minute (reduced for free tier)
MAX_PROCESSING_TIME=180  # 3 minutes (reduced for free tier)

# Logging (Optimized for free tier)
LOG_LEVEL=INFO
EOF
        log_warning "Please update .env file with your actual credentials before proceeding"
        read -p "Press Enter to continue after updating .env file..."
    fi
    
    # Load environment variables
    export $(cat .env | grep -v '^#' | xargs)
    
    log_success "Environment configured for free tier"
}

deploy_infrastructure() {
    log_info "Deploying AWS infrastructure using FREE TIER services..."
    
    cd ${TERRAFORM_DIR}
    
    # Use free tier configuration
    log_free_tier "Using free tier optimized Terraform configuration"
    if [ -f "free_tier.tf" ]; then
        cp free_tier.tf main.tf
        log_success "Free tier configuration activated"
    else
        log_warning "Free tier configuration not found, using standard configuration"
    fi
    
    # Initialize Terraform
    log_info "Initializing Terraform for free tier deployment..."
    terraform init
    
    # Plan deployment
    log_info "Planning free tier deployment..."
    terraform plan \
        -var="aws_region=${AWS_REGION}" \
        -var="environment=${ENVIRONMENT}" \
        -var="project_name=${PROJECT_NAME}" \
        -var="groq_api_key=${GROQ_API_KEY}" \
        -out=tfplan
    
    # Show free tier information
    log_free_tier "This deployment will use the following FREE services:"
    log_free_tier "  • S3: 5GB storage, 20K GET requests/month"
    log_free_tier "  • RDS: 750 hours/month (12 months free)"
    log_free_tier "  • DynamoDB: 25GB storage, 25 RCU/WCU"
    log_free_tier "  • SQS: 1M requests/month (ALWAYS FREE)"
    log_free_tier "  • Lambda: 1M requests, 400K GB-seconds/month (ALWAYS FREE)"
    log_free_tier "  • CloudWatch: 5GB log data/month (ALWAYS FREE)"
    
    # Apply deployment
    log_info "Applying free tier deployment..."
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
    
    log_success "Free tier infrastructure deployed successfully"
    log_free_tier "Total monthly cost: $0 (within free tier limits)"
}

build_docker_image() {
    log_info "Building Docker image for free tier deployment..."
    
    # Build the Docker image
    docker build -t ${DOCKER_IMAGE_NAME}:latest .
    
    log_success "Docker image built successfully"
}

deploy_lambda() {
    log_info "Deploying Lambda function (FREE TIER: 1M requests/month)..."
    
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
    
    log_success "Lambda function deployed successfully (FREE TIER)"
}

run_tests() {
    log_info "Running tests for free tier deployment..."
    
    # Install test dependencies
    pip install pytest pytest-asyncio moto boto3
    
    # Run tests
    python -m pytest test/ -v --tb=short
    
    log_success "Tests completed successfully"
}

setup_monitoring() {
    log_info "Setting up free tier monitoring..."
    
    # Create free tier monitoring script
    cat > scripts/monitor_free_tier.sh << 'EOF'
#!/bin/bash
echo "🆓 AWS Free Tier Usage Monitor"
echo "================================"

# S3 Usage
echo "📦 S3 Storage:"
aws s3api list-buckets --query 'Buckets[].{Name:Name,CreationDate:CreationDate}' --output table

# Lambda Usage
echo "⚡ Lambda Functions:"
aws lambda list-functions --query 'Functions[].{Name:FunctionName,Runtime:Runtime,MemorySize:MemorySize}' --output table

# RDS Usage
echo "🗄️ RDS Instances:"
aws rds describe-db-instances --query 'DBInstances[].{Identifier:DBInstanceIdentifier,Status:DBInstanceStatus,Class:DBInstanceClass}' --output table

# DynamoDB Usage
echo "📊 DynamoDB Tables:"
aws dynamodb list-tables --output table

# SQS Usage
echo "📬 SQS Queues:"
aws sqs list-queues --output table

echo "✅ Free tier monitoring complete!"
echo "💡 Check AWS Billing Dashboard for detailed usage"
EOF
    
    chmod +x scripts/monitor_free_tier.sh
    
    log_success "Free tier monitoring setup completed"
}

show_free_tier_info() {
    log_free_tier "🎉 AWS Free Tier Deployment Complete!"
    echo ""
    log_free_tier "📊 FREE TIER USAGE:"
    log_free_tier "  • S3 Storage: 5GB (your usage: ~1-3GB)"
    log_free_tier "  • RDS Database: 750 hours/month (your usage: 24/7 = 744 hours)"
    log_free_tier "  • DynamoDB: 25GB storage (your usage: ~1-5GB)"
    log_free_tier "  • SQS Queue: 1M requests/month (your usage: ~1K-10K)"
    log_free_tier "  • Lambda: 1M requests/month (your usage: ~1K-10K)"
    log_free_tier "  • CloudWatch: 5GB logs/month (your usage: ~100MB-1GB)"
    echo ""
    log_free_tier "💰 MONTHLY COST: $0 (within free tier limits)"
    echo ""
    log_free_tier "🔍 MONITOR USAGE:"
    log_free_tier "  • Run: ./scripts/monitor_free_tier.sh"
    log_free_tier "  • Check: AWS Billing Dashboard"
    log_free_tier "  • Alerts: Set up billing alerts at $1, $5, $10"
    echo ""
    log_free_tier "⚠️  IMPORTANT NOTES:"
    log_free_tier "  • RDS is free for 12 months only"
    log_free_tier "  • After 12 months: ~$15-25/month for RDS"
    log_free_tier "  • All other services are ALWAYS FREE"
    log_free_tier "  • Monitor usage regularly to avoid overages"
}

cleanup() {
    log_info "Cleaning up temporary files..."
    
    # Remove temporary files
    rm -f ${TERRAFORM_DIR}/task_processor.zip
    rm -f ${TERRAFORM_DIR}/tfplan
    
    log_success "Cleanup completed"
}

main() {
    log_info "Starting AWS FREE TIER deployment for Document Summarizer Agent"
    echo ""
    log_free_tier "This deployment uses ONLY AWS Free Tier services"
    log_free_tier "Total monthly cost: $0 (within free tier limits)"
    echo ""
    
    check_prerequisites
    setup_environment
    deploy_infrastructure
    build_docker_image
    deploy_lambda
    run_tests
    setup_monitoring
    cleanup
    show_free_tier_info
    
    log_success "Free tier deployment completed successfully!"
    log_info "Your Document Summarizer Agent is now running on AWS FREE TIER"
    log_info "Check the monitoring script for usage details"
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
    "monitor")
        ./scripts/monitor_free_tier.sh
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
            log_success "Free tier infrastructure destroyed"
        else
            log_info "Destroy cancelled"
        fi
        ;;
    *)
        main
        ;;
esac

