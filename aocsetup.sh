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
   echo "Syntax: aocsetup [-h|v|V] YEAR DAY"
   echo "Set up Advent of Code folder <DAY> in current directory."
   echo
   echo "Options:"
   echo "   -h     Print this Help."
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
# Get the options. This is not using getopts and works fine
# with positional arguments, but has the disadvantage of
# not being able to recognize incorrect arguments.
while :
do
    case "$1" in
        -V) Version ; exit;;
        -h) Help ; exit;;
        *) break ;;
    esac
    shift
done

if [[ -z "$1" ]] || [[ -z "$2" ]]; then
    echo Usage: $0 [-h] [-V] YEAR DAY
    exit 1
else
    YEAR="$1"
    DAY="$2"
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

echo "Advent of Code folder set up for ${DAY}/${YEAR}. Have fun!"