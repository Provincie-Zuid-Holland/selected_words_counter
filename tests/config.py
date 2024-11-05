aword_list = ["Shell", "Hero", "Big", "City", "Dutch", "omgeving"]
# Lower case all words for easier matching.
aword_list = [aword.lower().replace(".", "") for aword in aword_list]


target_dir = "./test_data"
target_dir_extracted = target_dir[::-1].replace("/", "", 1)[::-1] + "_converted/"

keep_extracted = False

output_dir = "./output/"
