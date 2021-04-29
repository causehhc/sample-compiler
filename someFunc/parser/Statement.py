from Expression import Match_expr, Match_g_expr
from Match_base import Match_base


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

        self.i = 0
        self.token = self.arr[self.i]
        self.anls.clear()
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

    def run_export_decl_stmt(self, flag):
        self.res = self.func_decl_stmt('root')
        if self.res is True:
            if len(self.arr) > len(self.anls):
                self.error(2, 'unmatched characters')
                if flag:
                    self.res = False
        if self.i == 0:
            self.i += 1
        return self.res, self.i - 1, self.tree


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
    <循环语句> -> <声明语句> | <循环执行语句> | <循环用复合语句>
    <循环用复合语句> -> { <循环语句表> }
    <循环语句表> -> <循环语句> | <循环语句> <循环语句表>
    <循环执行语句> -> <循环用if语句> | <for语句> | <while语句> | <do while语句> | <return语句> | <break语句> | <continue语句>
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
    do_while_stmt -> do comp_stmt_for_loops while ( expr ) ;
    loop_stmt -> decl_stmt | loop_exec_stmt | comp_stmt_for_loops
    comp_stmt_for_loops -> { list_of_loop_stmt }
    list_of_loop_stmt -> loop_stmt | loop_stmt list_of_loop_stmt
    loop_exec_stmt -> if_stmt_for_loop | for_stmt | while_stmt | do_while_stmt | return_stmt | break_stmt | continue_stmt
    if_stmt_for_loop -> if ( expr ) loop_stmt | if ( expr ) loop_stmt else loop_stmt
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
          do_while_stmt -> do comp_stmt_for_loops while ( expr ) ;
              loop_stmt -> decl_stmt
                         | loop_exec_stmt
                         | comp_stmt_for_loops
    comp_stmt_for_loops -> { list_of_loop_stmt }
      list_of_loop_stmt -> decl_stmt list_of_loop_stmt'
                         | loop_exec_stmt list_of_loop_stmt'
                         | { list_of_loop_stmt } list_of_loop_stmt'
         loop_exec_stmt -> if_stmt_for_loop
                         | for ( expr ; expr ; expr ) loop_stmt
                         | while ( expr ) loop_stmt
                         | do comp_stmt_for_loops while ( expr ) ;
                         | return_stmt
                         | break_stmt
                         | continue_stmt
       if_stmt_for_loop -> if ( expr ) loop_stmt if_stmt_for_loop'
            return_stmt -> return return_stmt'
             break_stmt -> break ;
          continue_stmt -> continue ;
             stmt_list' -> ϵ
                         | stmt stmt_list'
               if_stmt' -> ϵ
                         | else stmt
     list_of_loop_stmt' -> ϵ
                         | decl_stmt list_of_loop_stmt'
                         | if ( expr ) loop_stmt if_stmt_for_loop' list_of_loop_stmt'
                         | for ( expr ; expr ; expr ) loop_stmt list_of_loop_stmt'
                         | while ( expr ) loop_stmt list_of_loop_stmt'
                         | do comp_stmt_for_loops while ( expr ) ; list_of_loop_stmt'
                         | return return_stmt' list_of_loop_stmt'
                         | break ; list_of_loop_stmt'
                         | continue ; list_of_loop_stmt'
                         | { list_of_loop_stmt } list_of_loop_stmt'
      if_stmt_for_loop' -> ϵ
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

        self.i = 0
        self.token = self.arr[self.i]
        self.anls.clear()
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
            # if self.get_next(iid) is None:
            #     return True
            return True
        elif self.func_for_stmt(iid):
            # if self.get_next(iid) is None:
            #     return True
            return True
        elif self.func_while_stmt(iid):
            # if self.get_next(iid) is None:
            #     return True
            return True
        elif self.func_do_while_stmt(iid):
            # if self.get_next(iid) is None:
            #     return True
            return True
        elif self.func_return_stmt(iid):
            # if self.get_next(iid) is None:
            #     return True
            return True

        self.i = 0
        self.token = self.arr[self.i]
        self.anls.clear()
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

        self.i = 0
        self.token = self.arr[self.i]
        self.anls.clear()
        return False

    def func_stmt_list(self, parent):
        iid = self.creat_node('stmt_list', parent)

        if self.is_stmt(iid):
            if self.get_next(iid) is None:
                return True
            if self.func_stmt_list1(iid):
                # if self.get_next(iid) is None:
                #     return True
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
                                # if self.get_next(iid) is None:
                                #     return True
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
                                            # if self.get_next(iid) is None:
                                            #     return True
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
            if self.func_comp_stmt_for_loops(iid):
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
            # if self.get_next(iid) is None:
            #     return True
            return True
        elif self.func_comp_stmt_for_loops(iid):
            # if self.get_next(iid) is None:
            #     return True
            return True
        return False

    def func_comp_stmt_for_loops(self, parent):
        iid = self.creat_node('comp_stmt_for_loops', parent)

        if self.token == '{':
            if self.get_next(iid) is None:
                return True
            if self.func_list_of_loop_stmt(iid):
                if self.token == '}':
                    if self.get_next(iid) is None:
                        return True
                    return True
        return False

    def func_list_of_loop_stmt(self, parent):
        iid = self.creat_node('list_of_loop_stmt', parent)

        if self.is_decl_stmt(iid):
            if self.get_next(iid) is None:
                return True
            if self.func_list_of_loop_stmt1(iid):
                # if self.get_next(iid) is None:
                #     return True
                return True
        elif self.func_loop_exec_stmt(iid):
            # if self.get_next(iid) is None:
            #     return True
            if self.func_list_of_loop_stmt1(iid):
                # if self.get_next(iid) is None:
                #     return True
                return True
        elif self.token == '{':
            if self.get_next(iid) is None:
                return True
            if self.func_list_of_loop_stmt(iid):
                if self.token == '}':
                    if self.get_next(iid) is None:
                        return True
                    if self.func_list_of_loop_stmt1(iid):
                        # if self.get_next(iid) is None:
                        #     return True
                        return True
        return False

    def func_loop_exec_stmt(self, parent):
        iid = self.creat_node('loop_exec_stmt', parent)

        if self.func_if_stmt_for_loop(iid):
            # if self.get_next(iid) is None:
            #     return True
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
                                            # if self.get_next(iid) is None:
                                            #     return True
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
                            # if self.get_next(iid) is None:
                            #     return True
                            return True
        elif self.token == 'do':
            if self.get_next(iid) is None:
                return True
            if self.func_comp_stmt_for_loops(iid):
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
            # if self.get_next(iid) is None:
            #     return True
            return True
        elif self.func_break_stmt(iid):
            # if self.get_next(iid) is None:
            #     return True
            return True
        elif self.func_continue_stmt(iid):
            # if self.get_next(iid) is None:
            #     return True
            return True
        return False

    def func_if_stmt_for_loop(self, parent):
        iid = self.creat_node('if_stmt_for_loop', parent)

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
                            if self.func_if_stmt_for_loop1(iid):
                                # if self.get_next(iid) is None:
                                #     return True
                                return True
        return False

    def func_return_stmt(self, parent):
        iid = self.creat_node('return_stmt', parent)

        if self.token == 'return':
            if self.get_next(iid) is None:
                return True
            if self.func_return_stmt1(iid):
                # if self.get_next(iid) is None:
                #     return True
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
                # if self.get_next(iid) is None:
                #     return True
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

    def func_list_of_loop_stmt1(self, parent):
        iid = self.creat_node('list_of_loop_stmt1', parent)

        if self.is_decl_stmt(iid):
            if self.get_next(iid) is None:
                return True
            if self.func_list_of_loop_stmt1(iid):
                # if self.get_next(iid) is None:
                #     return True
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
                            if self.func_if_stmt_for_loop1(iid):
                                if self.func_list_of_loop_stmt1(iid):
                                    # if self.get_next(iid) is None:
                                    #     return True
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
                                            if self.func_list_of_loop_stmt1(iid):
                                                # if self.get_next(iid) is None:
                                                #     return True
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
                            if self.func_list_of_loop_stmt1(iid):
                                # if self.get_next(iid) is None:
                                #     return True
                                return True
        elif self.token == 'do':
            if self.get_next(iid) is None:
                return True
            if self.func_comp_stmt_for_loops(iid):
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
                                    if self.func_list_of_loop_stmt1(iid):
                                        # if self.get_next(iid) is None:
                                        #     return True
                                        return True
        elif self.token == 'return':
            if self.get_next(iid) is None:
                return True
            if self.func_return_stmt1(iid):
                if self.func_list_of_loop_stmt1(iid):
                    # if self.get_next(iid) is None:
                    #     return True
                    return True
        elif self.token == 'break':
            if self.get_next(iid) is None:
                return True
            if self.token == ';':
                if self.get_next(iid) is None:
                    return True
                if self.func_list_of_loop_stmt1(iid):
                    # if self.get_next(iid) is None:
                    #     return True
                    return True
        elif self.token == 'continue':
            if self.get_next(iid) is None:
                return True
            if self.token == ';':
                if self.get_next(iid) is None:
                    return True
                if self.func_list_of_loop_stmt1(iid):
                    # if self.get_next(iid) is None:
                    #     return True
                    return True
        elif self.token == '{':
            if self.get_next(iid) is None:
                return True
            if self.func_list_of_loop_stmt(iid):
                if self.token == '}':
                    if self.get_next(iid) is None:
                        return True
                    if self.func_list_of_loop_stmt1(iid):
                        # if self.get_next(iid) is None:
                        #     return True
                        return True
        return True

    def func_if_stmt_for_loop1(self, parent):
        iid = self.creat_node('if_stmt_for_loop1', parent)

        if self.token == 'else':
            if self.get_next(iid) is None:
                return True
            if self.func_loop_stmt(iid):
                # if self.get_next(iid) is None:
                #     return True
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
        self.i = 0
        handler = Match_g_expr()
        res = False
        if self.i < len(self.arr):
            handler.set_tokenList(self.arr[self.i:])
            res, i, subtree = handler.run(False)
            self.i += i
            self.tree.paste(iid, subtree)
        return res

    def is_func_call(self, iid):
        # TODO a_expr
        return True

    def is_stmt(self, iid):
        handler = Match_base_stmt()
        res = False
        if self.i < len(self.arr):
            handler.set_tokenList(self.arr[self.i:])
            res, i, subtree = handler.run(False)
            self.i += i
            self.tree.paste(iid, subtree)
        return res

    def is_expr(self, iid):
        handler = Match_expr()
        res = False
        if self.i < len(self.arr):
            handler.set_tokenList(self.arr[self.i:])
            res, i, subtree = handler.run(False)
            self.i += i
            self.tree.paste(iid, subtree)
        return res

    def is_decl_stmt(self, iid):
        handler = Match_base_stmt()
        res = False
        if self.i < len(self.arr):
            handler.set_tokenList(self.arr[self.i:])
            # TODO 疑似<声明语句>应该为<语句>，书上错了
            # res, i, subtree = handler.run_export_decl_stmt(False)
            res, i, subtree = handler.run(False)
            self.i += i
            self.tree.paste(iid, subtree)
        return res

    def run_export_comp_stmt(self, flag):
        self.res = self.func_comp_stmt('root')
        if self.res is True:
            if len(self.arr) > len(self.anls):
                self.error(2, 'unmatched characters')
                if flag:
                    self.res = False
        if self.i == 0:
            self.i += 1
        return self.res, self.i - 1, self.tree


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
            # if self.get_next(iid) is None:
            #     return True
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
                    # if self.get_next(iid) is None:
                    #     return True
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
        if self.i < len(self.arr):
            handler.set_tokenList(self.arr[self.i:])
            res, i, subtree = handler.run(False)
            self.i += i
            self.tree.paste(iid, subtree)
        return res

    def is_var_type(self, iid):
        if self.token in ['int', 'char', 'float']:
            return True
        return False


