from someFunc.lexical.Automata import Lex_analyzer
from someFunc.parser_re.Match_base import Match_base
from someFunc.parser_re.Expression import Match_expr, Match_g_expr, Match_a_expr


class Match_base_stmt(Match_base):
    """
    <语句> -> <声明语句> | <执行语句>
    <声明语句> -> <值声明> | <函数声明> | ϵ
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
    <函数声明形参列表> -> <函数声明形参> | ϵ
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

    """
    def __init__(self):
        super().__init__()

    def func_main(self, parent):
        iid = self.creat_node('stmt', parent)

        if self.is_exec_stmt(iid):
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
        return False

    def func_val_decl(self, parent):
        iid = self.creat_node('val_decl', parent)

        if self.func_const_decl(iid):
            return True
        elif self.func_var_decl(iid):
            return True

        self.reset_token()
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

    def is_exec_stmt(self, iid):
        handler = Match_exec_stmt()
        handler.set_tokenList(self.token_list[self.index:])
        res, i, subtree, _ = handler.run(False)
        self.index += i
        self.tree.paste(iid, subtree)
        return res

    def is_expr(self, iid):
        handler = Match_expr()
        handler.set_tokenList(self.token_list[self.index:])
        res, i, subtree, _ = handler.run(False)
        self.index += i
        self.tree.paste(iid, subtree)
        return res

    def run_export_decl_stmt(self, flag):
        self.res = self.func_decl_stmt('root')
        if self.res is True:
            if len(self.token_list) > len(self.anls_proc):
                self.info = 'error: {}, token: {}, row: {}, col: {}\n'.format('unmatched char',
                                                                              self.token_node.val,
                                                                              self.token_node.row,
                                                                              self.token_node.col)
                if flag:
                    self.res = False
        if self.index == 0:
            self.index += 1
        return self.res, self.index - 1, self.tree, self.info


