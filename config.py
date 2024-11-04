# Word lists Settings
# Example words to be found, make you own word list here
aword_list = ["Hero", "Big", "City", "Dutch", "Omgeving"]
# Lower case all words for easier matching.
aword_list = [aword.lower().replace(".", "") for aword in aword_list]

# Directories Settings
# Directory with data in it where the words should be found
local_folder_mount_point = "./data/"
# Directory where to write the converted data to.
local_folder_mount_point_extracted = (
    local_folder_mount_point[::-1].replace("/", "", 1)[::-1] + "_converted/"
)


# Extracting settings.
# Wether to delete converted data.
keep_extracted = False
# Wether to multithread read in of files, a possible speed up but currently not always working
multi_thread = False

# Set this to false if files have already been extracted.
extract = True


# Output Settings.
# Directory to output data to.
output_dir = "./output/"
version = 1
