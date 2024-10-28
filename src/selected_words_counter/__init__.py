import os
from glob import glob

import config
from selected_words_counter import counting, extract_files, functions


class SelectedWordCounter:
    def __init__(self, version=1, extract=True, output_extension=".xlsx", awordlist =False, local_folder_mount_point = False, keep_extracted = False, output_dir= False):
        self.extract = extract
        self.version = version
        self.output_extension = output_extension

        #Overwrite config settings if arguments are given.
        if aword_list:
            # Lower case all words for easier matching.
            aword_list = [aword.lower().replace(".", "") for aword in aword_list]
            config.aword_list = aword_list
        if local_folder_mount_point:
            config.local_folder_mount_point = local_folder_mount_point
        if keep_extracted:
            config.keep_extracted = keep_extracted
        if output_dir:
            config.output_dir = output_dir

    def run(self):
        if self.extract:
            if os.path.isdir(config.local_folder_mount_point_extracted) == False or len(
                glob(config.local_folder_mount_point_extracted + "*")
            ) < len(glob(config.local_folder_mount_point + "*")):
                print("Extracting data:")
                extract_files.run()

        print("Finding words:")
        df = counting.word_counting_in_files(
            config.aword_list,
            [
                afilepath.replace("\\", "/")
                for afilepath in glob(
                    os.path.join(
                        config.local_folder_mount_point_extracted, "**", "*.txt"
                    ),
                    recursive=True,
                )
            ],
        )

        filename_output = functions.generate_filename(self.version)

        if self.output_extension == ".xlsx":
            df.to_excel(filename_output + ".xlsx", index=False)

        elif self.output_extension == ".csv":
            df.to_csv(filename_output + ".csv", index=False)

        print(f"Output found at {functions.generate_filename(self.version)}")

        if config.keep_extracted == False:
            functions.delete_directory(config.local_folder_mount_point_extracted)
