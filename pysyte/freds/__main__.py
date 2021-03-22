from pysyte import cli


@cli.args
def fred():
    pass


# Below reformatted to allow flaking


def pa(*_, **__):
    pass


some_args = [
    pa(
        "directories",
        metavar="items",
        type=str,
        nargs="*",
        help="Only look for fred files in these directories",
    ),
    pa(
        "-d",
        "--debug",
        action="store_true",
        help="Debug the first fred.py with pudb",
    ),
    pa("-e", "--edit", action="store_true", help="Edit the freds with vim"),
    pa("-l", "--list", action="store_true", help="Use long listing"),
    pa("-r", "--remove", action="store_true", help="Remove the freds"),
    pa(
        "-p",
        "--python",
        action="store_true",
        help="Run the first fred.py script",
    ),
    pa(
        "-s",
        "--shell",
        action="store_true",
        help="Run the first fred.sh script",
    ),
    pa("-v", "--version", action="store_true", help="Show version"),
]
