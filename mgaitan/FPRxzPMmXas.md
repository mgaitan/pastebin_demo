Uploader of  file to your own folder on the pastebin repo.
To enable the use of this script, first yuo have to create a github token
and set it as an environment variable.

Follow these instructions to create the token
https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token
make sure of:
- set the Repo ans User scope
- Enable SSO
- install pygithub

Then set the env variable

export SHBIN_GITHUB_TOKEN = "<your personal token>"

to upload a file just: python pastebin_uploader <path to your file> <optional: message to commit>
"""

import argparse
import os
import pathlib
import secrets
import subprocess
import sys

from github import Github, GithubException


