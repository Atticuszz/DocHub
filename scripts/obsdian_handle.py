"""
-*- coding: utf-8 -*-
@Organization : SupaVision
@Author       : 18317
@Date Created : 29/12/2023
@Description  :
"""
import logging
from pathlib import Path
import zipfile

from scripts.logs.config import setup_logging


def zip_directory(folder_path, output_path):
    folder_path = Path(folder_path)
    output_path = Path(output_path)

    # Ensure the output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Create a ZipFile object
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through the directory
        for file in folder_path.rglob('*'):
            if file.is_file():  # Make sure to only add files
                # Create a relative path for files to keep the directory structure
                zipf.write(file, file.relative_to(folder_path))
    logging.info(f"Created zip file at: {output_path}")

root_path = Path(__file__).parents[1]

# Specify the directory you want to zip
directory_to_zip = root_path /'.obsidian'  # Change to your specific folder path

# Specify the output zip file path
output_zip_file = root_path / "assets/obsidian.zip"  # Change to your desired output path



if __name__ == "__main__":
    setup_logging()
    # Call the function
    zip_directory(directory_to_zip, output_zip_file)
