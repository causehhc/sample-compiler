<表达式> -> <算术表达式> | <关系表达式> | <布尔表达式> | <赋值表达式>  
<算术表达式> -> <算术表达式> + <项> | <算术表达式> - <项> | <项>  
<项> -> <项> * <因子> | <项> / <因子> | <项> % <因子> | <因子>  
<因子> -> - <参数> | <参数>  
<参数> -> ( <算术表达式> ) | <常量> | <变量>  
<关系表达式> -> <算术表达式> <关系运算符> <算术表达式>  
<关系运算符> -> > | < | >= | <= | == | !=  
<布尔表达式> -> <布尔表达式> || <布尔项> | <布尔项>  
<布尔项> -> <布尔项> && <布尔因子> | <布尔因子>  
<布尔因子> -> <算数表达式> | <关系表达式> | ! <布尔表达式>
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
    expr -> a_expr | r_expr | b_expr | g_expr  
  a_expr -> a_item a_expr2  
  a_item -> a_factor a_item2  
a_factor -> - a_para | a_para  
  a_para -> ( a_expr ) | const | var  
  r_expr -> - a_para a_item2 a_expr2 r_op a_expr | ( a_expr ) a_item2 a_expr2 r_op a_expr | const a_item2 a_expr2 r_op a_expr | var a_item2 a_expr2 r_op a_expr  
    r_op -> > | < | >= | <= | == | !=  
  b_expr -> b_item b_expr1  
  b_item -> b_factor b_item1  
b_factor -> - a_para a_item2 a_expr2 | ( a_expr ) a_item2 a_expr2 | const a_item2 a_expr2 | var a_item2 a_expr2 | - a_para a_item2 a_expr2 r_op a_expr | ( a_expr ) a_item2 a_expr2 r_op a_expr | const a_item2 a_expr2 r_op a_expr | var a_item2 a_expr2 r_op a_expr | ! b_expr  
  g_expr -> var = expr  
 a_expr1 -> + a_item | - a_item  
 a_item1 -> * a_factor | / a_factor | % a_factor  
 a_expr2 -> a_expr1 a_expr2 | #  
 a_item2 -> a_item1 a_item2 | #  
 b_expr1 -> || b_item b_expr1 | #  
 b_item1 -> && b_factor b_item1 | #  
END:const, var, ops  