import os

import config
from selected_words_counter import (
    SelectedWordCounter,
    counting,
    extract_files,
    functions,
)

# Reference testing varialbes.


def test_unzipping():
    extract_files.extract_zip_attachments()
    directory = (
        config.local_folder_mount_point
        + "/mega forth scripts sheriff placement continuity"
    )
    assert os.path.isdir(directory)
