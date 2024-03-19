from OE_Formatter_Functions.OE_Formatter import format_school

import os

def main():
    # Use the full path of the directory of the script being executed.
    script_directory = os.path.dirname(os.path.abspath(__file__))
    unformatted_directory = os.path.join(script_directory, 'Unformatted')
    school_folders = os.listdir(unformatted_directory)
    school_directories = [os.path.join(unformatted_directory, school_folder) for school_folder in school_folders if os.path.isdir(os.path.join(unformatted_directory, school_folder))]

    for school_directory in school_directories:
        format_school(school_directory, os.path.basename(school_directory))

if __name__ == "__main__":
    main()