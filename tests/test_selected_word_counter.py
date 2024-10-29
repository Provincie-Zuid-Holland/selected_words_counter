import os
import shutil
from glob import glob

import config
from selected_words_counter import (
    SelectedWordCounter,
    counting,
    extract_files,
    functions,
)

# Reference testing varialbes.
test_dir = "./test_data/"
text_dir_converted = "./test_data_converted/"


def replace_last_slash(path, replacement=""):
    parts = path.rsplit("/", 1)
    return replacement.join(parts)


def test_unzipping():
    extract_files.extract_zip_attachments(test_dir)

    # Check if at least there is one file in the directory
    for item in os.listdir(test_dir):
        item_path = os.path.join(test_dir, item)
        # Check if the item is a directory
        if os.path.isdir(item_path):
            # Test if there are files and that they contain the name of the zip folder in them
            assert len([afilepath for afilepath in glob(item_path + "/*")]) >= 1
            shutil.rmtree(item_path)


def test_msg_extraction():
    # TODO: No valid test data for this, still needs be made
    assert 0 == 0


def test_extract_files_run():
    extract_files.run(test_dir, text_dir_converted)

    found_file_paths = [afilepath for afilepath in glob(text_dir_converted + "/*.txt")]

    assert (
        len(found_file_paths) >= 10
    ), "Expected at least 10 files in text_dir_converted"

    # Assert if files from directories made it in the convert folder
    for item in os.listdir(test_dir):
        item_path = os.path.join(test_dir, item)
        # Check if the item is a directory
        if os.path.isdir(item_path):
            for afilepath in glob(item_path + "/*"):
                afilepath = afilepath.replace("\\", "/")
                assert (
                    len(
                        glob(
                            text_dir_converted
                            # Replace directory slashes with # to make one file name while still knowing the original directory
                            + f"/{replace_last_slash(afilepath, replacement="#").split("/")[-1].split(".")[0]}*.txt"
                        )
                    )
                    >= 1
                ), "Expected a file in a directory to be found as with a # in it's name denoting the directory in the converted map"

    assert (
        len(open(found_file_paths[0], "r").read()) > 0
    ), "ensure at least some words in the document"

    shutil.rmtree(text_dir_converted)
