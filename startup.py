"""args.py a mieru CLI processor
- it gets the commandline arguments and decides what to do
"""
import argparse

class Startup():
  def __init__(self):
    parser = argparse.ArgumentParser(description="A flexible manga and comic book reader.")
    parser.add_argument('-u',
                        help="specify user interface type", default="pc",
                        action="store", choices=["pc","hildon", "harmattan", "QML"])
    parser.add_argument('-p',
                        help="specify user interface type", default="pc",
                        action="store", choices=["maemo5", "harmattan", "desktop"])
    parser.add_argument('-o',
                        help="specify path to a manga or comic book to open", default=None,
                        action="store", metavar="path to file",)
    self.args = parser.parse_args()

