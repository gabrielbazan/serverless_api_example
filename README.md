# Serverless API Example

<p align="center">
    <a href="https://github.com/gabrielbazan/serverless_api_example/actions"><img alt="Test Workflow Status" src="https://github.com/gabrielbazan/serverless_api_example/workflows/Test/badge.svg"></a>
    <!-- <a href="https://coveralls.io/github/application-creators/create_app?branch=main"><img alt="Coverage Status" src="https://coveralls.io/repos/github/application-creators/create_app/badge.svg?branch=main"></a> -->
    <a href="https://www.python.org"><img alt="Python version" src="https://img.shields.io/badge/Python-3.8-3776AB.svg?style=flat&logo=python&logoColor=white"></a>
    <a href="https://github.com/pre-commit/pre-commit"><img alt="Pre-commit" src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white"></a>
    <a href="http://mypy-lang.org/"><img alt="Checked with mypy" src="http://www.mypy-lang.org/static/mypy_badge.svg"></a>
    <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

Yet another TODOs REST API. This one is based on AWS Lambdas, accessible through the AWS API Gateway, and persist into a DynamoDB table.

  * It uses [Pydantic](https://docs.pydantic.dev/) for schema valiation.
  * It can be deployed to AWS or LocalStack using the [Serverless Framework](https://www.serverless.com/).

It also includes:
  * Unit tests.
  * Functional tests, which are executed against [LocalStack](https://github.com/localstack/localstack).
  * [Pre-commit](https://pre-commit.com/) hooks: [Black](https://github.com/psf/black), [ISort](https://pycqa.github.io/isort/), [Flake8](https://flake8.pycqa.org/en/latest/), and [MyPy](https://mypy-lang.org/).
  * A [Makefile](https://www.gnu.org/software/make/manual/make.html) with useful commands.
  * A [Postman](https://www.postman.com/) colletion to use the API.


## Structure

The [serverless.yml](/serverless.yml) file contains the Serverless configuration to deploy the stack to either AWS or LocalStack.

The application logic is located in the [todos](/todos) package. Each AWS Lambda handler function is on a separate file. Common code is in the same package.

Unit tests are in the [todos/tests](/todos/tests) package.

Integration tests are in the [integration_tests](/integration_tests) package.

The [postman_collection.json](/postman_collection.json) file is the Postman collection. Go ahead and import it to your account! It has environment variables.

You can find useful commands in the [Makefile](/Makefile).

Python requirements:
  1. The requirements.txt file contains the essential Python dependencies required by the application logic to run.
  2. The requirements.dev.txt file contains the Python dependencies you need to have installed in your environment to contribute to the application logic.
  3. The requirements.test.txt file contains the Python dependencies required to run tests.


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

You can use the [Postman Collection in this repo](/postman_collection.json) to use the API.
Just import it into Postman and set the collection variables (the API ID, mainly).


## Useful Stuff

Just a bunch of commands that may be useful for you.

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

Although you can only use layers if you're using LocalStack **Pro**, the following can be useful if you paid for it.

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
