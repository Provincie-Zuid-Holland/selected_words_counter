import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from glob import glob

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
    if os.path.isdir(config.local_folder_mount_point_extracted) == False:
        os.makedirs(config.local_folder_mount_point_extracted)

    extracted_files_from_list_filepaths(
        [afilepath for afilepath in glob(config.local_folder_mount_point + "/*")]
    )
