# Serverless API Example

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

Go to the root directory of this repo and install the _serverless-localstack_ plugin:
```bash
cd serverless_api_example

npm install --save-dev serverless-localstack
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
✔ Service deployed to stack todos-service (22s)

endpoint: http://localhost:4566/restapis/{{ENDPOINT URL}}/local/_user_request_
functions:
  create: todos-service-create
  list: todos-service-list
  get: todos-service-get
  update: todos-service-update
  delete: todos-service-delete
```


## Check out the API

You can use the [Postman Collection in this repo](/postman_collection.json) to interact with the API.
Just import it into Postman and configure the collection variables.


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
