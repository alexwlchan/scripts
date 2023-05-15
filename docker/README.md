# docker

These scripts are all Docker-based wrappers for tools of the same name (`cloc`, `rubocop`, and so on).

I prefer to use Docker over installing packages directly on my system because I've had multiple headaches with Mac package managers, whereas Docker works fairly reliably for me.

The `docker` script is a wrapper around the real Docker CLI.
I don't always have Docker running; this wrapper intercepts all calls to `docker` and starts Docker if it isn't already running.
