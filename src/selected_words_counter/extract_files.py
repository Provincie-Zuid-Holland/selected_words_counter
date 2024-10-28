import os
import re
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from glob import glob

import extract_msg
from tqdm import tqdm

import config
from selected_words_counter.functions import process_file


def process_and_save_file(afilepath, verbose=False):
    if verbose:
        print("-------")
        print(afilepath)
    afilepath = afilepath.replace("\\", "/")

    try:
        text_content = process_file(afilepath)

        a_output_name = (
            config.local_folder_mount_point_extracted
            + "/"
            + re.sub(
                r"\.(?!.*\.)",
                "_",
                afilepath.replace(config.local_folder_mount_point, "").replace(
                    "/", "#"
                ),
            )
            + ".txt"
        )
        if verbose:
            print(a_output_name)
        with open(a_output_name, "w") as file:
            file.write(str(text_content))

    except Exception as e:
        print(f"Error processing {afilepath}: {e}")


def extract_msg_attachments():
    # Extract all .msg files into a directory
    for afilepath in glob(config.local_folder_mount_point + "*.msg"):
        afilepath = afilepath.replace("\\", "/")
        try:
            msg = extract_msg.Message(afilepath)

            if len(msg.attachments) > 0:
                a_output_directory = afilepath.rsplit(".", 1)[0]
                print("Making :" + str(a_output_directory))
                os.makedirs(a_output_directory)

                for item in range(0, len(msg.attachments)):
                    att = msg.attachments[item]
                    msg.attachments[item].save(
                        customPath=a_output_directory, customFilename=att.longFilename
                    )
        except Exception as e:
            print(e)


def extract_zip_attachments():
    # Extract a zip file into a new directory

    for afilepath in glob(config.local_folder_mount_point + "*.zip"):
        try:
            afilepath = afilepath.replace("\\", "/")
            print(afilepath)
            a_output_directory = str(afilepath.rsplit(".", 1)[0])
            print("Making directory to save files in:" + a_output_directory)
            os.makedirs(a_output_directory)

            # Extract the contents of the zip file
            with zipfile.ZipFile(afilepath, "r") as zip_ref:
                zip_ref.extractall(a_output_directory)
        except Exception as e:
            print(e)


def extracted_files_from_list_filepaths(afilepaths, verbose=False):
    with ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(process_and_save_file, afilepath, verbose): afilepath
            for afilepath in afilepaths
        }
        for future in tqdm(as_completed(futures), total=len(futures)):
            try:
                future.result()
            except Exception as e:
                print(f"Exception occurred: {e}")


def run():
    # First extract all the .msg files.
    print("Extracting .msg files")
    extract_msg_attachments()
    # Then extract all the .zip files.
    print("Extracting .zip files")
    extract_zip_attachments()

    if os.path.isdir(config.local_folder_mount_point_extracted) == False:
        os.makedirs(config.local_folder_mount_point_extracted)

    extracted_files_from_list_filepaths(
        [
            afilepath
            for afilepath in glob(
                os.path.join(config.local_folder_mount_point, "**", "*"), recursive=True
            )
        ]
    )
