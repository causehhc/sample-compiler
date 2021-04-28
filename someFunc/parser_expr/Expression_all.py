"""
<表达式> -> <算术表达式>|<关系表达式>|<布尔表达式>|<赋值表达式>
=============================================================
expr -> a_expr | r_expr | b_expr | g_expr

=============================================================

"""
from Match_base import Match_base


class Match_g_expr(Match_base):
    def __init__(self):
        super().__init__()

    def func_main(self, parent):
        iid = self.creat_node('g_expr', parent)

        if self.is_var():
            if self.get_next(iid) is None:
                return True
            if self.token == '=':
                if self.get_next(iid) is None:
                    return True
                if self.is_expr(iid):
                    if self.get_next(iid) is None:
                        return True
                    return True
        return False

    def is_var(self):
        return self.token.isidentifier()

    def is_expr(self, iid):
        handler = Match_expr()
        handler.set_tokenList(self.arr[self.i:])
        res, i, subtree = handler.run(False)
        self.i += i
        self.tree.paste(iid, subtree)
        return res


from Expression_arithmetic import Match_a_expr
from Expression_relation import Match_r_expr
from Expression_bool import Match_b_expr
# from Give_expression import Match_g_expr


class Match_expr(Match_base):
    def __init__(self):
        super().__init__()

    def func_main(self, parent):
        iid = self.creat_node('expr', parent)

        if self.is_g_expr(iid):
            if self.get_next(iid) is None:
                return True
            return True
        elif self.is_r_expr(iid):
            if self.get_next(iid) is None:
                return True
            return True
        elif self.is_b_expr(iid):
            if self.get_next(iid) is None:
                return True
            return True
        elif self.is_a_expr(iid):
            if self.get_next(iid) is None:
                return True
            return True
        return False

    def is_a_expr(self, iid):
        self.i = 0
        handler = Match_a_expr()
        handler.set_tokenList(self.arr[self.i:])
        res, i, subtree = handler.run(False)
        self.i += i
        self.tree.paste(iid, subtree)
        return res

    def is_r_expr(self, iid):
        self.i = 0
        handler = Match_r_expr()
        handler.set_tokenList(self.arr[self.i:])
        res, i, subtree = handler.run(False)
        self.i += i
        self.tree.paste(iid, subtree)
        return res

    def is_b_expr(self, iid):
        self.i = 0
        handler = Match_b_expr()
        handler.set_tokenList(self.arr[self.i:])
        res, i, subtree = handler.run(False)
        self.i += i
        self.tree.paste(iid, subtree)
        return res

    def is_g_expr(self, iid):
        self.i = 0
        handler = Match_g_expr()
        handler.set_tokenList(self.arr[self.i:])
        res, i, subtree = handler.run(False)
        self.i += i
        self.tree.paste(iid, subtree)
        return res


def main():
    handler = Match_expr()
    s = [
        # '1',
        # '1 + 1',
        # '1 || 1',
        # 'a = 1',
        'c = ( a + 1 ) > b'
    ]
    for item in s:
        print('Detected string: ', item)
        handler.set_tokenList(item.split(' '))
        res, idx, tree = handler.run(True)
        print('Compliance with the rules: ', res)
        if res is False:
            print('error info:', handler.info)
            print('error idx:', idx + 1)
        # handler.tree.show()
        print()


if __name__ == '__main__':
    main()
