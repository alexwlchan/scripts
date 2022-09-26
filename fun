#!/usr/bin/env bash
# This is a shortcut for 'mv' that I use for filing documents.
#
# I have a 'fun' directory that's divided into years where I put fun stuff;
# running `fun nameofdocument.pdf` will move it to the appropriate folder
# for the current year.

_file_by_year ~/Documents/fun "$@"