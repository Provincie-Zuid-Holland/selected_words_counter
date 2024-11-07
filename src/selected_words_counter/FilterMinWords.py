import pandas as pd


class FilterMinWords:
    """
    This class is used to filter out certain documents if that contain words in title or the filepath.

    """

    def __init__(self, afilename, min_words_path, aproject):
        if isinstance(afilename, pd.DataFrame):
            self.hits = afilename
        # Read in the file if it's only a file path
        elif ".xls" in afilename or ".xlsx" in afilename:
            self.hits = pd.read_excel(afilename)

        self.mins = pd.read_excel(min_words_path, engine="odf", header=None)
        self.project = aproject

    def filter(self):
        "Filter out in filepath and in filename"
        if self.project == "woo_shell_2024":
            for word in self.mins[0][0:56]:
                self.hits = self.hits[
                    ~self.hits["Locatie in iDMS"].str.contains(word.lower())
                ]
                # self.hits =self.hits[~self.hits['Bestandsnaam in export'].str.lower().str.contains(word.lower())]

        return self.hits
