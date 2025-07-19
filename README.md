# FastAPI Application - DevOps Session Lab 1

This repository contains a simple FastAPI application with CI/CD pipeline for automated testing and deployment to AWS EC2 using Docker.

## Features

- FastAPI application with a GET endpoint
- Automated testing with pytest
- Docker containerization
- CI/CD pipeline using GitHub Actions
- Automatic deployment to AWS EC2

## Local Development

### Prerequisites

- Python 3.9+
- Docker (optional for local containerization)

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd DevOps-Session-Lab-1
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application locally:
   ```bash
   uvicorn app:app --reload
   ```

5. Access the API at http://localhost:8000

### Running Tests

```bash
pytest
```

## Docker

### Building the Docker Image

```bash
docker build -t fastapi-app .
```

### Running the Container

```bash
docker run -d -p 8000:8000 --name fastapi-app fastapi-app
```

Access the API at http://localhost:8000

## CI/CD Pipeline

The application uses GitHub Actions for CI/CD:

1. On every push or pull request to the main branch, tests are run
2. When changes are pushed to the main branch, the application is:
   - Tested
   - Built as a Docker image
   - Pushed to Amazon ECR
   - Deployed to an EC2 instance

### Setting up OIDC with AWS

This workflow uses OpenID Connect (OIDC) to authenticate with AWS without storing long-lived credentials in GitHub secrets:

1. Create an IAM OIDC identity provider for GitHub:
   ```
   https://token.actions.githubusercontent.com
   ```

2. Create an IAM role with a trust policy:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": {
           "Federated": "arn:aws:iam::<ACCOUNT_ID>:oidc-provider/token.actions.githubusercontent.com"
         },
         "Action": "sts:AssumeRoleWithWebIdentity",
         "Condition": {
           "StringEquals": {
             "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
           },
           "StringLike": {
             "token.actions.githubusercontent.com:sub": "repo:<GITHUB_USERNAME>/<REPO_NAME>:*"
           }
         }
       }
     ]
   }
   ```

3. Attach policies to the role for ECR access (e.g., `AmazonECR-FullAccess` or a custom policy)

4. Add the role ARN to your GitHub repository secrets as `AWS_ROLE_ARN`

### Required Secrets

To use the GitHub Actions workflow, you need to set up the following secrets in your GitHub repository:

- `AWS_ROLE_ARN`: ARN of the IAM role with permissions for ECR (for OIDC authentication)
- `AWS_REGION`: AWS region (e.g., us-east-1)
- `ECR_REPOSITORY`: Name of your ECR repository
- `EC2_HOST`: Public IP or DNS of your EC2 instance
- `EC2_USERNAME`: SSH username for your EC2 instance (typically 'ec2-user' or 'ubuntu')
- `EC2_SSH_KEY`: SSH private key for accessing the EC2 instance

## EC2 Instance Setup

Your EC2 instance should have:

1. Docker installed
2. AWS CLI configured
3. Permissions to pull from your ECR repository
4. Port 80 open in the security group

## API Endpoints

- `GET /v1/api`: Returns a JSON response with the message "hello form hands on session lab 1"

## License

This project is licensed under the MIT License - see the LICENSE file for details. 