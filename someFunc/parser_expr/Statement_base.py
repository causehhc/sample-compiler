"""
<语句> -> <声明语句> | <执行语句>
<声明语句> -> <值声明> | <函数声明> | @
<值声明> -> <常量声明> | <变量声明>
<常量声明> -> const <常量类型> <常量声明表>
<常量类型> -> int | char | float
<常量声明表> -> <标识符> = <常量> ; | <标识符> = <常量> , <常量声明表>
<变量声明> -> <变量类型> <变量声明表>
<变量类型> -> int | char | float
<变量声明表> -> <单变量声明> ; | <单变量声明> , <变量声明表>
<单变量声明> -> <变量> | <变量> = <表达式>
<函数声明> -> <函数类型> <标识符> ( <函数声明形参列表> ) ;
<函数类型> -> int | char | float | void
<函数声明形参列表> -> <函数声明形参> | @
<函数声明形参> -> <变量类型> | <变量类型> , <函数声明形参>
=============================================================
stmt -> decl_stmt | exec_stmt
decl_stmt -> val_decl | func_decl | ϵ
val_decl -> const_decl | var_decl
const_decl -> const const_type const_decl_table
const_type -> int | char | float
const_decl_table -> id = const ; | id = const , const_decl_table
var_decl -> var_type var_decl_table
var_type -> int | char | float
var_decl_table -> sin_var_decl ; | sin_var_decl , var_decl_table
sin_var_decl -> var | var = expr
func_decl -> func_type id ( func_decl_formal_para_list ) ;
func_type -> int | char | float | void
func_decl_formal_para_list -> func_decl_para | ϵ
func_decl_para -> var_type | var_type , func_decl_para
=============================================================
                      stmt -> decl_stmt
                            | exec_stmt
                 decl_stmt -> val_decl
                            | func_decl
                            | ϵ
                  val_decl -> const_decl
                            | var_decl
                const_decl -> const const_type const_decl_table
                const_type -> int
                            | char
                            | float
          const_decl_table -> id = const const_decl_table'
                  var_decl -> var_type var_decl_table
                  var_type -> int
                            | char
                            | float
            var_decl_table -> sin_var_decl var_decl_table'
              sin_var_decl -> var sin_var_decl'
                 func_decl -> func_type id ( func_decl_formal_para_list ) ;
                 func_type -> int
                            | char
                            | float
                            | void
func_decl_formal_para_list -> func_decl_para
                            | ϵ
            func_decl_para -> int func_decl_para'
                            | char func_decl_para'
                            | float func_decl_para'
         const_decl_table' -> ;
                            | , const_decl_table
           var_decl_table' -> ;
                            | , var_decl_table
             sin_var_decl' -> ϵ
                            | = expr
           func_decl_para' -> ϵ
                            | , func_decl_para

=============================================================
Symbol	Nullable	First	Follow
const_decl	false	const	$
const_decl_table	false	id	$
const_decl_table'	false	, ;	$
const_type	false	char float int	id
decl_stmt	false	@ char const float int void	$
func_decl	false	char float int void	$
func_decl_formal_para_list	false	@ char float int	)
func_decl_para	false	char float int	)
func_decl_para'	true	, ϵ	)
func_type	false	char float int void	id
sin_var_decl	false	var	, ;
sin_var_decl'	true	= ϵ	, ;
stmt	false	@ char const exec_stmt float int void	$
val_decl	false	char const float int	$
var_decl	false	char float int	$
var_decl_table	false	var	$
var_decl_table'	false	, ;	$
var_type	false	char float int	var
=============================================================

"""
from Match_base import Match_base
from Expression_all import Match_expr, Match_g_expr


