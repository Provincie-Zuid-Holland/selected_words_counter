import re

import pandas as pd
from tqdm import tqdm


def replace_underscore_with_period(ainput_string):
    # Replace the last underscore with a period in the file name because of the conversion to .txt
    return re.sub("_(?!.*_)", ".", ainput_string)


def word_finding_in_files(aword_list, afilepaths, exact_match=False):
    word_counts = []

    # dubble check to lower all word
    aword_list = [aword.lower() for aword in aword_list]

    # Loop through each file in the directory
    for filepath in tqdm(afilepaths):
        # Read the contents of the file
        with open(filepath, "r", encoding="utf-8") as file:
            if exact_match:
                text = (
                    file.read().lower().split()
                )  # Splitting for exact match, slow down performance though
            else:
                text = file.read().lower()

            # Create a dictionary to store the count for each word in this file
            counts = [
                # TODO: Strangely on stackoverflow it says that re are faster yet with internal testing it is not!
                # sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(word), text)) for word in aword_list
                text.count(aword)
                for aword in aword_list
            ]
            # Append filename and counts as a list (or tuple)
            word_counts.append([filepath] + counts)

    # Convert the list to a pandas DataFrame
    df = pd.DataFrame(word_counts, columns=["Bestandsnaam"] + aword_list)

    # TODO: make this split more efficient for now this column is only for debugging.
    df["Path"] = df["Bestandsnaam"]
    df["Bestandsnaam"] = df["Bestandsnaam"].str.split("/").str[-1]
    df["Bestandsnaam"] = df["Bestandsnaam"].str.split(".txt").str[0]
    df["Bestandsnaam"] = df["Bestandsnaam"].apply(replace_underscore_with_period)
    df["ID"] = df["Bestandsnaam"].str.split("-").str[0]

    return df
