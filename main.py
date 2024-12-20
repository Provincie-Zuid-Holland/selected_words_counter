import argparse

import config
from selected_words_counter.selected_words_counter import SelectedWordCounter


def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(
        description="Override config parameters when using this program from the command line."
    )

    # Add arguments for the config parameters you want to override
    parser.add_argument("--aword_list", type=str, help="Words array to be counted")
    parser.add_argument(
        "--target_dir", type=str, help="The directory to read files from"
    )
    parser.add_argument(
        "--target_dir_extracted",
        type=str,
        help="The directory to read files from",
    )

    parser.add_argument("--output_dir", type=str, help="Where to store the output file")

    parser.add_argument(
        "--keep_extracted",
        type=str,
        help="Wether the file extraction should be kept, which is used a intermittent step",
    )
    parser.add_argument(
        "--extract",
        type=str,
        help="Wether to extract files, use this only if files have already been extracted.",
    )

    parser.add_argument(
        "--multi_thread", type=str, help="Where to store the output file"
    )

    # Parse the command-line arguments
    args = parser.parse_args()

    # Override config parameters if they are provided in the command line
    if args.aword_list:
        # Lower case all words for easier matching.
        aword_list = [aword.lower().replace(".", "") for aword in args.aword_list]
        config.aword_list = aword_list
    if args.target_dir:
        config.target_dir = args.target_dir
    if args.target_dir_extracted:
        config.target_dir_extracted = args.target_dir_extracted
    if args.output_dir:
        config.output_dir = args.output_dir
    if args.keep_extracted:
        config.keep_extracted = args.keep_extracted
    if args.extract:
        config.extract = args.extract
    if args.multi_thread:
        config.multi_thread = args.multi_thread

    aselected_words_counter_class = SelectedWordCounter(
        config.aword_list,
        config.target_dir,
        config.target_dir_extracted,
        config.output_dir,
        keep_extract=config.keep_extracted,
        extract=config.extract,
        multi_thread=config.multi_thread,
    )
    aselected_words_counter_class.run()


if __name__ == "__main__":
    main()
