tmp/generated: openapi-generator-cli.jar SpaceTraders.json
	java -jar openapi-generator-cli.jar generate -g python-pydantic-v1 -o tmp/generated -i SpaceTraders.json
	python3 ratelimit_generated.py

openapi-generator-cli.jar:
	wget https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/7.9.0/openapi-generator-cli-7.9.0.jar -O openapi-generator-cli.jar

SpaceTraders.json:
#	# wget https://stoplight.io/api/v1/projects/spacetraders/spacetraders/nodes/reference/SpaceTraders.json?fromExportButton=true&snapshotType=http_service&deref=optimizedBundle --output-document=SpaceTraders.json
	curl "https://stoplight.io/api/v1/projects/spacetraders/spacetraders/nodes/reference/SpaceTraders.json?fromExportButton=true&snapshotType=http_service&deref=optimizedBundle" >> SpaceTraders.json

.PHONY: tmp/generated