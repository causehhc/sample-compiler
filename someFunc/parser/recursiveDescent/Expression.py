from someFunc.lexical.Automata import Lex_analyzer
from someFunc.parser.recursiveDescent.Match_base import Match_base


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
        self.index = 0
        handler = Match_a_expr()
        res = False
        if self.index < len(self.token_list):
            handler.set_tokenList(self.token_list[self.index:])
            res, i, subtree, info = handler.run(False)
            self.index += i
            self.tree.paste(iid, subtree)
            self.info = info
        return res

    def is_r_expr(self, iid):
        self.index = 0
        handler = Match_r_expr()
        res = False
        if self.index < len(self.token_list):
            handler.set_tokenList(self.token_list[self.index:])
            res, i, subtree, info = handler.run(False)
            self.index += i
            self.tree.paste(iid, subtree)
            self.info = info
        return res

    def is_b_expr(self, iid):
        self.index = 0
        handler = Match_b_expr()
        res = False
        if self.index < len(self.token_list):
            handler.set_tokenList(self.token_list[self.index:])
            res, i, subtree, info = handler.run(False)
            self.index += i
            self.tree.paste(iid, subtree)
            self.info = info
        return res

    def is_g_expr(self, iid):
        handler = Match_g_expr()
        res = False
        if self.index < len(self.token_list):
            handler.set_tokenList(self.token_list[self.index:])
            res, i, subtree, info = handler.run(False)
            self.index += i
            self.tree.paste(iid, subtree)
            self.info = info
        return res


class Match_a_expr(Match_base):
    """
    <算术表达式> -> <算术表达式> + <项> | <算术表达式> - <项> | <项>
    <项> -> <项> * <因子> | <项> / <因子> | <项> % <因子> | <因子>
    <因子> -> ( <算术表达式> ) | <常量> | <变量> | <函数调用>
    <常量> -> <数值型常量> | <字符型常量>
    <变量> -> <标识符>
    <函数调用> -> <标识符> | ( <实参列表> )
    <实参列表> -> <实参> | ϵ
    <实参> -> <表达式> | <表达式> , <实参>
    =============================================================
    a_expr -> a_expr + a_item | a_expr - a_item | a_item
    a_item -> a_item * a_factor | a_item / a_factor | a_item % a_factor | a_factor
    a_factor -> ( a_expr ) | const | var | func_call
    func_call -> var ( args_list )
    args_list -> args | ϵ
    =============================================================
   <a_expr> -> <a_term> <a_expr>''
   <a_term> -> <a_factor> <a_term>''
 <a_factor> -> ( <a_expr> )
             | <a_const>
             | <a_var>
             | <func_call>
  <a_const> -> <a_num_const>
             | <a_char_const>
    <a_var> -> <a_id>
<func_call> -> <a_id> ( <args_list> )
<args_list> -> <args>
             | ϵ
     <args> -> <expr> <args>'
  <a_expr>' -> + <a_term>
             | - <a_term>
  <a_term>' -> * <a_factor>
             | / <a_factor>
             | % <a_factor>
    <args>' -> ϵ
             | , <args>
 <a_expr>'' -> <a_expr>' <a_expr>''
             | ϵ
 <a_term>'' -> <a_term>' <a_term>''
             | ϵ

    """

    def __init__(self):
        super().__init__()

    def func_main(self, parent):
        iid = self.creat_node('a_expr', parent)

        if self.func_a_term(iid):
            if self.func_a_expr2(iid):
                return True
        return False

    def func_a_term(self, parent):
        iid = self.creat_node('a_term', parent)

        if self.func_a_factor(iid):
            if self.func_a_term2(iid):
                return True
        return False

    def func_a_factor(self, parent):
        iid = self.creat_node('a_factor', parent)

        if self.token == '(':
            if self.get_next(iid) is None:
                return True
            if self.func_main(iid):
                if self.token == ')':
                    if self.get_next(iid) is None:
                        return True
                    return True
        elif self.func_func_call(iid):
            return True
        elif self.func_a_var(iid):
            return True
        elif self.func_a_const(iid):
            return True
        return False

    def func_a_const(self, parent):
        iid = self.creat_node('a_const', parent)

        if self.is_const():
            if self.get_next(iid) is None:
                return True
            return True
        return False

    def func_a_var(self, parent):
        iid = self.creat_node('a_var', parent)

        if self.is_var():
            if self.get_next(iid) is None:
                return True
            return True
        return False

    def func_func_call(self, parent):
        iid = self.creat_node('func_call', parent)
        re_num = 0

        if self.is_var():
            re_num += 1
            if self.get_next(iid) is None:
                return True
            if self.token == '(':
                re_num += 1
                if self.get_next(iid) is None:
                    return True
                if self.func_args_list(iid):
                    if self.token == ')':
                        re_num += 1
                        if self.get_next(iid) is None:
                            return True
                        return True
        self.reset_token(re_num)
        return False

    def func_args_list(self, parent):
        iid = self.creat_node('args_list', parent)

        if self.func_args(iid):
            return True
        return True

    def func_args(self, parent):
        iid = self.creat_node('args', parent)

        if self.func_main(iid):
            if self.func_args1(iid):
                return True
        return False

    def func_a_expr1(self, parent):
        iid = self.creat_node('a_expr1', parent)

        if self.token == '+':
            if self.get_next(iid) is None:
                return True
            if self.func_a_term(iid):
                return True
        elif self.token == '-':
            if self.get_next(iid) is None:
                return True
            if self.func_a_term(iid):
                return True
        return False

    def func_a_term1(self, parent):
        iid = self.creat_node('a_term1', parent)

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

    def func_args1(self, parent):
        iid = self.creat_node('args1', parent)

        if self.token == ',':
            if self.get_next(iid) is None:
                return True
            if self.func_args(iid):
                return True
        return True

    def func_a_expr2(self, parent):
        iid = self.creat_node('a_expr2', parent)

        if self.func_a_expr1(iid):
            if self.func_a_expr2(iid):
                return True
        return True

    def func_a_term2(self, parent):
        iid = self.creat_node('a_term2', parent)

        if self.func_a_term1(iid):
            if self.func_a_term2(iid):
                return True
        return True

    def run_export_func_call(self, flag):
        self.res = self.func_func_call('root')
        if self.res is True:
            if len(self.token_list) > len(self.anls_proc):
                self.info = 'error: {}, token: {}, row: {}, col: {}\n'.format('unmatched char',
                                                                              self.token_node.data,
                                                                              self.token_node.row,
                                                                              self.token_node.col)
                if flag:
                    self.res = False
        if self.index == 0:
            self.index += 1
        return self.res, self.index - 1, self.tree, self.info


