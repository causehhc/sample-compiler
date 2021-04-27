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
Symbol      Nullable	First	            Follow
a_expr	    false	    ( - const var	    != $ && ) + - < <= == > >= ||
a_factor	false	    ( - const var	    != $ % && ) * + - / < <= == > >= ||
a_item	    false	    ( - const var	    != $ % && ) * + - / < <= == > >= ||
a_para	    false	    ( const var	        != $ % && ) * + - / < <= == > >= ||
b_expr	    false	    ! ( - const var	    $ && ||
b_factor	false	    ! ( - const var	    $ && ||
b_item	    false	    ! ( - const var	    $ && ||
expr	    false	    ! ( - const var	    $
g_expr	    false	    var	                $
r_expr	    false	    ( - const var	    $ && ||
r_op	    false	    != < <= == > >=	    ( - const var











    expr -> a_expr
          | r_expr
          | b_expr
          | g_expr
  a_expr -> a_item a_expr''
  a_item -> a_factor a_item''
a_factor -> - a_para
          | a_para
  a_para -> ( a_expr )
          | const
          | var
  r_expr -> - a_para a_item'' a_expr'' r_op a_expr
          | ( a_expr ) a_item'' a_expr'' r_op a_expr
          | const a_item'' a_expr'' r_op a_expr
          | var a_item'' a_expr'' r_op a_expr
    r_op -> >
          | <
          | >=
          | <=
          | ==
          | !=
  b_expr -> b_item b_expr'
  b_item -> b_factor b_item'
b_factor -> - a_para a_item'' a_expr''
          | ( a_expr ) a_item'' a_expr''
          | const a_item'' a_expr''
          | var a_item'' a_expr''
          | - a_para a_item'' a_expr'' r_op a_expr
          | ( a_expr ) a_item'' a_expr'' r_op a_expr
          | const a_item'' a_expr'' r_op a_expr
          | var a_item'' a_expr'' r_op a_expr
          | ! b_expr
  g_expr -> var = expr
 a_expr' -> + a_item
          | - a_item
 a_item' -> * a_factor
          | / a_factor
          | % a_factor
a_expr'' -> a_expr' a_expr''
          | ϵ
a_item'' -> a_item' a_item''
          | ϵ
 b_expr' -> || b_item b_expr'
          | ϵ
 b_item' -> && b_factor b_item'
          | ϵ

"""


def main():
    pass


if __name__ == '__main__':
    main()
