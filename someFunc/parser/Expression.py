from Match_base import Match_base


class Match_expr(Match_base):
    """
    <表达式> -> <算术表达式>|<关系表达式>|<布尔表达式>|<赋值表达式>
    =============================================================
    expr -> a_expr | r_expr | b_expr | g_expr
    """

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
        res = False
        if self.i < len(self.arr):
            handler.set_tokenList(self.arr[self.i:])
            res, i, subtree = handler.run(False)
            self.i += i
            self.tree.paste(iid, subtree)
        return res

    def is_r_expr(self, iid):
        self.i = 0
        handler = Match_r_expr()
        res = False
        if self.i < len(self.arr):
            handler.set_tokenList(self.arr[self.i:])
            res, i, subtree = handler.run(False)
            self.i += i
            self.tree.paste(iid, subtree)
        return res

    def is_b_expr(self, iid):
        self.i = 0
        handler = Match_b_expr()
        res = False
        if self.i < len(self.arr):
            handler.set_tokenList(self.arr[self.i:])
            res, i, subtree = handler.run(False)
            self.i += i
            self.tree.paste(iid, subtree)
        return res

    def is_g_expr(self, iid):
        self.i = 0
        handler = Match_g_expr()
        res = False
        if self.i < len(self.arr):
            handler.set_tokenList(self.arr[self.i:])
            res, i, subtree = handler.run(False)
            self.i += i
            self.tree.paste(iid, subtree)
        return res


class Match_a_expr(Match_base):
    """
    <表达式> -> <算术表达式> | <关系表达式> | <布尔表达式> | <赋值表达式>
    <算术表达式> -> <算术表达式>+<项> | <算术表达式>-<项> | <项>
    <项> -> <项>*<因子> | <项>/<因子> | <项>%<因子> | <因子>
    <因子> -> (<算术表达式>) | <常量> | <变量> | <函数调用>
    <常量> -> <数值型常量> | <字符型常量>
    <变量> -> <标识符>
    <函数调用> -> <标识符> | (<实参列表>)
    <实参列表> -> <实参> | #
    <实参> -> <表达式> | <表达式>,<实参>
    =============================================================
    <算术表达式> -> <算术表达式>+<项> | <算术表达式>-<项> | <项>
    <项> -> <项>*<因子> | <项>/<因子> | <项>%<因子> | <因子>
    <因子> -> (<算术表达式>) | <常量> | <变量>
    <常量> -> <数值型常量> | <字符型常量>
    <变量> -> <标识符>
    =============================================================
      a_expr -> a_item a_expr2
     a_expr2 -> a_expr1 a_expr2
              | ϵ
     a_expr1 -> + a_item
              | - a_item
      a_item -> a_factor a_item2
     a_item2 -> a_item1 a_item2
              | ϵ
     a_item1 -> * a_factor
              | / a_factor
              | % a_factor
    a_factor -> - a_para
              | a_para
      a_para -> ( a_expr )
              | const
              | var
    """

    def __init__(self):
        super().__init__()

    def func_main(self, parent):
        iid = self.creat_node('a_expr', parent)

        if self.func_a_item(iid):
            if self.func_a_expr2(iid):
                return True
        return False

    def func_a_expr2(self, parent):
        iid = self.creat_node('a_expr2', parent)

        if self.func_a_expr1(iid):
            if self.func_a_expr2(iid):
                return True
        return True

    def func_a_expr1(self, parent):
        iid = self.creat_node('a_expr1', parent)

        if self.token == '+':
            if self.get_next(iid) is None:
                return True
            if self.func_a_item(iid):
                return True
        elif self.token == '-':
            if self.get_next(iid) is None:
                return True
            if self.func_a_item(iid):
                return True
        return False

    def func_a_item(self, parent):
        iid = self.creat_node('a_item', parent)

        if self.func_a_factor(iid):
            if self.func_a_item2(iid):
                return True
        return False

    def func_a_item2(self, parent):
        iid = self.creat_node('a_item2', parent)

        if self.func_a_item1(iid):
            if self.func_a_item2(iid):
                return True
        return True

    def func_a_item1(self, parent):
        iid = self.creat_node('a_item1', parent)

        if self.token == '*':
            if self.get_next(iid) is None:
                return True
            if self.func_a_factor(iid):
                return True
        elif self.token == '/':
            if self.get_next(iid) is None:
                return True
            if self.func_a_factor(iid):
                return True
        elif self.token == '%':
            if self.get_next(iid) is None:
                return True
            if self.func_a_factor(iid):
                return True
        return False

    def func_a_factor(self, parent):
        iid = self.creat_node('a_factor', parent)

        if self.token == '-':
            if self.get_next(iid) is None:
                return True
            if self.func_a_para(iid):
                return True
        elif self.func_a_para(iid):
            return True
        return False

    def func_a_para(self, parent):
        iid = self.creat_node('a_para', parent)

        if self.token == '(':
            if self.get_next(iid) is None:
                return True
            if self.func_main(iid):
                if self.token == ')':
                    if self.get_next(iid) is None:
                        return True
                    return True
        elif self.is_const():
            if self.get_next(iid) is None:
                return True
            return True
        elif self.is_var():
            if self.get_next(iid) is None:
                return True
            return True
        return False