class Match_program_stmt(Match_base):
    """
    <程序> -> <声明语句块> main() <复合语句> <函数块>
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
        handler.set_tokenList(self.arr[self.i:])
        res, i, subtree = handler.run_export_comp_stmt(False)
        self.i += i
        self.tree.paste(iid, subtree)
        return res

    def is_decl_stmt(self, iid):
        handler = Match_base_stmt()
        res = False
        if self.i < len(self.arr):
            handler.set_tokenList(self.arr[self.i:])
            res, i, subtree = handler.run(False)
            self.i += i
            self.tree.paste(iid, subtree)
        return res

    def is_func_def(self, iid):
        handler = Match_func_stmt()
        res = False
        if self.i < len(self.arr):
            handler.set_tokenList(self.arr[self.i:])
            res, i, subtree = handler.run(False)
            self.i += i
            self.tree.paste(iid, subtree)
        return res


def main_base():
    handler = Match_base_stmt()
    s = [
        # 'int i = 0 ;',
        # 'int i = 1 , j = 1 ;',
        # 'const int j = 0 ;',
        # 'int i = 1',
        # 'int i , j ; }',
        # '{ int i = 0 ; }',
        # '{ int i = 0 ; int j = 0 ; }',
        'int test_func ( int ) ;',
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


def main_exec():
    handler = Match_exec_stmt()
    s = [
        # 'if ( i < 10 ) i = i + 1 ; else const int j = 0 ;',
        # 'if ( i < 10 ) { i = i + 1 ; } else { const int j = 0 ; const int j = 0 ; }',
        # 'if ( i < 10 ) { i = i + 1 ; } else { if ( i < 10 ) i = i + 1 ; else const int j = 0 ; }',
        # 'for ( i = 0 ; i < 10 ; i + 1 ) { int j = 0 ; }',
        'for ( i = 0 ; i < 10 ; i + 1 ) { if ( i < 10 ) i = i + 1 ; else { const int j = 0 ; break ; } }',
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


def main_func():
    handler = Match_func_stmt()
    s = [
        'int test_func ( int para ) { int i = 0 ; return 0 ; }',
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


def main_program():
    handler = Match_program_stmt()
    s = [
        'int a = 1 ; '
        'int test_func ( int ) ; '
        'int main ( ) { '
        '  int i = 0 , j = 0 ; '
        '  if ( i == 0 ) { '
        '    while ( 1 ) { '
        '      i = 1 ; '
        '    } '
        '  } '
        '  for ( i = 0 ; i < 10 ; i = i + 1 ) { '
        '    for ( j = 0 ; j < 10 ; j = j + 1 ) { '
        '      j = j + 1 ; '
        '    } '
        '    if ( i < 10 ) { '
        '      i = i + 1 ; '
        '      if ( j > 5 ) { '
        '        j = j + 2 ; '
        '      } '
        '    } '
        '    else { '
        '      const int j = 0 ; '
        '      break ; '
        '    } '
        '  } '
        '  return 0 ; '
        '} '
        'int test_func ( int para ) { '
        '  int i = 0 ; '
        '  return 0 ; '
        '} ',
    ]
    for item in s:
        print('Detected string: ', item)
        temp = item.split(' ')
        # print(temp)
        while '' in temp:
            temp.remove('')
        print(temp)
        handler.set_tokenList(temp)
        res, idx, tree = handler.run(True)
        print('Compliance with the rules: ', res)
        if res is False:
            print('error info:', handler.info)
            print('error idx:', idx + 1)
        # handler.tree.show()
        print()


if __name__ == '__main__':
    print('hello world')
    # main_base()
    # main_exec()
    # main_func()
    main_program()
