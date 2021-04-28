"""
<关系表达式> -> <算术表达式><关系运算符><算术表达式>
<关系运算符> -> > | < | >= | <= | == | !=
=============================================================
r_expr -> a_expr r_op a_expr
  r_op -> >
        | <
        | >=
        | <=
        | ==
        | !=
"""

from Match_base import Match_base
from Expression_arithmetic import Match_a_expr


class Match_r_expr(Match_base):
    def __init__(self):
        super().__init__()

    def func_main(self, parent):
        iid = self.creat_node('r_expr', parent)

        if self.is_a_expr(iid):
            if self.get_next(iid) is None:
                return True
            if self.func_r_op(iid):
                if self.is_a_expr(iid):
                    if self.get_next(iid) is None:
                        return True
                    return True
        return False

    def func_r_op(self, parent):
        iid = self.creat_node('r_op', parent)

        if self.token in ['>', '<', '=', '!', '<=', '>=', '==', '!=']:
            if self.get_next(iid) is None:
                return True
            return True
        return False

    def is_a_expr(self, iid):
        handler = Match_a_expr()
        handler.set_tokenList(self.arr[self.i:])
        res, i, subtree = handler.run(False)
        self.i += i
        self.tree.paste(iid, subtree)
        return res


def main():
    handler = Match_r_expr()
    arr = [
        ['(', 'a', '+', '1', ')', '>', 'b'],
        ['1', '>', '2'],
        ['(', '1', '+', '1', ')', '<=', '(', '1', '+', '1', ')'],
    ]
    for item in arr:
        print('Detected string: ', item)
        handler.set_tokenList(item)
        res = handler.run(True)
        print('Compliance with the rules: ', res)
        if res is False:
            print(handler.info)
        # handler.tree.show()
        print()
    pass


if __name__ == '__main__':
    main()
