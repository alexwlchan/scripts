###############################################################################
# When I'm in the Tailscale repos, I should use ./tool/go instead of
# the vanilla version of Go.
#
# This function will remind me to use ./tool/go instead of vanilla Go.
###############################################################################

function go --description 'Remind me to use ./tool/go in Tailscale repos'
	set ROOT $(git rev-parse --show-toplevel 2>/dev/null)

	if test -n "$ROOT"; and test -f "$ROOT/tool/go"
		set_color red
		echo "You should use ./tool/go instead!" >&2
		set_color normal
	else
		command go $argv
	end
end
