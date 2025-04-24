# --- START OF FILE main.py ---

import os
import sys # Import sys module
import shutil
# Import necessary functions from your module
from htmlnode import (
    copy_directory_recursive,
    generate_pages_recursive
)

def main():
    # --- Base Path Handling ---
    base_path = "/" # Default for local testing
    if len(sys.argv) > 1:
        # Use the first argument from the command line if provided
        base_path = sys.argv[1]
        # Ensure it starts and ends with a slash for consistency
        if not base_path.startswith("/"):
            base_path = "/" + base_path
        if not base_path.endswith("/"):
            base_path += "/"
    print(f"Using base path: {base_path}")
    # --- / Base Path Handling ---

    # Define source and destination directories
    static_dir = "static"
    content_dir = "content"
    docs_dir = "docs" # Changed destination directory name
    template_path = "template.html"

    print("--- Static Site Generation ---")

    # 1. Clean the destination directory
    if os.path.exists(docs_dir):
        print(f"Deleting existing directory: '{docs_dir}'")
        shutil.rmtree(docs_dir)
    print(f"Creating destination directory: '{docs_dir}'")
    os.mkdir(docs_dir)

    # 2. Copy static assets to destination directory
    print(f"\nCopying static assets from '{static_dir}' to '{docs_dir}'...")
    if os.path.exists(static_dir):
        # Pass docs_dir as the destination
        copy_directory_recursive(static_dir, docs_dir)
        print("Static assets copied successfully.")
    else:
        print(f"Warning: Static directory '{static_dir}' not found. Skipping copy.")


    # 3. Generate content pages recursively
    print("\nGenerating content pages...")
    if not os.path.exists(content_dir):
         print(f"Error: Content directory '{content_dir}' not found.")
    elif not os.path.exists(template_path):
        print(f"Error: Template file '{template_path}' not found.")
    else:
        try:
            # Pass base_path and docs_dir to the generator
            generate_pages_recursive(content_dir, template_path, docs_dir, base_path)
            print("\nContent generation complete.")
        except Exception as e:
            print(f"\nError during recursive page generation: {e}")


    print("\n--- Static Site Generation Complete ---")

# Make sure main() is called when the script runs
if __name__ == "__main__":
    main()

# --- END OF FILE main.py ---