class Match_base_stmt(Match_base):
    def __init__(self):
        super().__init__()

    def func_main(self, parent):
        iid = self.creat_node('stmt', parent)

        # if self.func_decl_stmt(iid):
        #     return True
        # elif self.is_g_expr():
        #     if self.get_next(iid) is None:
        #         return True
        #     return True
        if self.is_g_expr(iid):
            if self.get_next(iid) is None:
                return True
            if self.token == ';':
                if self.get_next(iid) is None:
                    return True
                return True
        elif self.func_decl_stmt(iid):
            return True
        return False

    def func_decl_stmt(self, parent):
        iid = self.creat_node('decl_stmt', parent)

        if self.func_val_decl(iid):
            return True
        elif self.func_func_decl(iid):
            return True
        return True

    def func_val_decl(self, parent):
        iid = self.creat_node('val_decl', parent)

        if self.func_const_decl(iid):
            return True
        elif self.func_var_decl(iid):
            return True
        return False

    def func_const_decl(self, parent):
        iid = self.creat_node('const_decl', parent)

        if self.token == 'const':
            if self.get_next(iid) is None:
                return True
            if self.func_const_type(iid):
                if self.func_const_decl_table(iid):
                    return True
        return False

    def func_const_type(self, parent):
        iid = self.creat_node('const_type', parent)

        if self.token in ['int', 'char', 'float']:
            if self.get_next(iid) is None:
                return True
            return True
        return False

    def func_const_decl_table(self, parent):
        iid = self.creat_node('const_decl_table', parent)

        if self.is_var():
            if self.get_next(iid) is None:
                return True
            if self.token == '=':
                if self.get_next(iid) is None:
                    return True
                if self.is_const():
                    if self.get_next(iid) is None:
                        return True
                    if self.func_const_decl_table1(iid):
                        return True
        return False

    def func_var_decl(self, parent):
        iid = self.creat_node('var_decl', parent)

        if self.func_var_type(iid):
            if self.func_var_decl_table(iid):
                return True
        return False

    def func_var_type(self, parent):
        iid = self.creat_node('var_type', parent)

        if self.token in ['int', 'char', 'float']:
            if self.get_next(iid) is None:
                return True
            return True
        return False

    def func_var_decl_table(self, parent):
        iid = self.creat_node('var_decl_table', parent)

        if self.func_sin_var_decl(iid):
            if self.func_var_decl_table1(iid):
                return True
        return False

    def func_sin_var_decl(self, parent):
        iid = self.creat_node('sin_var_decl', parent)

        if self.is_var():
            if self.get_next(iid) is None:
                return True
            if self.func_sin_var_decl1(iid):
                return True
        return False

    def func_func_decl(self, parent):
        iid = self.creat_node('func_decl', parent)

        if self.func_func_type(iid):
            if self.is_var():
                if self.get_next(iid) is None:
                    return True
                if self.token == '(':
                    if self.get_next(iid) is None:
                        return True
                    if self.func_func_decl_formal_para_list(iid):
                        if self.token == ')':
                            if self.get_next(iid) is None:
                                return True
                            if self.token == ';':
                                if self.get_next(iid) is None:
                                    return True
                                return True
        return False

    def func_func_type(self, parent):
        iid = self.creat_node('func_type', parent)

        if self.token in ['int', 'char', 'float', 'void']:
            if self.get_next(iid) is None:
                return True
            return True
        return False

    def func_func_decl_formal_para_list(self, parent):
        iid = self.creat_node('func_decl_formal_para_list', parent)

        if self.func_func_decl_para(iid):
            return True
        return True

    def func_func_decl_para(self, parent):
        iid = self.creat_node('func_decl_para', parent)

        if self.token == 'int':
            if self.get_next(iid) is None:
                return True
            if self.func_func_decl_para1(iid):
                return True
        elif self.token == 'char':
            if self.get_next(iid) is None:
                return True
            if self.func_func_decl_para1(iid):
                return True
        elif self.token == 'float':
            if self.get_next(iid) is None:
                return True
            if self.func_func_decl_para1(iid):
                return True
        return False

    def func_const_decl_table1(self, parent):
        iid = self.creat_node('const_decl_table1', parent)

        if self.token == ';':
            if self.get_next(iid) is None:
                return True
            return True
        elif self.token == ',':
            if self.get_next(iid) is None:
                return True
            if self.func_const_decl_table(iid):
                return True
        return False

    def func_var_decl_table1(self, parent):
        iid = self.creat_node('var_decl_table1', parent)

        if self.token == ';':
            if self.get_next(iid) is None:
                return True
            return True
        elif self.token == ',':
            if self.get_next(iid) is None:
                return True
            if self.func_var_decl_table(iid):
                return True
        return False

    def func_sin_var_decl1(self, parent):
        iid = self.creat_node('sin_var_decl1', parent)

        if self.token == '=':
            if self.get_next(iid) is None:
                return True
            if self.is_expr(iid):
                if self.get_next(iid) is None:
                    return True
                return True
        return True

    def func_func_decl_para1(self, parent):
        iid = self.creat_node('func_decl_para1', parent)

        if self.token == ',':
            if self.get_next(iid) is None:
                return True
            if self.func_func_decl_para(iid):
                return True
        return True

    def is_var(self):
        return self.token.isidentifier()

    def is_const(self):
        return self.token.isdigit()

    def is_exec_stmt(self):
        # TODO
        return True

    def is_g_expr(self, iid):
        self.i = 0
        handler = Match_g_expr()
        handler.set_tokenList(self.arr[self.i:])
        res, i, subtree = handler.run(False)
        self.i += i
        self.tree.paste(iid, subtree)
        return res

    def is_expr(self, iid):
        handler = Match_expr()
        handler.set_tokenList(self.arr[self.i:])
        res, i, subtree = handler.run(False)
        self.i += i
        self.tree.paste(iid, subtree)
        return res


def main():
    handler = Match_base_stmt()
    s = [
        ['int', 'i', ',', 'j', ';'],
        ['int', 'i', '=', '1', ';'],
        ['int', 'i', '=', '1', ',', 'j', '=', '1', ';'],
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
