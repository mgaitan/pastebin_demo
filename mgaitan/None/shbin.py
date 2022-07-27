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

import itertools
import os
import pathlib
import secrets
import sys
from mimetypes import guess_extension

import magic
import pyclip
from docopt import DocoptExit, docopt
from github import Github, GithubException

__version__ = "0.1"



class FakePath:
    """
    A wrapper on a PurePath object (ie it doesn’t actually access a filesystem) 
    with an explicity content in bytes.
    """
    def __init__(self, *args, content=b""):
        self._path = pathlib.PurePath(*args)
        self._content = content

    def read_bytes(self):
        return self._content

    def __getattr__(self, attr):
        return getattr(self._path, attr)


def get_repo_and_user():
    gh = Github(os.environ["SHBIN_GITHUB_TOKEN"])
    return gh.get_repo(os.environ["SHBIN_REPO"]), gh.get_user().login
    

def main(argv=None) -> None:
    args = docopt(__doc__ + usage, argv, version=__version__)
    import ipdb;ipdb.set_trace()
    try:
        repo, user = get_repo_and_user()
    except Exception as e:
        raise DocoptExit(f"Ensure SHBIN_GITHUB_TOKEN and SHBIN_REPO environment variables are correctly set. (error {e})")


    if args["--from-clipboard"]:
        content = pyclip.paste()
        if args["--target"]:
            path_name = args['--target']
        else:
            extension = guess_extension(magic.from_buffer(content, mime=True))
            path_name = f"{secrets.token_urlsafe(8)}{extension}"
        files = [FakePath(path_name, content=content)]
        directory = f"{user}"
    else:
        files = itertools.chain.from_iterable(pathlib.Path(".").glob(pattern) for pattern in args["<path>"])
        directory = f"{user}/{args['--target']}".rstrip("/")
    
    message = args["--message"] or ""
    uploaded = 0
    for path in files:
        file_content = path.read_bytes()

        try:
            result = repo.create_file(f"{directory}/{path.name}", message, file_content)
        except GithubException:
            # file already exists
            if args["--new"]:
                new_path = f"{path.stem}_{secrets.token_urlsafe(8)}{path.suffix}"
                print(f"{path.name} already exists. Creating as {new_path}.", file=sys.stderr)
                result = repo.create_file(f"{directory}/{new_path}", message, file_content)

            else:           
                # TODO commit all the files in a single commit
                contents = repo.get_contents(f"{directory}/{path.name}")
                print(f"{path.name} already exists. Updating it.", file=sys.stderr)
                result = repo.update_file(f"{directory}/{path.name}", message, file_content, contents.sha)
        uploaded += 1

    url = result["content"].html_url.rpartition("/")[0] if uploaded > 1 else result["content"].html_url
    pyclip.copy(url)
    print(url)
    

if __name__ == "__main__":
    main()
