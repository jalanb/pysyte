"""A simpler main program

Usage:

import dotsite as site

@site.streamer
def main(streams):
    for stream in streams:
        if stream.read() in 'qQ':
            break


sys.exit(site.main(main, __name__))
"""

def streamer(main_method):
    """Open a stream for the first file in arguments, or stdin"""
    if not arguments:
        return [sys.stdin]
    elif arguments[0] == '-c':
        return [StringIO(get_clipboard_data())]
    for argument in arguments:
        if os.path.isfile(argument):
            return file(argument, 'r')
    return []


def main(method, name):
    if name != '__main__':
        return
    stream = streamer(sys.argv)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
