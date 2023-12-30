.PHONY: venv
venv:
	. .venv/Scripts/activate

.PHONY: synth
synth:
	cdf synth

.PHONY: deploy
deploy:
	cdk deploy

.PHONY: destroy
destroy:
	cdk destroy