class Match_exec_stmt(Match_base):
    """
    <执行语句> -> <数据处理语句> | <控制语句> | <复合语句>
    <数据处理语句> -> <赋值语句> | <函数调用语句>
    <赋值语句> -> <赋值表达式> ;
    <函数调用语句> -> <函数调用> ;
    <控制语句> -> <if语句> | <for语句> | <while语句> | <do while语句> | <return语句>
    <复合语句> -> { <语句表> }
    <语句表> -> <语句> | <语句> <语句表>
    <if语句> -> if ( <表达式> ) <语句> | if ( <表达式> ) <语句> else <语句>
    <for语句> -> for ( <表达式> ; <表达式> ; <表达式> ) <循环语句>
    <while语句> -> while ( <表达式> ) <循环语句>
    <do while语句> -> do <循环用复合语句> while ( <表达式> ) ;
    <循环语句> -> <声明语句> | <循环执行语句>
    <循环执行语句> -> <数据处理语句> | <循环控制语句> | <循环用复合语句>
    <循环用复合语句> -> { <循环语句表> }
    <循环语句表> -> <循环语句> | <循环语句> <循环语句表>
    <循环控制语句> -> <循环用if语句> | <for语句> | <while语句> | <do while语句> | <return语句> | <break语句> | <continue语句>
    <循环用if语句> -> if ( <表达式> ) <循环语句> | if ( <表达式> ) <循环语句> else <循环语句>
    <return语句> -> return ; | return <表达式> ;
    <break语句> -> break ;
    <continue语句> -> continue ;
    =============================================================
    exec_stmt -> data_proc_stmt | ctrl_stmt | comp_stmt
    data_proc_stmt -> give_stmt | func_call_stmt
    give_stmt -> give_expr ;
    func_call_stmt -> func_call ;
    ctrl_stmt -> if_stmt | for_stmt | while_stmt | do_while_stmt | return_stmt
    comp_stmt -> { stmt_list }
    stmt_list -> stmt | stmt stmt_list
    if_stmt -> if ( expr ) stmt | if ( expr ) stmt else stmt
    for_stmt -> for ( expr ; expr ; expr ) loop_stmt
    while_stmt -> while ( expr ) loop_stmt
    do_while_stmt -> do loop_comp_stmt while ( expr ) ;
    loop_stmt -> decl_stmt | loop_exec_stmt
    loop_exec_stmt -> data_proc_stmt | loop_ctrl_stmt | loop_comp_stmt
    loop_comp_stmt -> { loop_stmt_list }
    loop_stmt_list -> loop_stmt | loop_stmt loop_stmt_list
    loop_ctrl_stmt -> loop_if_stmt | for_stmt | while_stmt | do_while_stmt | return_stmt | break_stmt | continue_stmt
    loop_if_stmt -> if ( expr ) loop_stmt | if ( expr ) loop_stmt else loop_stmt
    return_stmt -> return ; | return expr ;
    break_stmt -> break ;
    continue_stmt -> continue ;
    =============================================================
          exec_stmt -> data_proc_stmt
                     | ctrl_stmt
                     | comp_stmt
     data_proc_stmt -> give_stmt
                     | func_call_stmt
          give_stmt -> give_expr ;
     func_call_stmt -> func_call ;
          ctrl_stmt -> if_stmt
                     | for_stmt
                     | while_stmt
                     | do_while_stmt
                     | return_stmt
          comp_stmt -> { stmt_list }
          stmt_list -> stmt stmt_list'
            if_stmt -> if ( expr ) stmt if_stmt'
           for_stmt -> for ( expr ; expr ; expr ) loop_stmt
         while_stmt -> while ( expr ) loop_stmt
      do_while_stmt -> do loop_comp_stmt while ( expr ) ;
          loop_stmt -> decl_stmt
                     | loop_exec_stmt
     loop_exec_stmt -> give_expr ;
                     | func_call ;
                     | loop_ctrl_stmt
                     | loop_comp_stmt
     loop_comp_stmt -> { loop_stmt_list }
     loop_stmt_list -> decl_stmt loop_stmt_list'
                     | give_expr ; loop_stmt_list'
                     | func_call ; loop_stmt_list'
                     | loop_ctrl_stmt loop_stmt_list'
                     | { loop_stmt_list } loop_stmt_list'
     loop_ctrl_stmt -> loop_if_stmt
                     | for ( expr ; expr ; expr ) loop_stmt
                     | while ( expr ) loop_stmt
                     | do loop_comp_stmt while ( expr ) ;
                     | return_stmt
                     | break_stmt
                     | continue_stmt
       loop_if_stmt -> if ( expr ) loop_stmt loop_if_stmt'
        return_stmt -> return return_stmt'
         break_stmt -> break ;
      continue_stmt -> continue ;
         stmt_list' -> ϵ
                     | stmt stmt_list'
           if_stmt' -> ϵ
                     | else stmt
    loop_stmt_list' -> ϵ
                     | decl_stmt loop_stmt_list'
                     | give_expr ; loop_stmt_list'
                     | func_call ; loop_stmt_list'
                     | if ( expr ) loop_stmt loop_if_stmt' loop_stmt_list'
                     | for ( expr ; expr ; expr ) loop_stmt loop_stmt_list'
                     | while ( expr ) loop_stmt loop_stmt_list'
                     | do loop_comp_stmt while ( expr ) ; loop_stmt_list'
                     | return return_stmt' loop_stmt_list'
                     | break ; loop_stmt_list'
                     | continue ; loop_stmt_list'
                     | { loop_stmt_list } loop_stmt_list'
      loop_if_stmt' -> ϵ
                     | else loop_stmt
       return_stmt' -> ;
                     | expr ;

    """
    def __init__(self):
        super().__init__()

    def func_main(self, parent):
        iid = self.creat_node('exec_stmt', parent)

        if self.func_data_proc_stmt(iid):
            return True
        elif self.func_ctrl_stmt(iid):
            return True
        elif self.func_comp_stmt(iid):
            return True
        return False

    def func_data_proc_stmt(self, parent):
        iid = self.creat_node('data_proc_stmt', parent)

        if self.func_give_stmt(iid):
            return True
        elif self.func_func_call_stmt(iid):
            return True

        self.reset_token()
        return False

    def func_give_stmt(self, parent):
        iid = self.creat_node('give_stmt', parent)

        if self.is_g_expr(iid):
            if self.get_next(iid) is None:
                return True
            if self.token == ';':
                if self.get_next(iid) is None:
                    return True
                return True
        return False

    def func_func_call_stmt(self, parent):
        iid = self.creat_node('func_call_stmt', parent)

        if self.is_func_call(iid):
            if self.get_next(iid) is None:
                return True
            if self.token == ';':
                if self.get_next(iid) is None:
                    return True
                return True
        return False

    def func_ctrl_stmt(self, parent):
        iid = self.creat_node('ctrl_stmt', parent)

        if self.func_if_stmt(iid):
            return True
        elif self.func_for_stmt(iid):
            return True
        elif self.func_while_stmt(iid):
            return True
        elif self.func_do_while_stmt(iid):
            return True
        elif self.func_return_stmt(iid):
            return True

        self.reset_token()
        return False

    def func_comp_stmt(self, parent):
        iid = self.creat_node('comp_stmt', parent)

        if self.token == '{':
            if self.get_next(iid) is None:
                return True
            if self.func_stmt_list(iid):
                if self.token == '}':
                    if self.get_next(iid) is None:
                        return True
                    return True

        self.reset_token()
        return False

    def func_stmt_list(self, parent):
        iid = self.creat_node('stmt_list', parent)

        if self.is_stmt(iid):
            if self.get_next(iid) is None:
                return True
            if self.func_stmt_list1(iid):
                return True
        return False

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
                        if self.is_stmt(iid):
                            if self.get_next(iid) is None:
                                return True
                            if self.func_if_stmt1(iid):
                                return True
        return False

    def func_for_stmt(self, parent):
        iid = self.creat_node('for_stmt', parent)

        if self.token == 'for':
            if self.get_next(iid) is None:
                return True
            if self.token == '(':
                if self.get_next(iid) is None:
                    return True
                if self.is_expr(iid):
                    if self.get_next(iid) is None:
                        return True
                    if self.token == ';':
                        if self.get_next(iid) is None:
                            return True
                        if self.is_expr(iid):
                            if self.get_next(iid) is None:
                                return True
                            if self.token == ';':
                                if self.get_next(iid) is None:
                                    return True
                                if self.is_expr(iid):
                                    if self.get_next(iid) is None:
                                        return True
                                    if self.token == ')':
                                        if self.get_next(iid) is None:
                                            return True
                                        if self.func_loop_stmt(iid):
                                            return True
        return False

    def func_while_stmt(self, parent):
        iid = self.creat_node('while_stmt', parent)

        if self.token == 'while':
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
                        if self.func_loop_stmt(iid):
                            # if self.get_next(iid) is None:
                            #     return True
                            return True
        return False

    def func_do_while_stmt(self, parent):
        iid = self.creat_node('do_while_stmt', parent)

        if self.token == 'do':
            if self.get_next(iid) is None:
                return True
            if self.func_loop_comp_stmt(iid):
                if self.token == 'while':
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
                                if self.token == ';':
                                    if self.get_next(iid) is None:
                                        return True
                                    return True
        return False

    def func_loop_stmt(self, parent):
        iid = self.creat_node('loop_stmt', parent)

        if self.is_decl_stmt(iid):
            if self.get_next(iid) is None:
                return True
            return True
        elif self.func_loop_exec_stmt(iid):
            return True
        return False

    def func_loop_exec_stmt(self, parent):
        iid = self.creat_node('loop_exec_stmt', parent)

        if self.is_g_expr(iid):
            if self.get_next(iid) is None:
                return True
            if self.token == ';':
                if self.get_next(iid) is None:
                    return True
                return True
        elif self.is_func_call(iid):
            if self.get_next(iid) is None:
                return True
            if self.token == ';':
                if self.get_next(iid) is None:
                    return True
                return True
        elif self.func_loop_ctrl_stmt(iid):
            return True
        elif self.func_loop_comp_stmt(iid):
            return True
        return False

    def func_loop_comp_stmt(self, parent):
        iid = self.creat_node('loop_comp_stmt', parent)

        if self.token == '{':
            if self.get_next(iid) is None:
                return True
            if self.func_loop_stmt_list(iid):
                if self.token == '}':
                    if self.get_next(iid) is None:
                        return True
                    return True
        return False

    def func_loop_stmt_list(self, parent):
        iid = self.creat_node('loop_stmt_list', parent)

        if self.is_decl_stmt(iid):
            if self.get_next(iid) is None:
                return True
            if self.loop_stmt_list1(iid):
                return True
        elif self.is_g_expr(iid):
            if self.get_next(iid) is None:
                return True
            if self.token == ';':
                if self.get_next(iid) is None:
                    return True
                if self.loop_stmt_list1(iid):
                    return True
        elif self.is_func_call(iid):
            if self.get_next(iid) is None:
                return True
            if self.token == ';':
                if self.get_next(iid) is None:
                    return True
                if self.loop_stmt_list1(iid):
                    return True
        elif self.func_loop_ctrl_stmt(iid):
            if self.loop_stmt_list1(iid):
                return True
        elif self.token == '{':
            if self.get_next(iid) is None:
                return True
            if self.func_loop_stmt_list(iid):
                if self.token == '}':
                    if self.get_next(iid) is None:
                        return True
                    if self.loop_stmt_list1(iid):
                        return True
        return False

    def func_loop_ctrl_stmt(self, parent):
        iid = self.creat_node('loop_ctrl_stmt', parent)

        if self.func_loop_if_stmt(iid):
            return True
        elif self.token == 'for':
            if self.get_next(iid) is None:
                return True
            if self.token == '(':
                if self.get_next(iid) is None:
                    return True
                if self.is_expr(iid):
                    if self.get_next(iid) is None:
                        return True
                    if self.token == ';':
                        if self.get_next(iid) is None:
                            return True
                        if self.is_expr(iid):
                            if self.get_next(iid) is None:
                                return True
                            if self.token == ';':
                                if self.get_next(iid) is None:
                                    return True
                                if self.is_expr(iid):
                                    if self.get_next(iid) is None:
                                        return True
                                    if self.token == ')':
                                        if self.get_next(iid) is None:
                                            return True
                                        if self.func_loop_stmt(iid):
                                            return True
        elif self.token == 'while':
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
                        if self.func_loop_stmt(iid):
                            return True
        elif self.token == 'do':
            if self.get_next(iid) is None:
                return True
            if self.func_loop_comp_stmt(iid):
                if self.token == 'while':
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
                                if self.token == ';':
                                    if self.get_next(iid) is None:
                                        return True
                                    return True
        elif self.func_return_stmt(iid):
            return True
        elif self.func_break_stmt(iid):
            return True
        elif self.func_continue_stmt(iid):
            return True
        return False

    def func_loop_if_stmt(self, parent):
        iid = self.creat_node('loop_if_stmt', parent)

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
                        if self.func_loop_stmt(iid):
                            if self.func_loop_if_stmt1(iid):
                                return True
        return False

    def func_return_stmt(self, parent):
        iid = self.creat_node('return_stmt', parent)

        if self.token == 'return':
            if self.get_next(iid) is None:
                return True
            if self.func_return_stmt1(iid):
                return True
        return False

    def func_break_stmt(self, parent):
        iid = self.creat_node('break_stmt', parent)

        if self.token == 'break':
            if self.get_next(iid) is None:
                return True
            if self.token == ';':
                if self.get_next(iid) is None:
                    return True
                return True
        return False

    def func_continue_stmt(self, parent):
        iid = self.creat_node('continue_stmt', parent)

        if self.token == 'continue':
            if self.get_next(iid) is None:
                return True
            if self.token == ';':
                if self.get_next(iid) is None:
                    return True
                return True
        return False

    def func_stmt_list1(self, parent):
        iid = self.creat_node('stmt_list1', parent)

        if self.is_stmt(iid):
            if self.get_next(iid) is None:
                return True
            if self.func_stmt_list1(iid):
                return True
        return True

    def func_if_stmt1(self, parent):
        iid = self.creat_node('if_stmt1', parent)

        if self.token == 'else':
            if self.get_next(iid) is None:
                return True
            if self.is_stmt(iid):
                if self.get_next(iid) is None:
                    return True
                return True
        return True

    def loop_stmt_list1(self, parent):
        iid = self.creat_node('list_of_loop_stmt1', parent)

        if self.is_decl_stmt(iid):
            if self.get_next(iid) is None:
                return True
            if self.loop_stmt_list1(iid):
                return True
        elif self.is_g_expr(iid):
            if self.get_next(iid) is None:
                return True
            if self.token == ';':
                if self.get_next(iid) is None:
                    return True
                if self.loop_stmt_list1(iid):
                    return True
        elif self.is_func_call(iid):
            if self.get_next(iid) is None:
                return True
            if self.token == ';':
                if self.get_next(iid) is None:
                    return True
                if self.loop_stmt_list1(iid):
                    return True
        elif self.token == 'if':
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
                        if self.func_loop_stmt(iid):
                            if self.func_loop_if_stmt1(iid):
                                if self.loop_stmt_list1(iid):
                                    return True
        elif self.token == 'for':
            if self.get_next(iid) is None:
                return True
            if self.token == '(':
                if self.get_next(iid) is None:
                    return True
                if self.is_expr(iid):
                    if self.get_next(iid) is None:
                        return True
                    if self.token == ';':
                        if self.get_next(iid) is None:
                            return True
                        if self.is_expr(iid):
                            if self.get_next(iid) is None:
                                return True
                            if self.token == ';':
                                if self.get_next(iid) is None:
                                    return True
                                if self.is_expr(iid):
                                    if self.get_next(iid) is None:
                                        return True
                                    if self.token == ')':
                                        if self.get_next(iid) is None:
                                            return True
                                        if self.func_loop_stmt(iid):
                                            if self.loop_stmt_list1(iid):
                                                return True
        elif self.token == 'while':
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
                        if self.func_loop_stmt(iid):
                            if self.loop_stmt_list1(iid):
                                return True
        elif self.token == 'do':
            if self.get_next(iid) is None:
                return True
            if self.func_loop_comp_stmt(iid):
                if self.token == 'while':
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
                                if self.token == ';':
                                    if self.loop_stmt_list1(iid):
                                        return True
        elif self.token == 'return':
            if self.get_next(iid) is None:
                return True
            if self.func_return_stmt1(iid):
                if self.loop_stmt_list1(iid):
                    return True
        elif self.token == 'break':
            if self.get_next(iid) is None:
                return True
            if self.token == ';':
                if self.get_next(iid) is None:
                    return True
                if self.loop_stmt_list1(iid):
                    return True
        elif self.token == 'continue':
            if self.get_next(iid) is None:
                return True
            if self.token == ';':
                if self.get_next(iid) is None:
                    return True
                if self.loop_stmt_list1(iid):
                    return True
        elif self.token == '{':
            if self.get_next(iid) is None:
                return True
            if self.func_loop_stmt_list(iid):
                if self.token == '}':
                    if self.get_next(iid) is None:
                        return True
                    if self.loop_stmt_list1(iid):
                        return True
        return True

    def func_loop_if_stmt1(self, parent):
        iid = self.creat_node('if_stmt_for_loop1', parent)

        if self.token == 'else':
            if self.get_next(iid) is None:
                return True
            if self.func_loop_stmt(iid):
                return True
        return True

    def func_return_stmt1(self, parent):
        iid = self.creat_node('return_stmt1', parent)

        if self.token == ';':
            if self.get_next(iid) is None:
                return True
            return True
        elif self.is_expr(iid):
            if self.get_next(iid) is None:
                return True
            if self.token == ';':
                if self.get_next(iid) is None:
                    return True
                return True
        return False

    def is_g_expr(self, iid):
        # self.index = 0
        handler = Match_g_expr()
        res = False
        if self.index < len(self.token_list):
            handler.set_tokenList(self.token_list[self.index:])
            res, i, subtree, _ = handler.run(False)
            self.index += i
            self.tree.paste(iid, subtree)
        return res

    def is_func_call(self, iid):
        handler = Match_a_expr()
        res = False
        if self.index < len(self.token_list):
            handler.set_tokenList(self.token_list[self.index:])
            res, i, subtree, _ = handler.run_export_func_call(False)
            self.index += i
            self.tree.paste(iid, subtree)
        return res

    def is_stmt(self, iid):
        handler = Match_base_stmt()
        res = False
        if self.index < len(self.token_list):
            handler.set_tokenList(self.token_list[self.index:])
            res, i, subtree, _ = handler.run(False)
            self.index += i
            self.tree.paste(iid, subtree)
        return res

    def is_expr(self, iid):
        handler = Match_expr()
        res = False
        if self.index < len(self.token_list):
            handler.set_tokenList(self.token_list[self.index:])
            res, i, subtree, _ = handler.run(False)
            self.index += i
            self.tree.paste(iid, subtree)
        return res

    def is_decl_stmt(self, iid):
        handler = Match_base_stmt()
        res = False
        if self.index < len(self.token_list):
            handler.set_tokenList(self.token_list[self.index:])
            # TODO 疑似<声明语句>应该为<语句>，书上错了
            res, i, subtree, _ = handler.run_export_decl_stmt(False)
            # res, i, subtree = handler.run(False)
            self.index += i
            self.tree.paste(iid, subtree)
        return res

    def run_export_comp_stmt(self, flag):
        self.res = self.func_comp_stmt('root')
        if self.res is True:
            if len(self.token_list) > len(self.anls_proc):
                self.info = 'error: {}, token: {}, row: {}, col: {}\n'.format('unmatched char',
                                                                              self.token_node.val,
                                                                              self.token_node.row,
                                                                              self.token_node.col)
                if flag:
                    self.res = False
        if self.index == 0:
            self.index += 1
        return self.res, self.index - 1, self.tree, self.info


