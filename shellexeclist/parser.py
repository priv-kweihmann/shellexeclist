from itertools import chain

from shellexeclist.bb.pysh import pyshlex
from shellexeclist.bb.pysh import pyshyacc


class ShellParser():
    def __init__(self):
        self.funcdefs = set()
        self.allexecs = set()
        self.execs = set()

    def parse_shell(self, value):
        try:
            self._parse_shell(value)
        except pyshlex.NeedMore:
            pass  # pragma: no cover
        self.execs = set(cmd for cmd in self.allexecs if cmd not in self.funcdefs)  # noqa C401

        return self.execs

    def _parse_shell(self, value):
        tokens, _ = pyshyacc.parse(value, eof=True, debug=False)

        self.process_tokens(tokens)

    def process_tokens(self, tokens):  # noqa: CFQ004
        def function_definition(value):
            self.funcdefs.add(value.name)
            return [value.body], None

        def case_clause(value):
            # Element 0 of each item in the case is the list of patterns, and
            # Element 1 of each item in the case is the list of commands to be
            # executed when that pattern matches.
            words = chain(*[item[0] for item in value.items])
            cmds = chain(*[item[1] for item in value.items])
            return cmds, words

        def if_clause(value):
            main = chain(value.cond, value.if_cmds)  # pragma: no cover
            rest = value.else_cmds  # pragma: no cover
            if isinstance(rest, tuple) and rest[0] == 'elif':  # pragma: no cover
                return chain(main, if_clause(rest[1]))  # pragma: no cover
            else:  # pragma: no cover
                return chain(main, rest)  # pragma: no cover

        def simple_command(value):
            return None, chain(value.words, (assign[1] for assign in value.assigns))

        token_handlers = {
            'and_or': lambda x: ((x.left, x.right), None),
            'async': lambda x: ([x], None),
            'brace_group': lambda x: (x.cmds, None),
            'for_clause': lambda x: (x.cmds, x.items),
            'function_definition': function_definition,
            'if_clause': lambda x: (if_clause(x), None),
            'pipeline': lambda x: (x.commands, None),
            'redirect_list': lambda x: ([x.cmd], None),
            'subshell': lambda x: (x.cmds, None),
            'while_clause': lambda x: (chain(x.condition, x.cmds), None),
            'until_clause': lambda x: (chain(x.condition, x.cmds), None),
            'simple_command': simple_command,
            'case_clause': case_clause,
        }

        def process_token_list(tokens):
            for token in tokens:
                if isinstance(token, list):
                    process_token_list(token)
                    continue
                name, value = token
                try:
                    more_tokens, words = token_handlers[name](value)
                except KeyError:  # pragma: no cover
                    raise NotImplementedError('Unsupported token type ' + name)

                if more_tokens:
                    self.process_tokens(more_tokens)

                if words:
                    self.process_words(words)

        process_token_list(tokens)

    def process_words(self, words):
        words = list(words)
        for word in list(words):
            wtree = pyshlex.make_wordtree(word[1])
            for part in wtree:
                if not isinstance(part, list):
                    continue

                if part[0] in ('`', '$('):
                    command = pyshlex.wordtree_as_string(part[1:-1])
                    self._parse_shell(command)

                    if word[0] in ('cmd_name', 'cmd_word'):  # pragma: no cover
                        if word in words:  # pragma: no cover
                            words.remove(word)

        usetoken = False
        for word in words:
            if word[0] in ('cmd_name', 'cmd_word') or \
               (usetoken and word[0] == 'TOKEN'):  # noqa N400
                if '=' in word[1]:
                    usetoken = True
                    continue

                cmd = word[1]
                if cmd.startswith('$'):
                    pass  # pragma: no cover
                elif cmd == 'eval':
                    command = ' '.join(
                        word for _, word in words[1:])  # pragma: no cover
                    self._parse_shell(command)  # pragma: no cover
                else:
                    self.allexecs.add(cmd)
                break
