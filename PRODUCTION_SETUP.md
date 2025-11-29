# 🚀 Production Setup Guide - Document Summarizer Agent

This guide will help you deploy the Document Summarizer Agent to AWS production environment using modern cloud-native services.

## 📋 Prerequisites

### Required Tools
- **AWS CLI** v2.0+ - [Install Guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- **Terraform** v1.0+ - [Install Guide](https://learn.hashicorp.com/tutorials/terraform/install-cli)
- **Docker** v20.0+ - [Install Guide](https://docs.docker.com/get-docker/)
- **Python** v3.11+ - [Install Guide](https://www.python.org/downloads/)

### AWS Account Setup
1. **Create AWS Account** - Sign up at [aws.amazon.com](https://aws.amazon.com)
2. **Configure AWS CLI** - Run `aws configure` with your credentials
3. **Set up IAM User** - Create a user with appropriate permissions (see IAM section below)

### API Keys Required
- **Groq API Key** - Get from [console.groq.com](https://console.groq.com)
- **AWS Access Keys** - From your AWS IAM user

## 🏗️ Architecture Overview

### Production Stack
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI       │    │   AWS S3        │    │   AWS RDS       │
│   (ECS/Fargate) │◄──►│   (File Storage)│    │   (PostgreSQL)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   AWS SQS       │    │   DynamoDB      │    │   AWS Lambda    │
│   (Task Queue)  │    │   (Caching)     │    │   (Processing)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Key Changes from Development
- ✅ **MinIO** → **AWS S3** (Object Storage)
- ✅ **Redis** → **DynamoDB + ElastiCache** (Caching)
- ✅ **Celery** → **AWS SQS + Lambda** (Task Processing)
- ✅ **Local PostgreSQL** → **AWS RDS** (Database)
- ✅ **Docker Compose** → **Terraform + ECS** (Infrastructure)

## 🚀 Quick Start Deployment

### 1. Clone and Setup
```bash
git clone <your-repo>
cd Document-Summarizer-Agent

# Copy environment template
cp env.example .env

# Edit configuration
nano .env
```

### 2. Configure Environment
Update `.env` with your values:
```bash
# AWS Configuration
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1

# S3 Configuration
S3_BUCKET_NAME=your-unique-bucket-name

# Database (will be updated by Terraform)
DATABASE_URL=postgresql://postgres:password@localhost:5432/docprocessing

# AI Configuration
GROQ_API_KEY=your_groq_api_key

# Security
SECRET_KEY=$(openssl rand -hex 32)
```

### 3. Deploy Infrastructure
```bash
# Make deployment script executable
chmod +x scripts/deploy_aws.sh

# Deploy everything
./scripts/deploy_aws.sh

# Or deploy step by step
./scripts/deploy_aws.sh infrastructure  # Deploy AWS resources
./scripts/deploy_aws.sh lambda         # Deploy Lambda function
./scripts/deploy_aws.sh test           # Run tests
```

### 4. Verify Deployment
```bash
# Check health endpoint
curl https://your-api-endpoint.com/health

# Test upload
curl -X POST https://your-api-endpoint.com/upload \
  -H "Authorization: Bearer your_jwt_token" \
  -F "file=@sample.pdf"
```

## 🔧 Detailed Configuration

### AWS Services Configuration

#### S3 Bucket
- **Purpose**: Store uploaded PDF files
- **Features**: Versioning, encryption, lifecycle policies
- **Access**: Private with presigned URLs

#### RDS PostgreSQL
- **Instance**: db.t3.micro (free tier eligible)
- **Storage**: 20GB with auto-scaling
- **Backup**: 7-day retention
- **Security**: VPC-only access

#### DynamoDB
- **Purpose**: Caching and session storage
- **Billing**: Pay-per-request
- **Features**: TTL, encryption at rest

#### SQS Queue
- **Purpose**: Task queue for document processing
- **Features**: Dead letter queue, long polling
- **Visibility**: 5-minute timeout

#### Lambda Function
- **Purpose**: Process documents asynchronously
- **Runtime**: Python 3.11
- **Memory**: 512MB
- **Timeout**: 5 minutes
- **Trigger**: SQS events

### Security Configuration

#### IAM Permissions Required
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:*",
        "rds:*",
        "dynamodb:*",
        "sqs:*",
        "lambda:*",
        "ec2:*",
        "iam:*",
        "cloudformation:*"
      ],
      "Resource": "*"
    }
  ]
}
```

#### Network Security
- **VPC**: Isolated network environment
- **Security Groups**: Restrictive access rules
- **NACLs**: Additional network protection
- **Encryption**: All data encrypted in transit and at rest

## 📊 Monitoring and Observability

### CloudWatch Integration
- **Logs**: Centralized logging for all services
- **Metrics**: Custom metrics for business logic
- **Alarms**: Automated alerting for failures
- **Dashboards**: Real-time monitoring

### Health Checks
- **API Health**: `/health` endpoint
- **Database**: Connection monitoring
- **S3**: Bucket accessibility
- **Lambda**: Function execution status

### Performance Monitoring
- **Response Times**: API endpoint performance
- **Throughput**: Requests per second
- **Error Rates**: 4xx/5xx error tracking
- **Resource Usage**: CPU, memory, storage

## 🧪 Testing Strategy

### Test Types
1. **Unit Tests** - Individual component testing
2. **Integration Tests** - Service interaction testing
3. **Load Tests** - Performance under load
4. **Security Tests** - Vulnerability scanning

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio moto boto3

# Run all tests
python -m pytest test/ -v

# Run specific test categories
python -m pytest test/test_aws_services.py -v
python -m pytest test/test_integration.py -v
```

### Test Coverage
- **API Endpoints**: All endpoints tested
- **AWS Services**: Mocked and real service testing
- **Error Handling**: Exception scenarios
- **Security**: Authentication and authorization

## 💰 Cost Optimization

### Free Tier Usage
- **RDS**: 750 hours/month (db.t3.micro)
- **S3**: 5GB storage, 20,000 GET requests
- **Lambda**: 1M requests, 400,000 GB-seconds
- **DynamoDB**: 25GB storage, 25 RCU/WCU

### Cost Monitoring
- **AWS Cost Explorer**: Track spending by service
- **Billing Alerts**: Set up budget notifications
- **Resource Tagging**: Track costs by environment

### Optimization Strategies
- **Auto Scaling**: Scale based on demand
- **Reserved Instances**: For predictable workloads
- **Spot Instances**: For non-critical tasks
- **Lifecycle Policies**: Archive old data

## 🔄 CI/CD Pipeline

### GitHub Actions (Recommended)
```yaml
name: Deploy to AWS
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
      - name: Deploy infrastructure
        run: ./scripts/deploy_aws.sh infrastructure
      - name: Deploy application
        run: ./scripts/deploy_aws.sh lambda
```

### Manual Deployment
```bash
# Deploy infrastructure only
./scripts/deploy_aws.sh infrastructure

# Deploy Lambda function
./scripts/deploy_aws.sh lambda

# Run tests
./scripts/deploy_aws.sh test

# Full deployment
./scripts/deploy_aws.sh
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. AWS Credentials
```bash
# Check credentials
aws sts get-caller-identity

# Configure if needed
aws configure
```

#### 2. Terraform State
```bash
# Initialize Terraform
cd infra/terraform
terraform init

# Check state
terraform show
```

#### 3. Lambda Deployment
```bash
# Check Lambda function
aws lambda get-function --function-name document-summarizer-production-task-processor

# View logs
aws logs tail /aws/lambda/document-summarizer-production-task-processor --follow
```

#### 4. Database Connection
```bash
# Test database connection
psql $DATABASE_URL -c "SELECT 1;"
```

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Run with verbose output
python -m uvicorn api.main:app --reload --log-level debug
```

## 📈 Scaling Considerations

### Horizontal Scaling
- **API**: Multiple ECS tasks behind ALB
- **Lambda**: Automatic scaling based on SQS queue depth
- **Database**: Read replicas for read-heavy workloads

### Vertical Scaling
- **RDS**: Upgrade instance class
- **Lambda**: Increase memory allocation
- **S3**: No scaling needed (unlimited)

### Performance Optimization
- **Caching**: ElastiCache for frequently accessed data
- **CDN**: CloudFront for static content
- **Compression**: Gzip compression for API responses

## 🔒 Security Best Practices

### Data Protection
- **Encryption**: All data encrypted at rest and in transit
- **Access Control**: IAM roles with least privilege
- **Network Security**: VPC with private subnets
- **Audit Logging**: CloudTrail for API calls

### Compliance
- **GDPR**: Data retention and deletion policies
- **SOC 2**: Security controls implementation
- **HIPAA**: Healthcare data protection (if applicable)

## 📚 Additional Resources

### Documentation
- [AWS Documentation](https://docs.aws.amazon.com/)
- [Terraform Documentation](https://www.terraform.io/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

### Support
- **AWS Support**: For infrastructure issues
- **Community**: GitHub Issues for code problems
- **Documentation**: This guide and inline comments

### Updates
- **Security Patches**: Regular dependency updates
- **Feature Updates**: Follow semantic versioning
- **Breaking Changes**: Documented in CHANGELOG.md

---

## 🎉 Congratulations!

Your Document Summarizer Agent is now running in production on AWS! 

### Next Steps
1. **Monitor** your application using CloudWatch
2. **Scale** based on usage patterns
3. **Optimize** costs using AWS Cost Explorer
4. **Secure** your application following best practices

### Need Help?
- Check the troubleshooting section above
- Review AWS documentation
- Open an issue on GitHub
- Contact your DevOps team

Happy processing! 🚀

