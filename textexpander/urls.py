import subprocess


def get_safari_url(window: int = 1) -> str:
    """
    Get the URL of the given Safari window.
    """
    cmd = ["/Users/alexwlchan/.cargo/bin/safari", "url", "--window", str(window)]

    url = subprocess.check_output(cmd).decode("utf8")

    return url
