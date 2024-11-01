import os
import re
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from glob import glob

import extract_msg
from tqdm import tqdm

from selected_words_counter.functions import process_file

"""

This file is used to store code for extracting text from different file formats.

@author: Michael de Winter
"""

def process_and_save_file(
    afilepath,
    alocal_folder_mount_point,
    alocal_folder_mount_point_extracted,
    verbose=False,
):
    """

    Method to call process_file and correctly generate a filename if it contains subdirectories.

    @param afilepath: Path to a specific file.
    @param alocal_folder_mount_point: the original directory of the file is stripped from the filename for naming purposes to get it's subdirectory.
    @oaram alocal_folder_mount_point_extracted: directory in which the file will be stored.
    """

    if verbose:
        print("-------")
        print(afilepath)
    afilepath = afilepath.replace("\\", "/")

    try:
        text_content = process_file(afilepath)
        
        # Generate a output name but if there are subdirectories in the directory put the subdirectories name in the filename.
        a_output_name = (
            alocal_folder_mount_point_extracted
            + "/"
            + re.sub(
                r"\.(?!.*\.)",
                "_",
                afilepath.replace(alocal_folder_mount_point, "").replace("/", "#"),
            )
            + ".txt"
        )
        if verbose:
            print(a_output_name)
        with open(a_output_name, "w") as file:
            file.write(str(text_content))

    except Exception as e:
        print(f"Error processing {afilepath}: {e}")


def extract_msg_attachments(alocal_folder_mount_point):
    """
    
    Extract all .msg files in a directory.

    @param alocal_folder_mount_point: directory where the .msg files are stored.
    """
    # Extract all .msg files into a directory
    for afilepath in glob(alocal_folder_mount_point + "*.msg"):
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


def extract_zip_attachments(alocal_folder_mount_point):
    """
    
    Extract all .zip files in a directory.
    
    @param alocal_folder_mount_point: directory where the .zip files are stored.
    """
    # Extract a zip file into a new directory

    for afilepath in glob(alocal_folder_mount_point + "*.zip"):
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


def extracted_files_from_list_filepaths(
    afilepaths,
    alocal_folder_mount_point,
    alocal_folder_mount_point_extracted,
    verbose=False,
    threads = False
):
    """

    Method to extract all files in directory in a .txt format in a other directory for easy searching and snapshotting.

    @param afilepaths: a array of filepaths to be extracted to .txt files.
    @param alocal_folder_mount_point: the original directory of the file is stripped from the filename for naming purposes to get it's subdirectory.
    @oaram alocal_folder_mount_point_extracted: directory in which the file will be stored.
    @param verbose: Wether to print more output.
    @param threads: Wether to multiprocess with the file reading thus speeding up the process but not all systems can handle it. 
    """
    if threads:
        with ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(
                    process_and_save_file,
                    afilepath,
                    alocal_folder_mount_point,
                    alocal_folder_mount_point_extracted,
                    verbose,
                ): afilepath
                for afilepath in afilepaths
            }
            for future in tqdm(as_completed(futures), total=len(futures)):
                try:
                    future.result()
                except Exception as e:
                    print(f"Exception occurred: {e}")
    else:
        [process_and_save_file(afilepath,alocal_folder_mount_point, alocal_folder_mount_point_extracted,verbose ) for afilepath in afilepaths]


def run(alocal_folder_mount_point, alocal_folder_mount_point_extracted, amulti_thread = False):
    """
    Method to run the process.

    @param alocal_folder_mount_point: the original directory of the file is stripped from the filename for naming purposes to get it's subdirectory.
    @oaram alocal_folder_mount_point_extracted: directory in which the file will be stored.
    @param amulti_thread: Wether to multiprocess with the file reading thus speeding up the process but not all systems can handle it. 
    """
    # First extract all the .msg files.
    print("Extracting .msg files")
    extract_msg_attachments(alocal_folder_mount_point)
    # Then extract all the .zip files.
    print("Extracting .zip files")
    extract_zip_attachments(alocal_folder_mount_point)

    # Make a directory if the directory does not exist yet.
    if os.path.isdir(alocal_folder_mount_point_extracted) == False:
        os.makedirs(alocal_folder_mount_point_extracted)

    extracted_files_from_list_filepaths(
        [
            afilepath
            for afilepath in glob(
                os.path.join(alocal_folder_mount_point, "**", "*"), recursive=True
            )
        ],
        alocal_folder_mount_point,
        alocal_folder_mount_point_extracted,
        threads=amulti_thread
    )
