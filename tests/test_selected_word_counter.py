import os
import shutil
from glob import glob

import pandas as pd

import config
from selected_words_counter import extract_files
from selected_words_counter.selected_words_counter import SelectedWordCounter

# Reference testing varialbes.
test_dir = "./test_data/"
test_dir_nl = "./test_data_nl/"
test_dir_converted = "./test_data_converted/"
test_dir_converted_test = "./test_data_converted_test/"
test_dir_output = "./test_output"


def test_unzipping():
    extract_files.extract_zip_attachments(test_dir)

    # Check if at least there is one file in the directory
    for item in os.listdir(test_dir):
        item_path = os.path.join(test_dir, item)
        # Check if the item is a directory
        if os.path.isdir(item_path):
            # Test if there are files and that they contain the name of the zip folder in them
            try:
                assert len([afilepath for afilepath in glob(item_path + "/*")]) >= 1
            finally:
                shutil.rmtree(item_path)


def test_msg_extraction():
    # TODO: No valid test data for this, still needs be made
    assert 0 == 0


def test_extract_files_run():
    extract_files.run(test_dir, test_dir_converted)

    try:
        found_file_paths = [
            afilepath for afilepath in glob(test_dir_converted + "/*.txt")
        ]

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
                                + f"/{extract_files.replace_last_slash(afilepath, replacement="#").split("/")[-1].split(".")[0]}*.txt"
                            )
                        )
                        >= 1
                    ), "Expected a file in a directory to be found as with a # in it's name denoting the directory in the converted map"
    finally:
        shutil.rmtree(test_dir_converted)

        for item in os.listdir(test_dir):
            item_path = os.path.join(test_dir, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)


def test_count_files():
    try:
        aword_list_test = [
            "fireplace",
            "dreams",
            "hybrid",
            "technological",
            "collapse",
            "netherlands",
            "fuji",
        ]

        result_output = SelectedWordCounter(
            aword_list_test,
            test_dir,
            test_dir_converted,
            test_dir_output,
            keep_extract=False,
        ).run()

        # Check if there is output
        assert len(glob(test_dir_output + "/*")) >= 1

        # Check the contents of the file
        df = pd.read_excel(result_output + ".xlsx")

        # Dictionary to store expected word counts per file format
        expected_counts = {
            "coated pendant hunter allowing can margin.docx": {
                "fireplace": 2,
                "dreams": 1,
            },
            "copyright endless dumb bandwidth trading define.xlsx": {
                "hybrid": 1,
                "technological": 1,
            },
            "alter strip lucy z cemetery kinds.pdf": {"collapse": 1, "netherlands": 1},
            "companies continuing politics tex parcel glass.msg": {"fuji": 1},
        }

        # Loop through each file format and check counts
        for filepath, words in expected_counts.items():
            test_file = df[df["Filepath"] == filepath]
            for word, count in words.items():
                assert (
                    test_file[word].values[0] == count
                ), f"{filepath} should contain {word} {count} times"
    finally:
        os.remove(result_output + ".xlsx")

        for item in os.listdir(test_dir):
            item_path = os.path.join(test_dir, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)


def test_no_extract():
    try:
        aword_list_test = [
            "floppy",
            "banana",
            "cingular",
            "cheat",
            "companion",
            "satisfaction",
            "fuji",
        ]

        result_output = SelectedWordCounter(
            aword_list_test,
            test_dir,
            test_dir_converted_test,
            test_dir_output,
            extract=False,
        ).run()

        # Check if there is output
        assert len(glob(test_dir_output + "/*")) >= 1

        # Check the contents of the file
        df = pd.read_excel(result_output + ".xlsx")

        # Dictionary to store expected word counts per file format
        expected_counts = {
            "arabia registry regardless under four directions.docx": {
                "floppy": 1,
                "banana": 1,
            },
            "balance session rest wholesale pins timothy.docx": {
                "cingular": 1,
                "cheat": 1,
            },
            "ban handle monte gba spreading nine.pdf": {
                "companion": 1,
                "satisfaction": 1,
            },
        }

        # Loop through each file format and check counts
        for filepath, words in expected_counts.items():
            test_file = df[df["Filepath"] == filepath]
            for word, count in words.items():
                assert (
                    test_file[word].values[0] == count
                ), f"{filepath} should contain {word} {count} times"
    finally:
        os.remove(result_output + ".xlsx")
        for item in os.listdir(test_dir):
            item_path = os.path.join(test_dir, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)


def test_count_files_nl():
    try:
        aword_list_test = [
            "relaties",
            "familiebanden",
            "communiceren",
            "filmpjes",
            "geschiedenis",
            "nederland",
            "smits",
            "verblijfkosten",
            "cruijff",
            "halsema",
            "ministerie van justitie en veiligheid",
            "ifzo",
            "rvdk",
        ]

        result_output = SelectedWordCounter(
            aword_list_test,
            test_dir_nl,
            test_dir_converted,
            test_dir_output,
            keep_extract=False,
        ).run()

        # Check if there is output
        assert len(glob(test_dir_output + "/*")) >= 1

        # Check the contents of the file
        df = pd.read_excel(result_output + ".xlsx")

        # Dictionary to store expected word counts per file format
        expected_counts = {
            "analyse_analyse_20241109_191154.docx": {
                "relaties": 4,
                "familiebanden": 2,
            },
            "onderzoek_beschrijving_20241109_165724.pptx": {
                "communiceren": 2,
                "filmpjes": 1,
            },
            "gmb-2024-469908.pdf": {
                "smits": 1,
                "verblijfkosten": 6,
            },
            "gmb-2024-471945.pdf": {"cruijff": 6, "halsema": 1},
            "blg-1159474.pdf": {
                "ministerie van justitie en veiligheid": 18,
                "ifzo": 449,
            },
            "blg-1161086.pdf": {
                "ministerie van justitie en veiligheid": 12,
                "rvdk": 13,
            },
        }

        # Loop through each file format and check counts
        for filepath, words in expected_counts.items():
            test_file = df[df["Filepath"] == filepath]
            for word, count in words.items():
                assert (
                    test_file[word].values[0] == count
                ), f"{filepath} should contain {word} {count} times"
    finally:
        os.remove(result_output + ".xlsx")

        for item in os.listdir(test_dir_nl):
            item_path = os.path.join(test_dir_nl, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
