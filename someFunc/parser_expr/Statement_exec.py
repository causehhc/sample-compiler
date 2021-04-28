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
com_stmt -> { stmt_list }
stmt_list -> stmt | stmt stmt_list
if_stmt -> if ( expr ) stmt | if ( expr ) stmt else stmt
for_stmt -> for ( expr ; expr ; expr ) loop_stmt
while_stmt -> while ( expr ) loop_stmt
do_while_stmt -> do comp_stmt_for_loops while ( expr ) ;
loop_stmt -> decl_stmt | loop_exec_stmt | loop_comp_stmt
comp_stmt_for_loop -> { list_of_loop_stmt }
loop_stmt_list -> loop_stmt | loop_stmt loop_stmt_list
loop_exec_stmt -> loop_if_stmt | for_stmt | while_stmt | do_while_stmt | return_stmt | break_stmt | continue_stmt
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
          com_stmt -> { stmt_list }
         stmt_list -> stmt stmt_list'
           if_stmt -> if ( expr ) stmt if_stmt'
          for_stmt -> for ( expr ; expr ; expr ) loop_stmt
        while_stmt -> while ( expr ) loop_stmt
     do_while_stmt -> do comp_stmt_for_loops while ( expr ) ;
         loop_stmt -> decl_stmt
                    | loop_exec_stmt
                    | loop_comp_stmt
comp_stmt_for_loop -> { list_of_loop_stmt }
    loop_stmt_list -> decl_stmt loop_stmt_list'
                    | loop_exec_stmt loop_stmt_list'
                    | loop_comp_stmt loop_stmt_list'
    loop_exec_stmt -> loop_if_stmt
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
   loop_stmt_list' -> ϵ
                    | decl_stmt loop_stmt_list'
                    | loop_if_stmt loop_stmt_list'
                    | for ( expr ; expr ; expr ) loop_stmt loop_stmt_list'
                    | while ( expr ) loop_stmt loop_stmt_list'
                    | do comp_stmt_for_loops while ( expr ) ; loop_stmt_list'
                    | return return_stmt' loop_stmt_list'
                    | break ; loop_stmt_list'
                    | continue ; loop_stmt_list'
                    | loop_comp_stmt loop_stmt_list'
 if_stmt_for_loop' -> ϵ
                    | else loop_stmt
      return_stmt' -> ;
                    | expr ;

"""
from Match_base import Match_base


class Match_exec_stmt(Match_base):
    def __init__(self):
        super().__init__()

    def func_main(self, parent):
        iid = self.creat_node('func name', parent)
        # TODO
        return False


def main():
    handler = Match_exec_stmt()
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
