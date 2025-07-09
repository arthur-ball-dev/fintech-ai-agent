# Deployment Guide

Guide for deploying the FinTech AI Agent Framework in production environments.

## 🚀 Deployment Options

### Local Development
```bash
# Standard local setup
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configure environment
export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"

# Run application
python src/examples/run_fintech_agents.py
```

### Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.8-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY src/ ./src/
COPY tests/ ./tests/

# Set environment variables
ENV PYTHONPATH=/app

# Run application
CMD ["python", "src/examples/run_fintech_agents.py"]
```

Build and run:
```bash
# Build image
docker build -t fintech-ai-agent .

# Run container
docker run -it \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  fintech-ai-agent
```

### Cloud Deployment (AWS Example)

#### EC2 Instance
```bash
# Install Python 3.8+
sudo apt-get update
sudo apt-get install python3.8 python3.8-venv

# Clone repository
git clone <repository-url>
cd fintech-ai-agent

# Setup environment
python3.8 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configure secrets (use AWS Secrets Manager)
export OPENAI_API_KEY=$(aws secretsmanager get-secret-value --secret-id openai-key --query SecretString --output text)
export ANTHROPIC_API_KEY=$(aws secretsmanager get-secret-value --secret-id anthropic-key --query SecretString --output text)
```

#### Lambda Function
```python
# lambda_handler.py
import os
from src.agents.file_explorer import create_agent_by_key

def lambda_handler(event, context):
    # Get analysis type from event
    analysis_type = event.get('analysis_type', 'fintech_comprehensive')
    project_path = event.get('project_path', '.')
    
    # Create and run agent
    agent = create_agent_by_key(analysis_type)
    memory = agent.run(f"Analyze {project_path}")
    
    # Return results
    return {
        'statusCode': 200,
        'body': memory.get_memories()[-1]['content']
    }
```

## 🔒 Production Security

### Environment Variables
```bash
# Use secret management service
# AWS Secrets Manager
aws secretsmanager create-secret --name fintech-ai-keys --secret-string '{
  "OPENAI_API_KEY": "sk-...",
  "ANTHROPIC_API_KEY": "sk-ant-..."
}'

# Azure Key Vault
az keyvault secret set --vault-name fintech-vault --name openai-key --value "sk-..."

# HashiCorp Vault
vault kv put secret/fintech openai_key="sk-..." anthropic_key="sk-ant-..."
```

### Network Security
- Deploy behind VPC with restricted access
- Use private subnets for processing
- Implement API Gateway for external access
- Enable SSL/TLS for all communications

### Access Control
```yaml
# IAM Policy Example
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue"
      ],
      "Resource": "arn:aws:secretsmanager:region:account:secret:fintech-ai-*"
    }
  ]
}
```

## 📊 Monitoring & Logging

### CloudWatch Configuration
```python
import logging
import watchtower

# Configure CloudWatch logging
logger = logging.getLogger(__name__)
handler = watchtower.CloudWatchLogHandler(
    log_group='fintech-ai-agent',
    stream_name='analysis-logs'
)
logger.addHandler(handler)
```

### Metrics to Monitor
- Analysis execution time
- LLM API response times
- Error rates by provider
- Cost per analysis
- Memory usage

### Alerts Configuration
```yaml
# CloudWatch Alarm Example
AlarmName: HighErrorRate
MetricName: Errors
Threshold: 5
ComparisonOperator: GreaterThanThreshold
EvaluationPeriods: 2
Period: 300
```

## 🔄 CI/CD Pipeline

### GitHub Actions Example
```yaml
name: Deploy FinTech AI Agent

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      - name: Run tests
        run: |
          pip install -r requirements-test.txt
          pytest
  
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to AWS
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        run: |
          # Deployment script
```

## 🎯 Performance Optimization

### Caching Strategy
```python
# Redis caching for analysis results
import redis
import hashlib
import json

cache = redis.Redis(host='localhost', port=6379, db=0)

def get_cached_analysis(project_path, analysis_type):
    cache_key = hashlib.md5(f"{project_path}:{analysis_type}".encode()).hexdigest()
    cached = cache.get(cache_key)
    if cached:
        return json.loads(cached)
    return None

def cache_analysis(project_path, analysis_type, result, ttl=3600):
    cache_key = hashlib.md5(f"{project_path}:{analysis_type}".encode()).hexdigest()
    cache.setex(cache_key, ttl, json.dumps(result))
```

### Scaling Considerations
- Use connection pooling for LLM providers
- Implement request queuing for high volume
- Consider read replicas for file systems
- Use CDN for static analysis reports

## 📋 Deployment Checklist

- [ ] Environment variables configured
- [ ] API keys stored securely
- [ ] Network security configured
- [ ] Monitoring enabled
- [ ] Logging configured
- [ ] Error handling tested
- [ ] Backup strategy defined
- [ ] Recovery procedures documented
- [ ] Performance benchmarked
- [ ] Security scan completed

## 🆘 Troubleshooting

### Common Issues

**LLM Provider Timeouts**
```python
# Increase timeout settings
client = LLMClient(timeout=60)
```

**Memory Issues**
```bash
# Increase container memory
docker run -m 4g fintech-ai-agent
```

**Rate Limiting**
```python
# Implement exponential backoff
import time
from functools import wraps

def retry_with_backoff(max_retries=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except RateLimitError:
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
            raise
        return wrapper
    return decorator
```

This deployment guide provides a foundation for deploying the FinTech AI Agent Framework in production environments with enterprise-grade security and reliability.