class Match_func_stmt(Match_base):
    """
    <函数定义> -> <函数类型> <标识符> ( <函数定义形参列表> ) <复合语句>
    <函数定义形参列表> -> <函数定义形参> | ϵ
    <函数定义形参> -> <变量类型> <标识符> | <变量类型> <标识符> , <函数定义形参>
    =============================================================
    func_def -> func_type id ( func_def_para_list ) comp_stmt
    func_def_para_list -> func_def_para | ϵ
    func_def_para -> var_type id | var_type id , func_def_para
    =============================================================
              func_def -> func_type id ( func_def_para_list ) comp_stmt
    func_def_para_list -> func_def_para
                        | ϵ
         func_def_para -> var_type id func_def_para'
        func_def_para' -> ϵ
                        | , func_def_para

    """
    def __init__(self):
        super().__init__()

    def func_main(self, parent):
        iid = self.creat_node('func_def', parent)

        if self.is_func_type(iid):
            if self.get_next(iid) is None:
                return True
            if self.is_var():
                if self.get_next(iid) is None:
                    return True
                if self.token == '(':
                    if self.get_next(iid) is None:
                        return True
                    if self.func_func_def_para_list(iid):
                        if self.token == ')':
                            if self.get_next(iid) is None:
                                return True
                            if self.is_comp_stmt(iid):
                                if self.get_next(iid) is None:
                                    return True
                                return True
        return False

    def func_func_def_para_list(self, parent):
        iid = self.creat_node('func_def_para_list', parent)

        if self.func_func_def_para(iid):
            return True
        return True

    def func_func_def_para(self, parent):
        iid = self.creat_node('func_def_para', parent)

        if self.is_var_type(iid):
            if self.get_next(iid) is None:
                return True
            if self.is_var():
                if self.get_next(iid) is None:
                    return True
                if self.func_func_def_para1(iid):
                    return True
        return False

    def func_func_def_para1(self, parent):
        iid = self.creat_node('func_def_para1', parent)

        if self.token == ',':
            if self.get_next(iid) is None:
                return True
            if self.func_func_def_para(iid):
                return True
        return True

    def is_func_type(self, iid):
        if self.token in ['int', 'char', 'float']:
            return True
        return False

    def is_comp_stmt(self, iid):
        handler = Match_exec_stmt()
        res = False
        if self.index < len(self.token_list):
            handler.set_tokenList(self.token_list[self.index:])
            res, i, subtree, _ = handler.run(False)
            self.index += i
            self.tree.paste(iid, subtree)
        return res

    def is_var_type(self, iid):
        if self.token in ['int', 'char', 'float']:
            return True
        return False


