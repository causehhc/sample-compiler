"""
<布尔表达式>-><布尔表达式>||<布尔项>|<布尔项>
<布尔项>-><布尔项>&&<布尔因子>|<布尔因子>
<布尔因子>-><算数表达式>|<关系表达式>|!<布尔表达式>
=============================================================
  b_expr -> b_item b_expr1
 b_expr1 -> || b_item b_expr1
          | ϵ
  b_item -> b_factor b_item1
 b_item1 -> && b_factor b_item1
          | ϵ
b_factor -> a_expr
          | r_expr
          | ! b_expr
"""
from Match_base import Match_base
from Expression_arithmetic import Match_a_expr
from Expression_relation import Match_r_expr


class Match_b_expr(Match_base):
    def __init__(self):
        super().__init__()

    def func_main(self, parent):
        iid = self.creat_node('b_expr', parent)

        if self.func_b_item(iid):
            if self.func_b_expr1(iid):
                return True
        return False

    def func_b_expr1(self, parent):
        iid = self.creat_node('b_expr1', parent)

        if self.token == '||':
            if self.get_next(iid) is None:
                return True
            if self.func_b_item(iid):
                if self.func_b_expr1(iid):
                    return True
        return True

    def func_b_item(self, parent):
        iid = self.creat_node('b_item', parent)

        if self.func_b_factor(iid):
            if self.func_b_item1(iid):
                return True
        return False

    def func_b_item1(self, parent):
        iid = self.creat_node('b_item1', parent)

        if self.token == '&&':
            if self.get_next(iid) is None:
                return True
            if self.func_b_factor(iid):
                if self.func_b_item1(iid):
                    return True
        return True

    def func_b_factor(self, parent):
        iid = self.creat_node('b_factor', parent)

        if self.is_a_expr(iid):
            if self.get_next(iid) is None:
                return True
            return True
        elif self.is_r_expr(iid):
            if self.get_next(iid) is None:
                return True
            return True
        elif self.token == '!':
            if self.get_next(iid) is None:
                return True
            if self.func_main(iid):
                return True
        return False

    def is_a_expr(self, iid):
        handler = Match_a_expr()
        handler.set_tokenList(self.arr[self.i:])
        res, i, subtree = handler.run(False)
        self.i += i
        self.tree.paste(iid, subtree)
        return res

    def is_r_expr(self, iid):
        handler = Match_r_expr()
        handler.set_tokenList(self.arr[self.i:])
        res, i, subtree = handler.run(False)
        self.i += i
        self.tree.paste(iid, subtree)
        return res


def main():
    handler = Match_b_expr()
    arr = [
        ['1', '&&', '1', '>', '2'],
        ['1', '+', '1', ')', '&&', '(', '(', '1', '+', '1', ')', '<=', '(', '1', '+', '1', ')'],
        ['(', '1', '+', '1', ')', '&&', '(', '1', '+', '1', ')', '<=', '(', '1', '+', '1', ')'],
        ['(', '1', '+', '1', ')', '&&', '(', '(', '1', '+', '1', ')', '<=', '(', '1', '+', '1', ')', ')']
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
