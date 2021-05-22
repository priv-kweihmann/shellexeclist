import argparse

from shellexeclist.shellident import ShellIdent


class ExtendAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        items = getattr(namespace, self.dest) or [] # pragma: no cover
        items.extend(values) # pragma: no cover
        setattr(namespace, self.dest, items) # pragma: no cover


def create_parser():
    parser = argparse.ArgumentParser(
        prog='shellexeclist', description='a tool to list executables called by a shell script',
    )
    parser.register('action', 'extend', ExtendAction)
    parser.add_argument('--forceshell', default=None,
                        help='Force to interpret as shell x')
    parser.add_argument('files', default=[], nargs='+',
                        help='Files to analyze')
    return parser


def parse_args():
    return create_parser().parse_args()  # pragma: no cover


def run(_args):
    res = set()
    for f in _args.files:
        for cmd in ShellIdent(f, forced_shell=_args.forceshell).RequiredBinaries:
            res.add(cmd)
    return sorted(res)


def main():
    _args = parse_args() # pragma: no cover
    for x in run(_args): # pragma: no cover
        print(x) # noqa T001, pragma: no cover


if __name__ == '__main__':
    main() # pragma: no cover
