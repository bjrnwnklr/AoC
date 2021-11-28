#!/bin/bash
############################################################
# AoC Setup script.
#
# - Creates a folder for the AoC day in the folder it is 
#   called from
# - Copies the contents of the `template` folder into the
#   new folder
# - Renames the files to the `aoc<year>_<day>.py` format
#   and changes references in the python files to the
#   correct year and day.
#
# v1.0, 27 Nov 2021
# Bjoern Winkler
############################################################

# Set variables
Version="1.0"
Date="27 Nov 2021"

############################################################
# Help                                                     #
############################################################
Help()
{
   # Display Help
   echo "Sets up a day folder for Advent of Code. Creates a new <day> folder in"
   echo "the current folder, if not existing, then copies files from the"
   echo "'template' folder into the new folder and does some renaming."
   echo
   echo "Syntax: aocsetup [-h|v|V] -y YEAR -d DAY"
   echo "Set up Advent of Code folder <DAY> in current directory."
   echo
   echo "Options:"
   echo "   -h     Print this Help."
   echo "   -v     Verbose mode."
   echo "   -V     Print software version and exit."
   echo
}

############################################################
# Version                                                  #
############################################################
Version()
{
   # Display Help
   echo "aocsetup ${Version}, ${Date}"
   echo
}

############################################################
############################################################
# Main program                                             #
############################################################
############################################################

############################################################
# Process the input options. Add options as needed.        #
############################################################
# Get the options
while getopts ":hVy:d:" option; do
    case $option in
        h) # display Help
            Help
            exit;;
        V) # display Version and exit
            Version
            exit;;
        y) # the AoC Year
            YEAR=$OPTARG;;
        d) # the AoC day
            DAY=$OPTARG;;
        \?) # Invalid option
            echo "Error: Invalid option"
            exit 1;;
    esac
done

# check if date and year have been Set
if [[ -z ${YEAR} ]];
then
    echo "Year not specified, exiting."
    exit 1;
fi

if [[ -z ${DAY} ]];
then
    echo "Day not specified, exiting."
    exit 1;
fi

############################################################
# Check if Day folder exists, if not create it.
############################################################
if [[ -d ${DAY} ]];
then
    echo "Folder ${DAY} already exists, exiting."
    exit 1;
else
    mkdir ${DAY}
fi

############################################################
# Copy templates folder contents into the new Day folder
############################################################
# get the directory the script is run from
# https://stackoverflow.com/a/246128
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# check if templates directory exists
if [[ -d "${SCRIPT_DIR}/template" ]];
then
    cp -r "${SCRIPT_DIR}"/template/* "${DAY}"
else
    echo "Template directory not found in ${SCRIPT_DIR}, exiting."
    exit 1;
fi

############################################################
# Rename the files with YEAR and DAY
############################################################
FILES=("aocyyyy_dd.py" "test/test_aocyyyy_dd.py")

for f in ${FILES[@]}; do
    RESULT=$( echo $f | sed "s/yyyy/${YEAR}/ ; s/dd/${DAY}/")
    mv ${DAY}/$f ${DAY}/$RESULT
done

# substitute references to yyyy and dd with YEAR and DAY in the test files
sed -i "s/yyyy_dd/${YEAR}_${DAY}/g" ${DAY}/test/test_aoc${YEAR}_${DAY}.py

echo "Called from ${SCRIPT_DIR}"