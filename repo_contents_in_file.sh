#!/bin/bash

# Assign arguments to variables
REPO_PATH=./Downloads/DeepFaceLab
OUTPUT_FILE=./repo_viz/repo_code_text.txt

# List of meaningful file extensions
extensions=("*.py" "*.js" "*.html" "*.css" "*.java" "*.rb" "*.sh" "*.ts" "*.go" "*.php" "*.c" "*.cpp" "*.h" "*.json" "*.xml" "*.md")

# Check if the specified repository directory exists
if [ ! -d "$REPO_PATH" ]; then
    echo "The specified repository directory does not exist: $REPO_PATH"
    exit 1
fi

# Create the output directory if it doesn't exist
OUTPUT_DIR=$(dirname "$OUTPUT_FILE")
if [ ! -d "$OUTPUT_DIR" ]; then
    echo "The output directory does not exist, creating: $OUTPUT_DIR"
    mkdir -p "$OUTPUT_DIR"
fi

# Clear the output file if it exists or create a new one
> "$OUTPUT_FILE"

# Find files in the repository path with meaningful extensions and consolidate them
for ext in "${extensions[@]}"; do
    find "$REPO_PATH" -type f -name "$ext" | while read -r file; do
        # Get the relative file path by removing the REPO_PATH from the full file path
        relative_file_path="${file#$REPO_PATH/}"

        # Add the relative file path as a comment in the consolidated file
        echo "### File: $relative_file_path ###" >> "$OUTPUT_FILE"

        # Append the contents of each file to the output file
        cat "$file" >> "$OUTPUT_FILE"

        # Add a newline between files for readability
        echo -e "\n\n" >> "$OUTPUT_FILE"
    done
done

# Print success message
echo "Files with meaningful extensions have been consolidated into: $OUTPUT_FILE"