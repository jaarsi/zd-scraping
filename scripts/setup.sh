#!/bin/sh -ex
poetry lock
poetry install
poetry run pre-commit install