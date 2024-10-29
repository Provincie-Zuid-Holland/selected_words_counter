import os
from glob import glob

import config
from selected_words_counter import counting, extract_files, functions


class SelectedWordCounter:
    def __init__(
        self,
        aword_list,
        local_folder_mount_point,
        local_folder_mount_point_extracted,
        keep_extracted,
        output_dir,
        extract=True,
        keep_extract=True,
        version=1,
        output_extension=".xlsx",
    ):
        # Lower case all words for easier matching.
        self.aword_list = [aword.lower().replace(".", "") for aword in aword_list]
        self.local_folder_mount_point = local_folder_mount_point
        self.local_folder_mount_point_extracted = local_folder_mount_point_extracted
        self.keep_extracted = keep_extracted
        self.output_dir = output_dir

        self.extract = extract
        self.keep_extract = keep_extract
        self.version = version
        self.output_extension = output_extension

    def run(self):
        if self.extract:
            if os.path.isdir(self.local_folder_mount_point_extracted) == False or len(
                glob(self.local_folder_mount_point_extracted + "*")
            ) < len(glob(self.local_folder_mount_point + "*")):
                print("Extracting data:")
                extract_files.run(
                    self.local_folder_mount_point,
                    self.local_folder_mount_point_extracted,
                )

        print("Finding words:")
        df = counting.word_counting_in_files(
            config.aword_list,
            [
                afilepath.replace("\\", "/")
                for afilepath in glob(
                    os.path.join(
                        self.local_folder_mount_point_extracted, "**", "*.txt"
                    ),
                    recursive=True,
                )
            ],
        )

        filename_output = functions.generate_filename(self.output_dir, self.version)

        if self.output_extension == ".xlsx":
            df.to_excel(filename_output + ".xlsx", index=False)

        elif self.output_extension == ".csv":
            df.to_csv(filename_output + ".csv", index=False)

        print(f"Output found at {filename_output}")

        if config.keep_extracted == False:
            functions.delete_directory(config.local_folder_mount_point_extracted)
