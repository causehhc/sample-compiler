"""
<表达式> -> <算术表达式>|<关系表达式>|<布尔表达式>|<赋值表达式>

<算术表达式> -> <算术表达式>+<项> | <算术表达式>-<项> | <项>
<项> -> <项>*<因子> | <项>/<因子> | <项>%<因子> | <因子>
<因子> -> -<参数>|<参数>
<参数> -> (<算术表达式>) | <常量> | <变量>

<关系表达式> -> <算术表达式><关系运算符><算术表达式>
<关系运算符> -> > | < | >= | <= | == | !=

<布尔表达式>-><布尔表达式>||<布尔项>|<布尔项>
<布尔项>-><布尔项>&&<布尔因子>|<布尔因子>
<布尔因子>-><算数表达式>|<关系表达式>|!<布尔表达式>

<赋值表达式> -> <标识符>=<表达式>
=============================================================
expr -> a_expr | r_expr | b_expr | g_expr
a_expr -> a_expr + a_item | a_expr - a_item | a_item
a_item -> a_item * a_factor | a_item / a_factor | a_item % a_factor | a_factor
a_factor -> - a_para | a_para
a_para -> ( a_expr ) | const | var
r_expr -> a_expr r_op a_expr
r_op -> > | < | >= | <= | == | !=
b_expr -> b_expr || b_item | b_item
b_item -> b_item && b_factor | b_factor
b_factor -> a_expr | r_expr | ! b_expr
g_expr -> var = expr
END:const, var, ops
=============================================================
    expr -> a_expr
          | r_expr
          | b_expr
          | g_expr
  a_expr -> a_item a_expr2
  a_item -> a_factor a_item2
a_factor -> - a_para
          | a_para
  a_para -> ( a_expr )
          | const
          | var
  r_expr -> - a_para a_item2 a_expr2 r_op a_expr
          | ( a_expr ) a_item2 a_expr2 r_op a_expr
          | const a_item2 a_expr2 r_op a_expr
          | var a_item2 a_expr2 r_op a_expr
    r_op -> >
          | <
          | >=
          | <=
          | ==
          | !=
  b_expr -> b_item b_expr1
  b_item -> b_factor b_item1
b_factor -> - a_para a_item2 a_expr2
          | ( a_expr ) a_item2 a_expr2
          | const a_item2 a_expr2
          | var a_item2 a_expr2
          | - a_para a_item2 a_expr2 r_op a_expr
          | ( a_expr ) a_item2 a_expr2 r_op a_expr
          | const a_item2 a_expr2 r_op a_expr
          | var a_item2 a_expr2 r_op a_expr
          | ! b_expr
  g_expr -> var = expr
 a_expr1 -> + a_item
          | - a_item
 a_item1 -> * a_factor
          | / a_factor
          | % a_factor
 a_expr2 -> a_expr1 a_expr2
          | #
 a_item2 -> a_item1 a_item2
          | #
 b_expr1 -> || b_item b_expr1
          | #
 b_item1 -> && b_factor b_item1
          | #
END:const, var, ops
"""
import uuid
from treelib import Tree


