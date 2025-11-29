# AWS Free Tier Optimized Configuration
# This configuration is designed to stay within AWS Free Tier limits

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Variables
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "free-tier"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "document-summarizer"
}

# Data sources
data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

# S3 Bucket for file storage (FREE TIER: 5GB storage, 20,000 GET requests)
resource "aws_s3_bucket" "document_storage" {
  bucket = "${var.project_name}-${var.environment}-documents-${random_string.bucket_suffix.result}"
  
  tags = {
    Name        = "Document Storage - Free Tier"
    Environment = var.environment
    Project     = var.project_name
    CostCenter  = "FreeTier"
  }
}

resource "random_string" "bucket_suffix" {
  length  = 8
  special = false
  upper   = false
}

resource "aws_s3_bucket_versioning" "document_storage" {
  bucket = aws_s3_bucket.document_storage.id
  versioning_configuration {
    status = "Disabled"  # Disable versioning to save costs
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "document_storage" {
  bucket = aws_s3_bucket.document_storage.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "document_storage" {
  bucket = aws_s3_bucket.document_storage.id
  
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# RDS PostgreSQL Database (FREE TIER: 750 hours/month for 12 months)
resource "aws_db_subnet_group" "main" {
  name       = "${var.project_name}-${var.environment}-db-subnet-group"
  subnet_ids = aws_subnet.private[*].id
  
  tags = {
    Name        = "DB subnet group - Free Tier"
    Environment = var.environment
    CostCenter  = "FreeTier"
  }
}

resource "aws_db_instance" "postgres" {
  identifier = "${var.project_name}-${var.environment}-postgres"
  
  engine         = "postgres"
  engine_version = "15.4"
  instance_class = "db.t3.micro"  # Free tier eligible
  
  allocated_storage     = 20  # Free tier: 20GB
  max_allocated_storage = 20  # Limit to free tier
  storage_type          = "gp2"
  storage_encrypted     = true
  
  db_name  = "docprocessing"
  username = "postgres"
  password = random_password.db_password.result
  
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
  
  backup_retention_period = 0  # Disable backups to save costs
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  skip_final_snapshot = true
  deletion_protection = false
  
  # Free tier optimizations
  auto_minor_version_upgrade = false
  performance_insights_enabled = false
  monitoring_interval = 0
  monitoring_role_arn = null
  
  tags = {
    Name        = "PostgreSQL Database - Free Tier"
    Environment = var.environment
    CostCenter  = "FreeTier"
  }
}

resource "random_password" "db_password" {
  length  = 16
  special = true
}

# DynamoDB Table for caching (FREE TIER: 25GB storage, 25 RCU/WCU)
resource "aws_dynamodb_table" "cache" {
  name           = "${var.project_name}-${var.environment}-cache"
  billing_mode   = "PAY_PER_REQUEST"  # Free tier friendly
  hash_key       = "cache_key"
  
  attribute {
    name = "cache_key"
    type = "S"
  }
  
  ttl {
    attribute_name = "ttl"
    enabled        = true
  }
  
  # Free tier optimizations
  point_in_time_recovery {
    enabled = false  # Disable to save costs
  }
  
  tags = {
    Name        = "Cache Table - Free Tier"
    Environment = var.environment
    CostCenter  = "FreeTier"
  }
}

# SQS Queue for task processing (FREE TIER: 1 million requests/month - ALWAYS FREE)
resource "aws_sqs_queue" "task_queue" {
  name = "${var.project_name}-${var.environment}-task-queue"
  
  visibility_timeout_seconds = 300
  message_retention_seconds  = 1209600  # 14 days
  receive_wait_time_seconds  = 20
  
  tags = {
    Name        = "Task Queue - Free Tier"
    Environment = var.environment
    CostCenter  = "FreeTier"
  }
}

# Dead Letter Queue (FREE TIER: 1 million requests/month - ALWAYS FREE)
resource "aws_sqs_queue" "task_dlq" {
  name = "${var.project_name}-${var.environment}-task-dlq"
  
  message_retention_seconds = 1209600  # 14 days
  
  tags = {
    Name        = "Task Dead Letter Queue - Free Tier"
    Environment = var.environment
    CostCenter  = "FreeTier"
  }
}

# Lambda function for task processing (FREE TIER: 1M requests, 400,000 GB-seconds - ALWAYS FREE)
resource "aws_lambda_function" "task_processor" {
  filename         = "task_processor.zip"
  function_name    = "${var.project_name}-${var.environment}-task-processor"
  role            = aws_iam_role.lambda_role.arn
  handler         = "tasks.aws_task_processor.lambda_handler"
  runtime         = "python3.11"
  timeout         = 300
  memory_size     = 128  # Reduced memory for free tier
  
  environment {
    variables = {
      DATABASE_URL = "postgresql://postgres:${random_password.db_password.result}@${aws_db_instance.postgres.endpoint}/docprocessing"
      S3_BUCKET_NAME = aws_s3_bucket.document_storage.bucket
      DYNAMODB_CACHE_TABLE = aws_dynamodb_table.cache.name
      SQS_QUEUE_URL = aws_sqs_queue.task_queue.url
      GROQ_API_KEY = var.groq_api_key
    }
  }
  
  vpc_config {
    subnet_ids         = aws_subnet.private[*].id
    security_group_ids = [aws_security_group.lambda.id]
  }
  
  depends_on = [aws_cloudwatch_log_group.lambda_logs]
  
  tags = {
    Name        = "Task Processor Lambda - Free Tier"
    Environment = var.environment
    CostCenter  = "FreeTier"
  }
}

variable "groq_api_key" {
  description = "Groq API key"
  type        = string
  sensitive   = true
}

# CloudWatch Log Group for Lambda (FREE TIER: 5GB log data ingestion - ALWAYS FREE)
resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/${var.project_name}-${var.environment}-task-processor"
  retention_in_days = 7  # Reduced retention for free tier
  
  tags = {
    Name        = "Lambda Logs - Free Tier"
    Environment = var.environment
    CostCenter  = "FreeTier"
  }
}

# SQS Event Source Mapping
resource "aws_lambda_event_source_mapping" "sqs_trigger" {
  event_source_arn = aws_sqs_queue.task_queue.arn
  function_name    = aws_lambda_function.task_processor.arn
  batch_size       = 1  # Reduced batch size for free tier
  maximum_batching_window_in_seconds = 0
}

# VPC and Networking (FREE TIER: No additional charges for basic VPC)
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name        = "${var.project_name}-${var.environment}-vpc"
    Environment = var.environment
    CostCenter  = "FreeTier"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  
  tags = {
    Name        = "${var.project_name}-${var.environment}-igw"
    Environment = var.environment
    CostCenter  = "FreeTier"
  }
}

resource "aws_subnet" "public" {
  count = 2
  
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.${count.index + 1}.0/24"
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true
  
  tags = {
    Name        = "${var.project_name}-${var.environment}-public-${count.index + 1}"
    Environment = var.environment
    Type        = "Public"
    CostCenter  = "FreeTier"
  }
}

resource "aws_subnet" "private" {
  count = 2
  
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 10}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]
  
  tags = {
    Name        = "${var.project_name}-${var.environment}-private-${count.index + 1}"
    Environment = var.environment
    Type        = "Private"
    CostCenter  = "FreeTier"
  }
}