class Match_program_stmt(Match_base):
    """
    <程序> -> <声明语句块> int main() <复合语句> <函数块>
    <声明语句块> -> <声明语句> <声明语句块> | ϵ
    <函数块> -> <函数定义> <函数块> | ϵ
    =============================================================
    program -> decl_stmt_block int main ( ) comp_stmt func_block
    decl_stmt_block -> decl_stmt decl_stmt_block | ϵ
    func_block -> func_def func_block | ϵ
    """
    def __init__(self):
        super().__init__()

    def func_main(self, parent):
        iid = self.creat_node('program', parent)

        if self.func_decl_stmt_block(iid):
            if self.token == 'int':
                if self.get_next(iid) is None:
                    return True
                if self.token == 'main':
                    if self.get_next(iid) is None:
                        return True
                    if self.token == '(':
                        if self.get_next(iid) is None:
                            return True
                        if self.token == ')':
                            if self.get_next(iid) is None:
                                return True
                            if self.is_comp_stmt(iid):
                                if self.get_next(iid) is None:
                                    return True
                                if self.func_func_block(iid):
                                    return True
        return False

    def func_decl_stmt_block(self, parent):
        iid = self.creat_node('decl_stmt_block', parent)

        if self.is_decl_stmt(iid):
            if self.get_next(iid) is None:
                return True
            if self.func_decl_stmt_block(iid):
                return True
        return True

    def func_func_block(self, parent):
        iid = self.creat_node('func_block', parent)

        if self.is_func_def(iid):
            if self.get_next(iid) is None:
                return True
            if self.func_func_block(iid):
                return True
        return True

    def is_comp_stmt(self, iid):
        handler = Match_exec_stmt()
        handler.set_tokenList(self.token_list[self.index:])
        res, i, subtree, _ = handler.run_export_comp_stmt(False)
        self.index += i
        self.tree.paste(iid, subtree)
        return res

    def is_decl_stmt(self, iid):
        handler = Match_base_stmt()
        res = False
        if self.index < len(self.token_list):
            handler.set_tokenList(self.token_list[self.index:])
            res, i, subtree, _ = handler.run(False)
            self.index += i
            self.tree.paste(iid, subtree)
        return res

    def is_func_def(self, iid):
        handler = Match_func_stmt()
        res = False
        if self.index < len(self.token_list):
            handler.set_tokenList(self.token_list[self.index:])
            res, i, subtree, _ = handler.run(False)
            self.index += i
            self.tree.paste(iid, subtree)
        return res


