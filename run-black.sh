#!/bin/bash

echo ""
echo "Running black..."
black --target-version py37 --diff fastavro/ tests/ setup.py
black --target-version py37 --check fastavro/ tests/ setup.py

