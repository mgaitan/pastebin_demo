"""Upload content to your pastebin repo"""
usage = """

Usage:
  shbin (-h | --help)
  shbin (<path>... | -x ) [-n] [-m <message>] [-o <target_path>]


Options:
  -h --help                                 Show this screen.
  -x --from-clipboard                       Paste content from clipboard instead file/s
  -m <message>, --message=<message>         Commit message
  -o <target>, --target=<target>            Optional filename or directory to upload file/s
  -n --new                                  Create a new file if the given already exists
  
"""
from docopt import docopt

print(docopt(__doc__ + usage, argv=None, version="0.1"))
