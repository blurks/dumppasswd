# dumppass

Dump your `pass` password store into a cleartext markdown file, so you
can print it out as a backup or share it via email or put in on github
or whatever.

## Usage

Just do `python dumppass.py`, enter the passphrase for your pgp key
and a `dump.md` file will be generated in your cwd.  If you have
multiple password stores or your password store is not at the default
location, set the "PASSWORD_STORE_DIR" environ variable accordingly,
eg.  `env PASSWORD_STORE_DIR=~/.password-store/ python dumppass.py`.

If you want to convert it into a pretty pdf that you can send to
management via email or put into your company's Dropbox, you can
install `pandoc` via `sudo apt-get install pandoc texlive-latex-base
texlive-fonts-recommended texlive-extra-utils texlive-latex-extra` and
do `pandoc dump.md -o dump.pdf`.

## Waranty

Use at your own risk.  There is no waranty for security because there
is no security in this package.  Don't be dumb dumping your passwords.
Don't send your passwords in cleartext via email.
