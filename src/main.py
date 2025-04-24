# --- START OF FILE main.py ---

import os
import shutil
# Import necessary functions from your module
from htmlnode import (
    copy_directory_recursive,
    generate_pages_recursive # Import the new function
)

def main():
    # Define source and destination directories
    static_dir = "static"
    content_dir = "content"
    public_dir = "public"
    template_path = "template.html"

    print("--- Static Site Generation ---")

    # 1. Clean the public directory
    if os.path.exists(public_dir):
        print(f"Deleting existing directory: '{public_dir}'")
        shutil.rmtree(public_dir)
    # It's good practice to recreate the top-level public dir immediately
    # Although generate_page creates subdirs, this ensures the base exists.
    print(f"Creating public directory: '{public_dir}'")
    os.mkdir(public_dir)

    # 2. Copy static assets to public directory
    print(f"\nCopying static assets from '{static_dir}' to '{public_dir}'...")
    if os.path.exists(static_dir):
        copy_directory_recursive(static_dir, public_dir)
        print("Static assets copied successfully.")
    else:
        print(f"Warning: Static directory '{static_dir}' not found. Skipping copy.")


    # 3. Generate content pages recursively
    print("\nGenerating content pages...")
    # Check if source content dir and template exist before generating
    if not os.path.exists(content_dir):
         print(f"Error: Content directory '{content_dir}' not found.")
    elif not os.path.exists(template_path):
        print(f"Error: Template file '{template_path}' not found.")
    else:
        try:
            generate_pages_recursive(content_dir, template_path, public_dir)
            print("\nContent generation complete.")
        except Exception as e:
            # Catch errors during the recursive generation
            print(f"\nError during recursive page generation: {e}")


    print("\n--- Static Site Generation Complete ---")

# Make sure main() is called when the script runs
if __name__ == "__main__":
    main()

# --- END OF FILE main.py ---