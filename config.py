#Words to be found.
aword_list = ["Shell", "Hero", "Big", "City", "Dutch", "omgeving"]
# Lower case all words for easier matching.
aword_list = [aword.lower().replace(".", "") for aword in aword_list]
# Directory with data in it.
local_folder_mount_point = "./data/"
# Directory where to write the converted data to.
local_folder_mount_point_extracted = (
    local_folder_mount_point[::-1].replace("/", "", 1)[::-1] + "_converted/"
)
# Directory to output data to.
output_dir = "./output/"
# Wether to delete converted data.
keep_extracted = False
# Wether to multithread read in of files, a possible speed up but currently not always working
multi_thread = False

#Set this to false if files have already been extracted.
extract = True