#!/bin/bash

pytest -v
ruff format .
ruff check --fix