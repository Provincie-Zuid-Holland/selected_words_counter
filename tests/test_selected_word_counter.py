import os
import shutil
from glob import glob

import config
import pandas as pd
from selected_words_counter import (
    SelectedWordCounter,
    counting,
    extract_files,
    functions,
)

# Reference testing varialbes.
test_dir = "./test_data/"
test_dir_converted = "./test_data_converted/"
test_dir_output ="./test_output"

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
    extract_files.run(test_dir, test_dir_converted)

    found_file_paths = [afilepath for afilepath in glob(test_dir_converted + "/*.txt")]

    assert (
        len(found_file_paths) >= 10
    ), "Expected at least 10 files in test_dir_converted"

    # Check pdf's have been converted.
    assert len(open(glob(test_dir_converted + "/*_pdf.txt")[0], "r").read()) > 0
    # Check if pptx files have been converted.
    assert len(open(glob(test_dir_converted + "/*_pptx.txt")[0], "r").read()) > 0
    # Check if docx files have been converted
    assert len(open(glob(test_dir_converted + "/*_docx.txt")[0], "r").read()) > 0
    # Check if doc files have been converted
    # TODO: it's hard to generate .doc files in python because of deprecated libraries, more effort needs to done to also generate these files.
    # assert len(open(glob(test_dir_converted + "/*_doc.text")[0], "r").read()) > 0
    # TODO: it's hard to generate .xls files in python because of deprecated libraries, more effort needs to done to also generate these files.
    # assert len(open(glob(test_dir_converted + "/*_xls.text")[0], "r").read()) > 0
    # Check if xlsx files have been converted
    assert len(open(glob(test_dir_converted + "/*_xlsx.txt")[0], "r").read()) > 0

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
                            test_dir_converted
                            # Replace directory slashes with # to make one file name while still knowing the original directory
                            + f"/{replace_last_slash(afilepath, replacement="#").split("/")[-1].split(".")[0]}*.txt"
                        )
                    )
                    >= 1
                ), "Expected a file in a directory to be found as with a # in it's name denoting the directory in the converted map"

    shutil.rmtree(test_dir_converted)

def test_count_files():

    aword_list_test = ["fireplace","dreams", "hybrid", "technological", "collapse", "netherlands"]

    result_output = SelectedWordCounter(aword_list_test, test_dir, test_dir_converted, False, test_dir_output).run()

    # Check if there is output
    assert len(glob(test_dir_output+"/*")) >= 1

    # Check the contents of the file
    df = pd.read_excel(result_output+".xlsx")

    # Dictionary to store expected word counts per file format
    expected_counts = {
        "coated pendant hunter allowing can margin.docx": {"fireplace": 2, "dreams": 1},
        "copyright endless dumb bandwidth trading define.xlsx": {"hybrid": 1, "technological": 1},
        "alter strip lucy z cemetery kinds.pdf": {"collapse": 1, "netherlands": 1},
    }

    # Loop through each file format and check counts
    for filepath, words in expected_counts.items():
        test_file = df[df["Filepath"] == filepath]
        for word, count in words.items():
            assert test_file[word].values[0] == count, f"{filepath} should contain {word} {count} times"


    os.remove(result_output+".xlsx")
    