

deploy_local:
	localstack stop
	localstack start -d
	sls deploy --stage local