class Match_expr:
    def __init__(self):
        self.arr = None
        self._i = None
        self._token = None
        self._anls = None
        self.tree = None
        self.info = None

    def set_tokenList(self, arr):
        self.arr = arr
        self._i = 0
        self._token = self.arr[self._i]
        self._anls = []
        self.info = []
        self.tree = Tree()
        self.tree.create_node(tag='main', identifier='root')

    def reset_token(self):
        self._i = 0
        self._token = self.arr[self._i]
        self._anls = []

    def get_next(self, parent):
        self._anls.append(self._token)
        self.tree.create_node(tag=self._token, identifier=str(uuid.uuid1()), parent=parent)

        if self._i == len(self.arr) - 1:
            self._token = None
            return self._token
        else:
            self._i += 1
            self._token = self.arr[self._i]
            return self._token

    def error(self, error, summer):
        self.info = 'error{}: {}'.format(error, summer)

    def creat_node(self, name, parent):
        iid = str(uuid.uuid1())
        self.tree.create_node(tag='{}'.format(name), identifier=iid, parent=parent)
        return iid

    def isVar(self):
        if self._token is None:
            return False
        return self._token.isidentifier()

    def isConst(self):
        if self._token is None:
            return False
        return self._token.isdigit()

    # def func_expr(self, parent):
    #     iid = self.creat_node('expr', parent)
    #
    #     self.func_a_expr(iid)
    #     self.info.append(self.__anls)
    #     self.reset_token()
    #
    #     self.func_r_expr(iid)
    #     self.info.append(self.__anls)
    #     self.reset_token()
    #
    #     self.func_b_expr(iid)
    #     self.info.append(self.__anls)
    #     self.reset_token()
    #
    #     self.func_g_expr(iid)
    #     self.info.append(self.__anls)
    #     self.reset_token()

    def func_expr(self, parent):
        iid = self.creat_node('expr', parent)

        temp, temp_i = self._token, self._i
        if self.func_g_expr(iid):
            return True
        else:
            self._token, self._i = temp, temp_i
            if self.func_b_expr(iid):
                return True
            else:
                self._token, self._i = temp, temp_i
                if self.func_r_expr(iid):
                    return True
                else:
                    self._token, self._i = temp, temp_i
                    if self.func_a_expr(iid):
                        return True
                    return False
        # if self.func_a_expr(iid):
        #     return True
        # elif self.func_r_expr(iid):
        #     return True
        # elif self.func_b_expr(iid):
        #     return True
        # elif self.func_g_expr(iid):
        #     return True
        # return False

    def func_a_expr(self, parent):
        iid = self.creat_node('a_expr', parent)

        if self.func_a_item(iid):
            if self.func_a_expr2(iid):
                return True
        return False

    def func_a_item(self, parent):
        iid = self.creat_node('a_item', parent)

        if self.func_a_factor(iid):
            if self.func_a_item2(iid):
                return True
        return False

    def func_a_factor(self, parent):
        iid = self.creat_node('a_factor', parent)

        if self._token == '-':
            if self.get_next(iid) is None:
                return True
            if self.func_a_para(iid):
                return True
        elif self.func_a_para(iid):
            return True
        return False

    def func_a_para(self, parent):
        iid = self.creat_node('a_para', parent)

        if self._token == '(':
            if self.get_next(iid) is None:
                return True
            if self.func_a_expr(iid):
                if self._token == ')':
                    if self.get_next(iid) is None:
                        return True
                    return True
        elif self.isConst():
            if self.get_next(iid) is None:
                return True
            return True
        elif self.isVar():
            if self.get_next(iid) is None:
                return True
            return True
        return False

    def func_r_expr(self, parent):
        iid = self.creat_node('r_expr', parent)

        if self._token == '-':
            if self.get_next(iid) is None:
                return True
            if self.func_a_para(iid):
                if self.func_a_item2(iid):
                    if self.func_a_expr2(iid):
                        if self.func_r_op(iid):
                            if self.func_a_expr(iid):
                                return True
        elif self._token == '(':
            if self.get_next(iid) is None:
                return True
            if self.func_a_expr(iid):
                if self._token == ')':
                    if self.get_next(iid) is None:
                        return True
                    if self.func_a_item2(iid):
                        if self.func_a_expr2(iid):
                            if self.func_r_op(iid):
                                if self.func_a_expr(iid):
                                    return True
        elif self.isConst():
            if self.get_next(iid) is None:
                return True
            if self.func_a_item2(iid):
                if self.func_a_expr2(iid):
                    if self.func_r_op(iid):
                        if self.func_a_expr(iid):
                            return True
        elif self.isVar():
            if self.get_next(iid) is None:
                return True
            if self.func_a_item2(iid):
                if self.func_a_expr2(iid):
                    if self.func_r_op(iid):
                        if self.func_a_expr(iid):
                            return True
        return False

    def func_r_op(self, parent):
        iid = self.creat_node('r_op', parent)

        if self._token in ['>', '<', '>=', '<=', '==', '!=']:
            if self.get_next(iid) is None:
                return True
            return True
        return False

    def func_b_expr(self, parent):
        iid = self.creat_node('b_expr', parent)

        if self.func_b_item(iid):
            if self.func_b_expr1(iid):
                return True
        return False

    def func_b_item(self, parent):
        iid = self.creat_node('b_item', parent)

        if self.func_b_factor(iid):
            if self.func_b_item1(iid):
                return True
        return False

    def func_b_factor(self, parent):
        iid = self.creat_node('b_factor', parent)

        if self._token == '-':
            if self.get_next(iid) is None:
                return True
            if self.func_a_para(iid):
                if self.func_a_item2(iid):
                    if self.func_a_expr2(iid):
                        return True
        elif self._token == '(':
            if self.get_next(iid) is None:
                return True
            if self.func_a_expr(iid):
                if self._token == ')':
                    if self.get_next(iid) is None:
                        return True
                    if self.func_a_item2(iid):
                        if self.func_a_expr2(iid):
                            return True
        elif self.isConst():
            if self.get_next(iid) is None:
                return True
            if self.func_a_item2(iid):
                if self.func_a_expr2(iid):
                    return True
        elif self.isVar():
            if self.get_next(iid) is None:
                return True
            if self.func_a_item2(iid):
                if self.func_a_expr2(iid):
                    return True

        if self._token == '-':
            if self.get_next(iid) is None:
                return True
            if self.func_a_para(iid):
                if self.func_a_item2(iid):
                    if self.func_a_expr2(iid):
                        if self.func_r_op(iid):
                            if self.func_a_expr(iid):
                                return True
        elif self._token == '(':
            if self.get_next(iid) is None:
                return True
            if self.func_a_expr(iid):
                if self._token == ')':
                    if self.get_next(iid) is None:
                        return True
                    if self.func_a_item2(iid):
                        if self.func_a_expr2(iid):
                            if self.func_r_op(iid):
                                if self.func_a_expr(iid):
                                    return True
        elif self.isConst():
            if self.get_next(iid) is None:
                return True
            if self.func_a_item2(iid):
                if self.func_a_expr2(iid):
                    if self.func_r_op(iid):
                        if self.func_a_expr(iid):
                            return True
        elif self.isVar():
            if self.get_next(iid) is None:
                return True
            if self.func_a_item2(iid):
                if self.func_a_expr2(iid):
                    if self.func_r_op(iid):
                        if self.func_a_expr(iid):
                            return True
        elif self._token == '!':
            if self.get_next(iid) is None:
                return True
            if self.func_b_expr(iid):
                return True
        return False

    def func_g_expr(self, parent):
        iid = self.creat_node('g_expr', parent)

        if self.isVar():
            if self.get_next(iid) is None:
                return True
            if self._token == '=':
                if self.get_next(iid) is None:
                    return True
                if self.func_expr(iid):
                    return True
        return False

    def func_a_expr1(self, parent):
        iid = self.creat_node('a_expr1', parent)

        if self._token == '+':
            if self.get_next(iid) is None:
                return True
            if self.func_a_item(iid):
                return True
        elif self._token == '-':
            if self.get_next(iid) is None:
                return True
            if self.func_a_item(iid):
                return True
        return False

    def func_a_item1(self, parent):
        iid = self.creat_node('a_item1', parent)

        if self._token == '*':
            if self.get_next(iid) is None:
                return True
            if self.func_a_factor(iid):
                return True
        elif self._token == '/':
            if self.get_next(iid) is None:
                return True
            if self.func_a_factor(iid):
                return True
        elif self._token == '%':
            if self.get_next(iid) is None:
                return True
            if self.func_a_factor(iid):
                return True
        return False

    def func_a_expr2(self, parent):
        iid = self.creat_node('a_expr2', parent)

        if self.func_a_expr1(iid):
            if self.func_a_expr2(iid):
                return True
        return True

    def func_a_item2(self, parent):
        iid = self.creat_node('a_item2', parent)

        if self.func_a_item1(iid):
            if self.func_a_item1(iid):
                return True
        return True

    def func_b_expr1(self, parent):
        iid = self.creat_node('b_expr1', parent)

        if self._token == '||':
            if self.get_next(iid) is None:
                return True
            if self.func_b_item(iid):
                if self.func_b_expr1(iid):
                    return True
        return True

    def func_b_item1(self, parent):
        iid = self.creat_node('b_item1', parent)

        if self._token == '&&':
            if self.get_next(iid) is None:
                return True
            if self.func_b_factor(iid):
                if self.func_b_item1(iid):
                    return True
        return True

    def run(self):
        self.func_expr('root')
        for case in self.info:
            if case == self.arr:
                return True
        return False


if __name__ == '__main__':
    handler = Match_expr()
    arr = []
    s = ['1 + 1',
         'c = ( ( a + 1 ) > b)',
         'a || a',
         'a = 1']
    for item in s:
        arr.append(item.split(' '))
    for i in range(1, 2):
        print('Detected string: ', arr[i])
        handler.set_tokenList(arr[i])
        res = handler.run()
        print('Compliance with the rules: ', res)
        if res is False:
            print(handler.info)
        handler.tree.show()
        print()
