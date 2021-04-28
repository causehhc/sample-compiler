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
from Match_base import Match_base


class Match_func_stmt(Match_base):
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
            if self.get_next(iid) is None:
                return True
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
                    if self.get_next(iid) is None:
                        return True
                    return True
        return False

    def func_func_def_para1(self, parent):
        iid = self.creat_node('func_def_para1', parent)

        if self.token == ',':
            if self.get_next(iid) is None:
                return True
            if self.func_func_def_para(iid):
                if self.get_next(iid) is None:
                    return True
                return True
        return True

    def is_func_type(self, iid):
        # TODO
        pass

    def is_var(self):
        # TODO
        pass

    def is_comp_stmt(self, iid):
        # TODO
        pass

    def is_var_type(self, iid):
        # TODO
        pass


def main():
    handler = Match_func_stmt()
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
