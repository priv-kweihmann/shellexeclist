import os
import re

import chardet

from shellexeclist.defaults import BUILTINS
from shellexeclist.parser import ShellParser
from shellexeclist.bb.pysh.sherrors import ShellSyntaxError


class ShellIdent():

    def __init__(self, path, forced_shell=None):
        self.__path = path

        with open(self.__path, 'rb') as i:
            self.__content = i.read()
            _enc = chardet.detect(self.__content)
            self.__content = self.__content.decode(_enc.get('encoding', 'utf-8'))

        self.__shell = forced_shell or self.__ident_shell()
        try:
            self.__binaries = [x.split(' ')[0] for x in ShellParser().parse_shell(self.__content)]
        except ShellSyntaxError:
            self.__binaries = []

    def __ident_shell(self):
        pattern = r'^#!\s*(?P<shell>.*)\s*'
        m = re.match(pattern, self.__content.split('\n')[0])
        if m:
            return os.path.basename(m.group('shell').split(' ')[0])
        return 'sh'

    @property
    def Shell(self):
        return self.__shell

    @property
    def UsedBinaries(self):
        _raw = [x.strip('"') for x in self.__binaries if x not in BUILTINS.get(self.Shell, [])]
        _raw = [x for x in _raw if not x.startswith('$')]
        _raw = [x for x in _raw if not x.startswith('-')]
        _raw = [re.sub(r'^\./', '', x) for x in _raw]
        return sorted(_raw)

    @property
    def RequiredBinaries(self):
        return sorted(set(self.UsedBinaries + [self.Shell]))
