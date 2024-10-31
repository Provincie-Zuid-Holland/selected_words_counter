import re

import pandas as pd
from tqdm import tqdm

"""
This file is used for code which handles the counting of the word in .txt files.

@author: Michael de Winter
"""

def replace_underscore_with_period(ainput_string):
    """
    Replace the last underscore with a period in the file name because of the conversion to .txt

    @param ainput_string: a string from which the last underscore needs to be replaced.
    """
    return re.sub("_(?!.*_)", ".", ainput_string)


def word_counting_in_files(aword_list, afilepaths, exact_match=False):
    """
    
    Main code for counting words in files. 
    2 options available for this either partial matching or exact matching.

    Performance seems to be better with partial matching.

    @oaram aword_list: Words to be searched and counted for.
    @param afilepaths: File paths of files.
    @param exact_match: Wether to do partial matching or exact matching.
    """
    word_counts = []

    #Double check to lower all word
    aword_list = [aword.lower() for aword in aword_list]

    #Loop through each file in the directory
    for filepath in tqdm(afilepaths):
        try:
            # Read the contents of the file
            with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
                text = file.read().lower()
                if exact_match:
                    # Note: Using regex for exact match, although it may slow down performance.
                    counts = [
                        sum(1 for _ in re.finditer(r"\b%s\b" % re.escape(word), text)) 
                        for word in aword_list
                    ]
                else:
                    counts = [text.count(word) for word in aword_list]

                # Append filename and counts as a list (or tuple)
                word_counts.append([filepath] + counts)
        except Exception as e:
            print(e)

    # Convert the list to a pandas DataFrame
    df = pd.DataFrame(word_counts, columns=["Filepath"] + aword_list)

    # TODO: make this split more efficient for now this column is only for debugging.
    df["Filepath_extracted"] = df["Filepath"]
    df["Filepath"] = df["Filepath"].str.split("/").str[-1]
    df["Filepath"] = df["Filepath"].str.split(".txt").str[0]
    df["Filepath"] = df["Filepath"].apply(replace_underscore_with_period)
    df["ID"] = df["Filepath"].str.split("-").str[0]

    return df