data "aws_availability_zones" "available" {
  state = "available"
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
  
  tags = {
    Name        = "${var.project_name}-${var.environment}-public-rt"
    Environment = var.environment
    CostCenter  = "FreeTier"
  }
}

resource "aws_route_table_association" "public" {
  count = 2
  
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

# Security Groups (FREE TIER: No additional charges)
resource "aws_security_group" "rds" {
  name_prefix = "${var.project_name}-${var.environment}-rds-"
  vpc_id      = aws_vpc.main.id
  
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.main.cidr_block]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name        = "RDS Security Group - Free Tier"
    Environment = var.environment
    CostCenter  = "FreeTier"
  }
}

resource "aws_security_group" "lambda" {
  name_prefix = "${var.project_name}-${var.environment}-lambda-"
  vpc_id      = aws_vpc.main.id
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name        = "Lambda Security Group - Free Tier"
    Environment = var.environment
    CostCenter  = "FreeTier"
  }
}

# IAM Roles and Policies (FREE TIER: No additional charges)
resource "aws_iam_role" "lambda_role" {
  name = "${var.project_name}-${var.environment}-lambda-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
  
  tags = {
    Name        = "Lambda Role - Free Tier"
    Environment = var.environment
    CostCenter  = "FreeTier"
  }
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

resource "aws_iam_role_policy" "lambda_permissions" {
  name = "${var.project_name}-${var.environment}-lambda-permissions"
  role = aws_iam_role.lambda_role.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ]
        Resource = "${aws_s3_bucket.document_storage.arn}/*"
      },
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:DeleteItem",
          "dynamodb:Query",
          "dynamodb:Scan"
        ]
        Resource = aws_dynamodb_table.cache.arn
      },
      {
        Effect = "Allow"
        Action = [
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes"
        ]
        Resource = aws_sqs_queue.task_queue.arn
      },
      {
        Effect = "Allow"
        Action = [
          "rds:DescribeDBInstances"
        ]
        Resource = "*"
      }
    ]
  })
}

# Outputs
output "s3_bucket_name" {
  description = "Name of the S3 bucket for document storage"
  value       = aws_s3_bucket.document_storage.bucket
}

output "database_endpoint" {
  description = "RDS instance endpoint"
  value       = aws_db_instance.postgres.endpoint
  sensitive   = true
}

output "database_password" {
  description = "RDS instance password"
  value       = random_password.db_password.result
  sensitive   = true
}

output "sqs_queue_url" {
  description = "SQS queue URL"
  value       = aws_sqs_queue.task_queue.url
}

output "dynamodb_table_name" {
  description = "DynamoDB table name"
  value       = aws_dynamodb_table.cache.name
}

output "lambda_function_name" {
  description = "Lambda function name"
  value       = aws_lambda_function.task_processor.function_name
}

output "free_tier_limits" {
  description = "AWS Free Tier limits for this deployment"
  value = {
    s3_storage = "5GB"
    s3_requests = "20,000 GET + 2,000 PUT per month"
    rds_hours = "750 hours/month for 12 months"
    dynamodb_storage = "25GB"
    dynamodb_rcu_wcu = "25 RCU + 25 WCU"
    sqs_requests = "1,000,000 requests/month (ALWAYS FREE)"
    lambda_requests = "1,000,000 requests/month (ALWAYS FREE)"
    lambda_compute = "400,000 GB-seconds/month (ALWAYS FREE)"
    cloudwatch_logs = "5GB log data ingestion/month (ALWAYS FREE)"
  }
}
