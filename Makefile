check-user:
ifndef USER_NAME
	$(error Please provide a user name with building/pushing a Docker image (e.g. make USER_NAME=<your-name> docker-build))
endif

check-region:
ifndef GCP_REGION
	$(error Please provide a GCP region with building/pushing a Docker image (e.g. make GCP_REGION=<region> docker-build))
endif

check-project-id:
ifndef PROJECT_ID
	$(error Please provide a project-id with building/pushing a Docker image (e.g. make PROJECT_ID=<project-id> docker-build))
endif

.PHONY: docker-init
docker-init:
	gcloud auth configure-docker ${GCP_REGION}-docker.pkg.dev

.PHONY: docker-build
docker-build: check-user check-region check-project-id
	docker build -t ${GCP_REGION}-docker.pkg.dev/${PROJECT_ID}/docker/fancy-fashion-${USER_NAME} .

.PHONY: docker-run
docker-run: docker-build
	docker run --rm -it ${GCP_REGION}-docker.pkg.dev/${PROJECT_ID}/docker/fancy-fashion-${USER_NAME} fancy-fashion --help

.PHONY: docker-push
docker-push: docker-build
	docker push ${GCP_REGION}-docker.pkg.dev/${PROJECT_ID}/docker/fancy-fashion-${USER_NAME}

.PHONY: python-init
python-init:
	poetry env use /opt/conda/envs/python3.9/bin/python
	poetry install

.PHONY: python-format
python-format:
	poetry run black src tests

.PHONY: python-lint
python-lint:
	poetry run pre-commit run --all

.PHONY: python-test
python-test:
	poetry run pytest

.PHONY: generate-data
generate-data: python-init
	poetry run python scripts/generate_data.py && gsutil -m cp -r ./data/ gs://{PROJECT_ID}-fashion-inputs/
