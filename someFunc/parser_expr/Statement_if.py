"""
<if语句> -> if ( <表达式> ) <语句> | if ( <表达式> ) <语句> else <语句>
=============================================================
if_stmt -> if ( expr ) base_stmt | if ( expr ) base_stmt else base_stmt
=============================================================
 if_stmt -> if ( expr ) base_stmt if_stmt1
if_stmt1 -> else base_stmt
          | ϵ
"""
from Match_base import Match_base
from Statement_base import Match_base_stmt
from Expression_all import Match_expr


class Match_if_stmt(Match_base):
    def __init__(self):
        super().__init__()

    def func_if_stmt(self, parent):
        iid = self.creat_node('if_stmt', parent)

        if self.token == 'if':
            if self.get_next(iid) is None:
                return True
            if self.token == '(':
                if self.get_next(iid) is None:
                    return True
                if self.is_expr(iid):
                    if self.get_next(iid) is None:
                        return True
                    if self.token == ')':
                        if self.get_next(iid) is None:
                            return True
                        if self.is_base_stmt(iid):
                            if self.get_next(iid) is None:
                                return True
                            if self.func_if_stmt1(iid):
                                if self.get_next(iid) is None:
                                    return True
                                return True
        return False

    def func_if_stmt1(self, parent):
        iid = self.creat_node('if_stmt1', parent)

        if self.token == 'else':
            if self.get_next(iid) is None:
                return True
            if self.is_base_stmt(iid):
                if self.get_next(iid) is None:
                    return True
                return True
        return True

    def is_expr(self, iid):
        handler = Match_expr()
        handler.set_tokenList(self.arr[self.i:])
        res, i, subtree = handler.run(False)
        self.i += i
        self.tree.paste(iid, subtree)
        return res

    def is_base_stmt(self, iid):
        handler = Match_base_stmt()
        handler.set_tokenList(self.arr[self.i:])
        res, i, subtree = handler.run(False)
        self.i += i
        self.tree.paste(iid, subtree)
        return res

    def run(self, flag):
        self.res = self.func_if_stmt('root')
        if self.i == len(self.arr) - 1:
            tmp = self.arr[:self.i + 1]
        else:
            tmp = self.arr[:self.i]
        if self.res is True:
            if tmp != self.anls or len(self.arr) > len(self.anls):
                self.error(2, 'unmatched characters')
                if flag:
                    self.res = False
        return self.res, self.i - 1, self.tree


def main():
    handler = Match_if_stmt()
    s = [
        'if ( i < 10 ) i = i + 1 ; else const int j = 0 ;',
        # 'if ( i < 10 ) i = i + 1 ; else i = 0 ;',
    ]
    for item in s:
        print('Detected string: ', item)
        handler.set_tokenList(item.split(' '))
        res = handler.run(True)
        print('Compliance with the rules: ', res)
        if res is False:
            print(handler.info)
        handler.tree.show()
        print()


if __name__ == '__main__':
    main()
