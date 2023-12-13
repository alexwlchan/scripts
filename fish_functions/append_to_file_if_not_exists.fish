# Append a line to a file, but only if the line isn't already in the file.
#
# This is similar to:
#
#     echo "This is my new line" >> myfile.txt
#
# but it will only insert it once, and won't insert it repeatedly if you
# call the function again.
#
function append_to_file_if_not_exists
    set target_file $argv[1]
    set line_to_append $argv[2]

    if not grep --quiet --fixed-strings --line-regexp "$line_to_append" "$target_file"
        echo $line_to_append >> $target_file
    end
end