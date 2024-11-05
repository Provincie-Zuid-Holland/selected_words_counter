import os
from glob import glob

from selected_words_counter import counting, extract_files, functions


class SelectedWordCounter:
    """

    A selected word counter class

    @param aword_list: a array with words to be counted in the files in the selected directory.
    @param target_dir: Path to a directory where all the files are stored which have to be searched
    @param target_dir_extracted: Files are being extracted to a .txt format for easier reading, this denoutes the directory where these converted files will be stored.
    @param output_dir: Directory in which the resulting excel file will be stored.
    @param extract: Wether to extract the files for a .txt format, only set this to FALSE if the files already have been extracted!
    @pparam keep_extract: Wether to keep the extracted .txt files or delete the folder. If multiple searches need to be done extraction does not need to be redone.
    @param version: This is used in the final filename.
    @param output_extension: What the resulting file format needs to be, defaults to a excel,
    @param multi_thread: Wether to read in files multithreaded, speeds up file conversion to .txt. But can not be used on all systems.

    @Author: Michael de Winter
    """

    def __init__(
        self,
        aword_list,
        target_dir,
        target_dir_extracted,
        output_dir,
        extract=True,
        keep_extract=True,
        version=1,
        output_extension=".xlsx",
        multi_thread=False,
    ):
        # Lower case all words for easier matching.
        self.aword_list = [aword.lower().replace(".", "") for aword in aword_list]
        self.target_dir = target_dir
        self.target_dir_extracted = target_dir_extracted
        self.output_dir = output_dir

        self.extract = extract
        self.keep_extract = keep_extract
        self.version = version
        self.output_extension = output_extension
        self.multi_thread = multi_thread

    def run(self):
        if self.extract:
            if os.path.isdir(self.target_dir_extracted) == False or len(
                glob(self.target_dir_extracted + "*")
            ) < len(glob(self.target_dir + "*")):
                print("Extracting data:")
                extract_files.run(
                    self.target_dir,
                    self.target_dir_extracted,
                    self.multi_thread,
                )

        print("Finding words:")
        df = counting.word_counting_in_files(
            self.aword_list,
            [
                afilepath.replace("\\", "/")
                for afilepath in glob(
                    os.path.join(self.target_dir_extracted, "**", "*.txt"),
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

        if self.keep_extract == False:
            functions.delete_directory(self.target_dir_extracted)

        return filename_output
        return filename_output
