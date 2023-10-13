#!/bin/bash

EXCLUDED=("vendor/*" ".venv/*" ".vscode/*" "vendor.zip" ".git/*" "*.pyc" "*__pycache__*")
OUTPUT="/mnt/c/Users/souam/Documents/Data Engineering/flights-metrics/."
# Cleanup
rm package.zip

# Create zip file
zip -r package.zip . -x "${EXCLUDED[@]}"

# Copy to windows drive
cp package.zip "${OUTPUT}"
