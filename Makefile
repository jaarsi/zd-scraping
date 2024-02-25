setup:
	@scripts/setup.sh
lint:
	@poetry run scripts/lint.sh
create-report:
	@poetry run scripts/create-report.sh "$${ARGS}"
create-report-fast:
	@poetry run scripts/create-report.sh --results_per_page=1000
git-push: create-requirements-file lint
	@poetry run scripts/git-push.sh
clear-reports:
	@rm -rf reports/*.csv reports/*.json
docker-build: create-requirements-file
	@docker build -t comprocard-scraping:latest .
docker-run: docker-build
	@docker run -it --rm -v "./reports:/app/reports" comprocard-scraping:latest "$${ARGS}"
create-requirements-file:
	@poetry export -q -o requirements.txt
