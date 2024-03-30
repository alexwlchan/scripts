# Append a line to a file, but only if the line isn't already in the file.
#
# This is similar to:
#
#     echo "This is my new line" >> myfile.txt
#
# but it will only insert it once, and won't insert it repeatedly if you
# call the function again.
#
function append_to_file_if_not_exists --description "Append a line to a file, but only if it's not already there" --argument-names target_file line_to_append
    if not grep --quiet --fixed-strings --line-regexp "$line_to_append" "$target_file" 2>/dev/null
        echo "$line_to_append" >>"$target_file"
    end
end