def main_base():
    handler = Match_base_stmt()
    s = [
        # 'int n = read ( 1 ) ;',
        # 'int i = 0 ;',
        # 'i = 0 ;'
        # 'int i = 1 , j = 1 ;',
        # 'const int j = 0 ;',
        # 'int i = 1',
        # 'int i , j ; }',
        # '{ int i = 0 ; }',
        '{ int i = 0 ; int j = 0 ; }',
        # 'int test_func ( int ) ;',
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


def main_exec():
    handler = Match_exec_stmt()
    s = [
        # 'break ; ',
        # 'if ( i < 10 ) i = i + 1 ; else const int j = 0 ; ',
        # 'if ( i < 10 ) { i = i + 1 ; } else { const int j = 0 ; const int j = 0 ; } ',
        # 'if ( i < 10 ) { i = i + 1 ; } else { if ( i < 10 ) i = i + 1 ; else const int j = 0 ; } ',
        # 'for ( i = 0 ; i < 10 ; i + 1 ) { int j = 0 ; } ',
        'for ( i = 0 ; i < 10 ; i + 1 ) { int j = 0 ; if ( i < 10 ) int i = i + 1 ; else { const int j = 0 ; break ; } } ',
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


def main_func():
    handler = Match_func_stmt()
    s = [
        'int test_func ( int para ) { int i = 0 ; return 0 ; }',
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


def main_program():
    handler = Match_program_stmt()
    s = [
        'int a = 1 ; '
        'int test_func ( int ) ; '
        'int main ( ) { '
        '  int i = 0 , j = 0 ; '
        '  int n = read ( 1 ) ;'
        '  return 0 ; '
        '} ',
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
    print('hello world')
    # main_base()
    # main_exec()
    # main_func()
    main_program()
