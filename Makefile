

deploy_local:
	localstack stop || true
	localstack start -d
	sls deploy --stage local
