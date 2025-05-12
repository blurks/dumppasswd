from collections import deque
from collections.abc import Iterator
from datetime import date
from getpass import getpass
from io import StringIO
from itertools import tee
import os
from os import path
from time import perf_counter

import gnupg  # type: ignore


PASSWORD_STORE_DIR = (
    os.environ.get("PASSWORD_STORE_DIR")
    or path.join(os.environ.get("HOME", default="."), ".password-store")
)
GNUPGHOME = (
    os.environ.get("GNUPGHOME")
    or path.join(os.environ.get("HOME", default="."), ".gnupg")
)


def walk(path_name: str) -> Iterator[tuple[int, str, tuple[str, ...]]]:
    if not path.isdir(path_name):
        raise ValueError("path must be a directory")

    stack: deque[tuple[int, str]] = deque()
    stack.append((0, path_name))

    while True:
        try:
            level, path_name = stack.pop()
            if path_name[-1] == "/":
                path_name = path_name[:-1]
            name = path.basename(path_name)
            listing1, listing2 = tee(
                path.join(path_name, basename)
                for basename in os.listdir(path_name)
            )
            files = tuple(
                filename
                for filename in sorted(listing1)
                if path.isfile(filename) and path.basename(filename)[0] != "."
            )
            yield (level, name, files)
            dirs = (
                (level + 1, dirname)
                for dirname in reversed(sorted(listing2))
                if path.isdir(dirname)
            )
            stack.extend(dirs)
        except IndexError:
            break


def build_document(passphrase: str) -> str:
    gpg = gnupg.GPG(gnupghome=GNUPGHOME)
    
    str_io = StringIO()
    str_io.write(f"# Passwörter\n\n")
    str_io.write(f"Stand {date.today().strftime('%d.%m.%Y')}\n\n")
    
    for level, name, files in walk(PASSWORD_STORE_DIR):
        headline_level = "#" * (level + 2)
        str_io.write(f"{headline_level} {name}\n\n")
        for f in files:
            str_io.write(f"* {path.basename(f)[:-4]}\n")
            str_io.write("  ```\n")
            str_io.write(str(gpg.decrypt_file(f, passphrase=passphrase)))
            str_io.write("  ```\n\n")
        str_io.write("\n")

    result = str_io.getvalue()
    str_io.close()
    return result


if __name__ == "__main__":
    passphrase = getpass()
    result = build_document(passphrase)
    with open("dump.md", "w") as f:
        f.write(result)
