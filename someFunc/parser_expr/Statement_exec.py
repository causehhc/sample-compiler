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
from Match_base import Match_base
from Expression_all import Match_expr, Match_g_expr
from someFunc.parser_expr.Statement_base import Match_base_stmt


class Match_exec_stmt(Match_base):
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
            if self.get_next(iid) is None:
                return True
            return True
        elif self.func_for_stmt(iid):
            if self.get_next(iid) is None:
                return True
            return True
        elif self.func_while_stmt(iid):
            if self.get_next(iid) is None:
                return True
            return True
        elif self.func_do_while_stmt(iid):
            if self.get_next(iid) is None:
                return True
            return True
        elif self.func_return_stmt(iid):
            if self.get_next(iid) is None:
                return True
            return True
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
        return False

    def func_stmt_list(self, parent):
        iid = self.creat_node('stmt_list', parent)

        if self.is_stmt(iid):
            if self.get_next(iid) is None:
                return True
            if self.func_stmt_list1(iid):
                if self.get_next(iid) is None:
                    return True
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
                                if self.get_next(iid) is None:
                                    return True
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
                                            if self.get_next(iid) is None:
                                                return True
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
                            if self.get_next(iid) is None:
                                return True
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
            if self.get_next(iid) is None:
                return True
            return True
        elif self.func_loop_exec_stmt(iid):
            if self.get_next(iid) is None:
                return True
            return True
        elif self.func_comp_stmt_for_loops(iid):
            if self.get_next(iid) is None:
                return True
            return True
        return False

    def func_comp_stmt_for_loops(self, parent):
        iid = self.creat_node('comp_stmt_for_loops', parent)

        if self.token == '{':
            if self.get_next(iid) is None:
                return True
            if self.list_of_loop_stmt(iid):
                if self.token == '}':
                    if self.get_next(iid) is None:
                        return True
                    return True
        return False

    def list_of_loop_stmt(self, parent):
        iid = self.creat_node('list_of_loop_stmt', parent)

        if self.is_decl_stmt(iid):
            if self.get_next(iid) is None:
                return True
            if self.list_of_loop_stmt1(iid):
                if self.get_next(iid) is None:
                    return True
                return True
        elif self.func_loop_exec_stmt(iid):
            if self.get_next(iid) is None:
                return True
            if self.list_of_loop_stmt1(iid):
                if self.get_next(iid) is None:
                    return True
                return True
        elif self.token == '{':
            if self.get_next(iid) is None:
                return True
            if self.list_of_loop_stmt(iid):
                if self.token == '}':
                    if self.get_next(iid) is None:
                        return True
                    if self.list_of_loop_stmt1(iid):
                        if self.get_next(iid) is None:
                            return True
                        return True
        return False

    def func_loop_exec_stmt(self, parent):
        iid = self.creat_node('loop_exec_stmt', parent)

        if self.func_if_stmt_for_loop(iid):
            if self.get_next(iid) is None:
                return True
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
                                            if self.get_next(iid) is None:
                                                return True
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
                            if self.get_next(iid) is None:
                                return True
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
            if self.get_next(iid) is None:
                return True
            return True
        elif self.func_break_stmt(iid):
            if self.get_next(iid) is None:
                return True
            return True
        elif self.func_continue_stmt(iid):
            if self.get_next(iid) is None:
                return True
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
                                if self.get_next(iid) is None:
                                    return True
                                return True
        return False

    def func_return_stmt(self, parent):
        iid = self.creat_node('return_stmt', parent)

        if self.token == 'return':
            if self.get_next(iid) is None:
                return True
            if self.func_return_stmt1(iid):
                if self.get_next(iid) is None:
                    return True
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
                if self.get_next(iid) is None:
                    return True
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

    def list_of_loop_stmt1(self, parent):
        iid = self.creat_node('list_of_loop_stmt1', parent)

        if self.is_decl_stmt(iid):
            if self.get_next(iid) is None:
                return True
            if self.list_of_loop_stmt1(iid):
                if self.get_next(iid) is None:
                    return True
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
                                if self.list_of_loop_stmt1(iid):
                                    if self.get_next(iid) is None:
                                        return True
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
                                            if self.list_of_loop_stmt1(iid):
                                                if self.get_next(iid) is None:
                                                    return True
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
                            if self.list_of_loop_stmt1(iid):
                                if self.get_next(iid) is None:
                                    return True
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
                                    if self.list_of_loop_stmt1(iid):
                                        if self.get_next(iid) is None:
                                            return True
                                        return True
        elif self.token == 'return':
            if self.get_next(iid) is None:
                return True
            if self.func_return_stmt1(iid):
                if self.list_of_loop_stmt1(iid):
                    if self.get_next(iid) is None:
                        return True
                    return True
        elif self.token == 'break':
            if self.get_next(iid) is None:
                return True
            if self.token == ';':
                if self.get_next(iid) is None:
                    return True
                if self.list_of_loop_stmt1(iid):
                    if self.get_next(iid) is None:
                        return True
                    return True
        elif self.token == 'continue':
            if self.get_next(iid) is None:
                return True
            if self.token == ';':
                if self.get_next(iid) is None:
                    return True
                if self.list_of_loop_stmt1(iid):
                    if self.get_next(iid) is None:
                        return True
                    return True
        elif self.token == '{':
            if self.get_next(iid) is None:
                return True
            if self.list_of_loop_stmt(iid):
                if self.token == '}':
                    if self.get_next(iid) is None:
                        return True
                    if self.list_of_loop_stmt1(iid):
                        if self.get_next(iid) is None:
                            return True
                        return True
        return True

    def func_if_stmt_for_loop1(self, parent):
        iid = self.creat_node('if_stmt_for_loop1', parent)

        if self.token == 'else':
            if self.get_next(iid) is None:
                return True
            if self.func_loop_stmt(iid):
                if self.get_next(iid) is None:
                    return True
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

    def is_decl_stmt(self, iid):
        handler = Match_base_stmt()
        handler.set_tokenList(self.arr[self.i:])
        res, i, subtree = handler.run_export_decl_stmt(False)
        self.i += i
        self.tree.paste(iid, subtree)
        return res

    def run_export_comp_stmt(self, flag):
        self.res = self.func_comp_stmt('root')
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
    handler = Match_exec_stmt()
    s = [
        'if ( i < 10 ) i = i + 1 ; else const int j = 0 ;',
        # 'if ( i < 10 ) i = i + 1 ; else i = 0 ;',
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
