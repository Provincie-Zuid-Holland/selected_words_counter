aword_list = ["Shell", "Hero", "Big", "City", "Dutch", "omgeving"]
# Lower case all words for easier matching.
aword_list = [aword.lower().replace(".", "") for aword in aword_list]


local_folder_mount_point = "./test_data"
local_folder_mount_point_extracted = (
    local_folder_mount_point[::-1].replace("/", "", 1)[::-1] + "_converted/"
)

keep_extracted = False

output_dir = "./output/"
