import datetime
from datetime import datetime
from glob import glob

import config
from selected_words_counter import counting

version = 3


def generate_filename(version):
    current_date = datetime.now().strftime("%Y-%m-%d")  # Format as YYYY-MM-DD
    filename = f"./output/selected_word_counter_{current_date}_v{version}.xlsx"
    return filename


df = counting.word_counting_in_files(
    config.aword_list,
    [
        afilepath
        for afilepath in glob(config.local_folder_mount_point_extracted + "/*.txt")
    ],
)

df.to_excel(generate_filename(version), index=False)
