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
终结符：<标识符>、<数值型常量>、<字符型常量>、(、)、运算符
=============================================================
<算术表达式> -> <算术表达式>+<项> | <算术表达式>-<项> | <项>
<项> -> <项>*<因子> | <项>/<因子> | <项>%<因子> | <因子>
<因子> -> (<算术表达式>) | <常量> | <变量>
<常量> -> <数值型常量> | <字符型常量>
<变量> -> <标识符>
终结符：<标识符>、<数值型常量>、<字符型常量>、(、)、运算符
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
END:const, var, ops
"""
from Match_base import Match_base


class Match_a_expr(Match_base):
    def __init__(self):
        super().__init__()

    def func_a_expr(self, parent):
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
            if self.func_a_expr(iid):
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

    def is_var(self):
        return self.token.isidentifier()

    def is_const(self):
        return self.token.isdigit()

    def run(self, flag):
        self.res = self.func_a_expr('root')
        if self.i == len(self.arr)-1:
            tmp = self.arr[:self.i+1]
        else:
            tmp = self.arr[:self.i]
        if self.res is True:
            if tmp != self.anls or len(self.arr) > len(self.anls):
                self.error(2, 'unmatched characters')
                if flag:
                    self.res = False
        return self.res, self.i-1, self.tree


def main():
    handler = Match_a_expr()
    s = [
        # ['1', '+', '1'],
        # ['1', '*', '1'],
        # ['(', '1', '+', '1', ')'],
        ['1', '.', '1'],
        ['1', '+', '+'],
        ['(', '1', '+', '1', '+', '(', '1', ')'],
        ['1', '*', '1', '+', '(', '1', ')', ')'],
        ['1', '*', '-', '1'],
        ['(', '(', '1', '+', '1', ')', ')'],
    ]
    for item in s:
        print('Detected string: ', item)
        handler.set_tokenList(item)
        res = handler.run(True)
        print('Compliance with the rules: ', res)
        if res is False:
            print(handler.info)
        # handler.tree.show()
        print()


if __name__ == '__main__':
    main()
