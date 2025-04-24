#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "--- Running Production Build ---"

# Replace YourRepoName with the actual name of your GitHub repository
REPO_NAME="https://github.com/olereon/StaticWeb" # <<< CHANGE THIS TO YOUR REPO NAME

# Run the main script, passing the base path as an argument
# Ensure the base path starts and ends with a slash
python3 src/main.py "/${REPO_NAME}/"

echo "--- Build Complete ---"
echo "Generated site placed in 'docs' directory."