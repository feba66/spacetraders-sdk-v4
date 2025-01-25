all: .venv tmp/generated

tmp/generated: tmp/openapi-generator-cli.jar tmp/SpaceTraders.json
	java -jar tmp/openapi-generator-cli.jar generate -g python-pydantic-v1 -o tmp/generated -i tmp/SpaceTraders.json
	python3 ratelimit_generated.py

tmp/openapi-generator-cli.jar:
	wget https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/7.9.0/openapi-generator-cli-7.9.0.jar -O tmp/openapi-generator-cli.jar

tmp/SpaceTraders.json:
#	# wget https://stoplight.io/api/v1/projects/spacetraders/spacetraders/nodes/reference/SpaceTraders.json?fromExportButton=true&snapshotType=http_service&deref=optimizedBundle --output-document=SpaceTraders.json
	curl "https://stoplight.io/api/v1/projects/spacetraders/spacetraders/nodes/reference/SpaceTraders.json?fromExportButton=true&snapshotType=http_service&deref=optimizedBundle" >> tmp/SpaceTraders.json

.venv:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt
	. .venv/bin/activate && poetry install

.PHONY: tmp/generated