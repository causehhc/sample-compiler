"""
<程序> -> <声明语句> main() <复合语句> <函数块>
<函数块> -> <函数定义> <函数块> | ϵ
=============================================================
program -> decl_stmt main ( ) comp_stmt func_block
func_block -> func_def func_block | ϵ
"""
from Match_base import Match_base
from someFunc.parser_expr.Statement_base import Match_base_stmt
from someFunc.parser_expr.Statement_exec import Match_exec_stmt
from someFunc.parser_expr.Statement_func import Match_func_stmt


class Match_program_stmt(Match_base):
    def __init__(self):
        super().__init__()

    def func_main(self, parent):
        iid = self.creat_node('program', parent)

        if self.is_decl_stmt(iid):
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
                                if self.get_next(iid) is None:
                                    return True
                                return True
        return False

    def func_func_block(self, parent):
        iid = self.creat_node('func_block', parent)

        if self.is_func_def(iid):
            if self.get_next(iid) is None:
                return True
            if self.func_func_block(iid):
                if self.get_next(iid) is None:
                    return True
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
        handler.set_tokenList(self.arr[self.i:])
        res, i, subtree = handler.run_export_decl_stmt(False)
        self.i += i
        self.tree.paste(iid, subtree)
        return res

    def is_func_def(self, iid):
        handler = Match_func_stmt()
        handler.set_tokenList(self.arr[self.i:])
        res, i, subtree = handler.run(False)
        self.i += i
        self.tree.paste(iid, subtree)
        return res


def main():
    handler = Match_program_stmt()
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
