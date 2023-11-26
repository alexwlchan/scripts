###############################################################################
# My fish prompt
#
# This has been inspired by various examples from other people, not all
# of whom I kept notes of.
###############################################################################


function print_current_directory
    set_color green
    printf (echo -n (prompt_pwd))
    set_color normal
end


# Print information about the current Git branch, if I'm in a Git repo.
#
# At one point I had similar functions for getting SVN and Mercurial information,
# but at time of writing (Apr 2022), it's been 5+ years since I used a non-Git VCS.
# It's not worth maintaining those alternatives or running them against every
# shell prompt.
function print_git_information
    which git 2>&1 >/dev/null
    if [ $status = 0 ]
        set branch (git branch --no-color 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/\1/')
        if [ -n "$branch" ]
            set_color normal
            printf " on git:"

            if test (basename "$branch") = main
                set_color cyan
            else
                set_color purple
            end

            printf "$branch"

            # Print an asterisk to indicate uncommitted changes, if there are any
            if ! git diff-index --quiet HEAD --
                printf "*"
            end

            set_color normal
        end
    end
end


# Print information about the current virtualenv, if one is enabled.
#
# The VIRTUAL_ENV_DISABLE_PROMPT command disables the auto-prepending of the
# venv into my prompt by the virtualenv itself; see
# https://stackoverflow.com/a/63029769/1558022
set -x VIRTUAL_ENV_DISABLE_PROMPT 1

function print_venv_information
    if [ -n "$VIRTUAL_ENV" ]
        set_color normal
        printf " using "

        if test (basename "$VIRTUAL_ENV") = ".venv"
            set_color cyan
        else
            set_color purple
        end

        printf (basename "$VIRTUAL_ENV")
        set_color normal
    end
end


# If I'm running over SSH, prepend the name of the remote host to
# the context line.
function print_ssh_information
    if set -q SSH_CLIENT
        printf "("
        set_color purple
        printf (echo -n (hostname))
        set_color normal
        printf ") "
    end
end


# Allow me to prevent certain dangerous commands from ever
# appearing in autocomplete.
#
# See https://alexwlchan.net/2023/forgetful-fish/
# See https://github.com/fish-shell/fish-shell/issues/10066
function forget_dangerous_history_commands
    set last_typed_command (history --max 1)

    if [ "$last_typed_command" = "git push origin (gcb) --force" ]
        history delete --exact --case-sensitive "$last_typed_command"
        history save
    end
end


function fish_prompt --description 'Write out the prompt'
    # forget_dangerous_history_commands

    # Put a newline between new prompts for cleanliness, but not on the first run.
    #
    # This means the first prompt of a new session is right at the top of
    # the terminal window, not with a newline above it.
    #
    # If we're in an SSH session, we always insert a newline, even on the first
    # command -- to separate from the client session.  I avoid getting the
    # 'Last login' message with `touch ~/.hushlogin`
    if set -q SSH_CLIENT
        echo ''
    else
        if test \( -f "/tmp/$TERM_SESSION_ID" -o -f "/tmp/$XDG_SESSION_ID" \)
            echo ''
        end

        touch "/tmp/$TERM_SESSION_ID" 2>/dev/null
        touch "/tmp/$XDG_SESSION_ID" 2>/dev/null
    end

    # Print some context about where I'm running this command.
    #
    # If I'm in my home directory, the context isn't very interesting (it's where
    # new shells open, and it's not in Git), so skip the context line to reduce
    # visual noise.
    if [ (prompt_pwd) = "~" ]
        if set -q SSH_CLIENT
            print_ssh_information
            echo ''
        end
        echo '$ '
        return
    end

    print_ssh_information
    print_current_directory
    print_git_information
    print_venv_information

    # Print the shell prompt.
    #
    # I have a different prompt for when I'm running as root; admittedly this
    # is extremely rare if I'm also using fish, but if I am I want a visual cue
    # that this terminal is unusual.
    #
    # I print the prompt on a separate line to the context information so it's
    # always in the same place: as I'm typing commands, I get the full width of
    # the terminal to use, rather than a variable amount based on the context line.
    set_color normal
    if [ "$USER" = root ]
        echo '' & echo '# '
    else
        echo '' & echo '$ '
    end
end
