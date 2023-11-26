# Removes the last-typed command from my fish history.
#
# This means that if I mistype a command and it starts appearing in
# my suggested commands, I can type it one more time then purge it from
# my history, to prevent it being suggested again.
#
# See https://alexwlchan.net/2023/forgetful-fish/
# See https://github.com/fish-shell/fish-shell/issues/10066
function forget_last_command
    set last_typed_command (history --max 1)
    history delete --exact --case-sensitive "$last_typed_command"
    history save
end