class Match_r_expr(Match_base):
    """
    <关系表达式> -> <算术表达式><关系运算符><算术表达式>
    <关系运算符> -> > | < | >= | <= | == | !=
    =============================================================
    r_expr -> a_expr r_op a_expr
    r_op -> > | < | >= | <= | == | !=
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
        if self.index < len(self.token_list):
            handler.set_tokenList(self.token_list[self.index:])
            res, i, subtree, info = handler.run(False)
            self.index += i
            self.tree.paste(iid, subtree)
            self.info = info
        return res


class Match_b_expr(Match_base):
    """
    <布尔表达式>-><布尔表达式>||<布尔项>|<布尔项>
    <布尔项>-><布尔项>&&<布尔因子>|<布尔因子>
    <布尔因子>-><算数表达式>|<关系表达式>|!<布尔表达式>
    =============================================================
    b_expr -> b_expr || b_item | b_item
    b_item -> b_item && b_factor | b_factor
    b_factor -> a_expr | r_expr | ! b_expr
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
        if self.index < len(self.token_list):
            handler.set_tokenList(self.token_list[self.index:])
            res, i, subtree, info = handler.run(False)
            self.index += i
            self.tree.paste(iid, subtree)
            self.info = info
        return res

    def is_r_expr(self, iid):
        handler = Match_r_expr()
        res = False
        if self.index < len(self.token_list):
            handler.set_tokenList(self.token_list[self.index:])
            res, i, subtree, info = handler.run(False)
            self.index += i
            self.tree.paste(iid, subtree)
            self.info = info
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
        if self.index < len(self.token_list):
            handler.set_tokenList(self.token_list[self.index:])
            res, i, subtree, info = handler.run(False)
            self.index += i
            self.tree.paste(iid, subtree)
            self.info = info
        return res


def main_expr():
    handler = Match_expr()
    s = [
        # '1 ',
        '1 + 1 ',
        # 'i<10 '
        # '1 || 1 ',
        # 'a = 1 ',
        # 'c = ( a + 1 ) > b ',
    ]
    lex_anal = Lex_analyzer()
    for item in s:
        print(item)
        lex_anal.set_text(item)
        token_list, info_list = lex_anal.get_token_info()
        handler.set_tokenList(token_list)
        res, idx, tree, error_list = handler.run(True)
        print(res)
        print(error_list)
        # handler.tree.show()
        print()


def main_a_expr():
    handler = Match_a_expr()
    s = [
        '1 + 1 ',
        # '1 * 1',
        # '( 1 + 1 )',
        # '1 . 1',
        # '1 + +',
        # '( 1 + 1 + ( 1 )',
        # '1 * 1 + ( 1 ) )',
        # '1 * - 1',
        # '( ( 1 + 1 ) )',
    ]
    lex_anal = Lex_analyzer()
    for item in s:
        print(item)
        lex_anal.set_text(item)
        token_list, info_list = lex_anal.get_token_info()
        handler.set_tokenList(token_list)
        res, idx, tree, error_list = handler.run(True)
        print(res)
        print(error_list)
        # handler.tree.show()
        print()


def main_r_expr():
    handler = Match_r_expr()
    s = [
        # '( a + 1 ) > b ',
        'i < 2 ',
        # '( 1 + 1 ) <= ( 1 + 1 ) ',
    ]
    lex_anal = Lex_analyzer()
    for item in s:
        print(item)
        lex_anal.set_text(item)
        token_list, info_list = lex_anal.get_token_info()
        handler.set_tokenList(token_list)
        res, idx, tree, error_list = handler.run(True)
        print(res)
        print(error_list)
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
    lex_anal = Lex_analyzer()
    for item in s:
        print(item)
        lex_anal.set_text(item)
        token_list, info_list = lex_anal.get_token_info()
        handler.set_tokenList(token_list)
        res, idx, tree, error_list = handler.run(True)
        print(res)
        print(error_list)
        # handler.tree.show()
        print()


def main_g_expr():
    handler = Match_g_expr()
    s = [
        '1 = 1',
    ]
    lex_anal = Lex_analyzer()
    for item in s:
        print(item)
        lex_anal.set_text(item)
        token_list, info_list = lex_anal.get_token_info()
        handler.set_tokenList(token_list)
        res, idx, tree, error_list = handler.run(True)
        print(res)
        print(error_list)
        # handler.tree.show()
        print()


if __name__ == '__main__':
    main_expr()
    # main_a_expr()
    # main_r_expr()
    # main_b_expr()
    # main_g_expr()
