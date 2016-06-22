"""A simpler main program

Usage:

import dotsite as site

def main(streams):
    for stream in streams:
        if stream.read() in 'qQ':
            break


sys.exit(site.main(main, __name__))
"""

@site.decorators.streamer
def main(streams):
    for stream in streams:
        if stream.read() in 'qQ':
            break


def exit(method, name):
    if __name__ == '__main__':
        sys.exit(method(sys.argv))
