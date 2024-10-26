from glob import glob

import config
from selected_words_counter import extract_files

extract_files.extracted_files_from_list_filepaths(
    [afilepath for afilepath in glob(config.local_folder_mount_point + "/*")]
)
