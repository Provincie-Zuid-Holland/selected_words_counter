import os
from glob import glob

from selected_words_counter import counting, extract_files


class SelectedWordCounter:
    """

    A selected word counter class

    @param aword_list: a array with words to be counted in the files in the selected directory.
    @param target_dir: Path to a directory where all the files are stored which have to be searched
    @param target_dir_extracted: Files are being extracted to a .txt format for easier reading, this denotes the directory where these converted files will be stored.
    @param output_dir: Directory in which the resulting excel file will be stored.
    @param extract: Whether to extract the files for a .txt format, only set this to FALSE if the files already have been extracted!
    @param keep_extract: Whether to keep the extracted .txt files or delete the folder. If multiple searches need to be done extraction does not need to be redone.
    @param output_extension: What the resulting file format needs to be, defaults to a excel,
    @param multi_thread: Whether to read in files multithreaded, speeds up file conversion to .txt. But can not be used on all systems.

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
        output_extension=".xlsx",
        multi_thread=False,
    ):
        # Lower case all words for easier matching.
        self.aword_list = aword_list
        self.target_dir = target_dir
        self.target_dir_extracted = target_dir_extracted
        self.output_dir = output_dir

        self.extract = extract
        self.keep_extract = keep_extract
        self.output_extension = output_extension
        self.multi_thread = multi_thread

    def run(self):
        # Check if files have to be extracted can optionally be check if files have already been extracted.
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

        list_of_files_to_be_searched = [
            afilepath.replace("\\", "/")
            for afilepath in glob(
                os.path.join(self.target_dir_extracted, "**", "*.txt"), recursive=True
            )
        ]
        print("Finding words:")
        df = counting.word_counting_in_files(
            self.aword_list, list_of_files_to_be_searched
        )

        filename_output = extract_files.generate_filename(self.output_dir)

        if self.output_extension == ".xlsx":
            df.to_excel(filename_output + ".xlsx", index=False)

        elif self.output_extension == ".csv":
            df.to_csv(filename_output + ".csv", index=False)

        print(f"Output found at {filename_output}")

        if self.keep_extract == False:
            extract_files.delete_directory(self.target_dir_extracted)

        return filename_output
