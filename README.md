# lambda-template

Template for quickly deploying Python projects as AWS Lambda functions.

In an existing Python project, where the lambda handler is at `lambda_handler.handler`, copy `Dockerfile` and `deploy-lambda.sh`. Then, in a terminal, run `sh deploy-lambda.sh`.

Will upload the Docker image to ECR then deploy to lambda. If these do not exist, will create them, otherwise will update.
