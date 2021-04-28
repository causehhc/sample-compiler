"""
<赋值语句> -> <赋值表达式> ;
终结符：<赋值表达式>、;
=============================================================
give_stmt -> g_expr ;
END:g_expr, ;
"""
from Match_base import Match_base
from Expression_all import Match_g_expr


class Match_give_stmt(Match_base):
    def __init__(self):
        super().__init__()

    def func_main(self, parent):
        iid = self.creat_node('give_stmt', parent)

        if self.is_g_expr(iid):
            if self.get_next(iid) is None:
                return True
            if self.token == ';':
                if self.get_next(iid) is None:
                    return True
                return True
        return False

    def is_g_expr(self, iid):
        self.i = 0
        handler = Match_g_expr()
        handler.set_tokenList(self.arr[self.i:])
        res, i, subtree = handler.run(False)
        self.i += i
        self.tree.paste(iid, subtree)
        return res


def main():
    handler = Match_give_stmt()
    s = [
        ['i', '=', '1', ';'],
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