class Match_r_expr(Match_base):
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
        res = False
        if self.i < len(self.arr):
            handler.set_tokenList(self.arr[self.i:])
            res, i, subtree = handler.run(False)
            self.i += i
            self.tree.paste(iid, subtree)
        return res


class Match_b_expr(Match_base):
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

        if self.token == '!':
            if self.get_next(iid) is None:
                return True
            if self.func_main(iid):
                return True
        elif self.is_r_expr(iid):
            if self.get_next(iid) is None:
                return True
            return True
        elif self.is_a_expr(iid):
            if self.get_next(iid) is None:
                return True
            return True
        return False

    def is_a_expr(self, iid):
        handler = Match_a_expr()
        res = False
        if self.i < len(self.arr):
            handler.set_tokenList(self.arr[self.i:])
            res, i, subtree = handler.run(False)
            self.i += i
            self.tree.paste(iid, subtree)
        return res

    def is_r_expr(self, iid):
        handler = Match_r_expr()
        res = False
        if self.i < len(self.arr):
            handler.set_tokenList(self.arr[self.i:])
            res, i, subtree = handler.run(False)
            self.i += i
            self.tree.paste(iid, subtree)
        return res


class Match_g_expr(Match_base):
    """
    <赋值表达式> -> <标识符>=<表达式>
    =============================================================
    g_expr -> var = expr
    """

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

    def is_expr(self, iid):
        handler = Match_expr()
        res = False
        if self.i < len(self.arr):
            handler.set_tokenList(self.arr[self.i:])
            res, i, subtree = handler.run(False)
            self.i += i
            self.tree.paste(iid, subtree)
        return res


def main_expr():
    handler = Match_expr()
    s = [
        '1',
        '1 + 1',
        '1 || 1',
        'a = 1',
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


def main_a_expr():
    handler = Match_a_expr()
    s = [
        '1 + 1',
        '1 * 1',
        '( 1 + 1 )',
        '1 . 1',
        '1 + +',
        '( 1 + 1 + ( 1 )',
        '1 * 1 + ( 1 ) )',
        '1 * - 1',
        '( ( 1 + 1 ) )',
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


def main_r_expr():
    handler = Match_r_expr()
    s = [
        '( a + 1 ) > b',
        '1 > 2',
        '( 1 + 1 ) <= ( 1 + 1 )',
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


def main_b_expr():
    handler = Match_b_expr()
    s = [
        '1 && 1',
        '1 && 1 > 2',
        '1 + 1 ) && ( ( 1 + 1 ) <= ( 1 + 1 )',
        '( 1 + 1 ) && ( 1 + 1 ) <= ( 1 + 1 )',
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


def main_g_expr():
    handler = Match_g_expr()
    s = [
        '1 = 1',
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
    main_expr()
    # main_a_expr()
    # main_r_expr()
    # main_b_expr()
    # main_g_expr()
