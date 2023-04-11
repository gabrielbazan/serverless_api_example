# Serverless API Example

<p align="center">
    <a href="https://github.com/application-creators/create_app/actions"><img alt="Test Workflow Status" src="https://github.com/gabrielbazan/serverless_api_example/workflows/Test/badge.svg"></a>
    <!-- <a href="https://coveralls.io/github/application-creators/create_app?branch=main"><img alt="Coverage Status" src="https://coveralls.io/repos/github/application-creators/create_app/badge.svg?branch=main"></a> -->
    <a href="https://github.com/pre-commit/pre-commit"><img alt="Pre-commit" src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white"></a>
    <a href="http://mypy-lang.org/"><img alt="Checked with mypy" src="http://www.mypy-lang.org/static/mypy_badge.svg"></a>
    <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>


A TODOs REST API put together with Serverless Framework, which uses the following AWS services:
 1. AWS API Gateway
 2. AWS Lambda
 3. AWS DynamoDB


## Structure

The application is located at the [todos](/todos) package. Each AWS Lambda handler function is on a separate file.


## Setup

### Install the Serverless Framework
```bash
npm install -g serverless
```

### Install LocalStack:
```bash
pip install localstack
```

### Install Serverless Framework Plugins

Go to the root directory of this repo and install the plugins:
```bash
cd serverless_api_example

npm i
```

### Install and Configure the AWS CLI

Follow [these instructions](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) to install the AWS CLI.

To interact with LocalStack through the AWS CLI, you can create a profile with dummy region and access key.

Add this to your `~/.aws/config` file:
```
[profile localstack]
region = us-east-1
output = json
```

And this to your `~/.aws/credentials` file:
```
[localstack]
aws_access_key_id = dummyaccesskey
aws_secret_access_key = dummysecretaccesskey
```

## Deploy to LocalStack

Start LocalStack:
```bash
localstack start
```

Deploy to LocalStack:
```bash
serverless deploy --stage local
```

You should get something like the following. Notice the endpoint URL:
```
✔ Service deployed to stack todos-service

endpoint: http://localhost:4566/restapis/{{ENDPOINT URL}}/local/_user_request_
functions:
  create: todos-service-create
  list: todos-service-list
  get: todos-service-read
  update: todos-service-update
  delete: todos-service-delete
```

You can alternatively start localstack as a daemon and deploy with a single command:
```bash
make deploy_local
```


## Check the API out

You can use the [Postman Collection in this repo](/postman_collection.json) to interact with the API.
Just import it into Postman and set the collection variables (the API ID, mainly).


## Useful Stuff

### Redeploy a Function

To redeploy just one Lambda instead of the whole service, run:
```bash
serverless deploy function --function update --stage local
```

That will deploy the "update" function.


### Check the logs of a function

This would show and follow the execution logs of the "update" function:
```bash
aws --endpoint-url=http://localhost:4566 --profile localstack logs tail /aws/lambda/todos-service-local-update --follow
```


### Get the URL where the Lambda code .zip file is

```bash
aws lambda get-function --profile localstack --endpoint-url=http://localhost:4566 --function-name todos-service-local-list --query 'Code.Location'
```


### Layers

Although you can only use layers in LocalStack **Pro**, these can be useful if you paid for it.

#### List layers
```bash
aws lambda list-layers --profile localstack --endpoint-url=http://localhost:4566 --query Content.Location --output text
```

#### Get layer source code by ARN (works on LocalStack)
```bash
aws lambda get-layer-version-by-arn --profile localstack --endpoint-url=http://localhost:4566 --arn arn:aws:lambda:us-east-1:000000000000:layer:todos-service-local-python-requirements:1 --query Content.Location --output text
```

#### Get layer source code by layer name (does NOT work on LocalStack)
```bash
aws lambda get-layer-version --profile localstack --endpoint-url=http://localhost:4566 --layer-name pythonRequirements --version-number 1 --query Content.Location --output text
```
