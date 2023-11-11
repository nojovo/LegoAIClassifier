from platform import uname
__all__ = []

os_type = uname()[4]

if os_type == "aarch64":
    from . import raspb
else:
    from . import windows


def capture():
    if os_type == "aarch64":
        return raspb.capture()
    else:
        from . import windows
        return windows.capture()


def get_frame(capture):
    if os_type == "aarch64":
        return raspb.get_frame(capture)
    else:
        return windows.get_frame(capture)
