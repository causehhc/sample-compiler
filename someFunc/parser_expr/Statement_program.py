"""
<程序> -> <声明语句> main() <复合语句> <函数块>
<函数块> -> <函数定义> <函数块> | ϵ
=============================================================
program -> decl_stmt main ( ) comp_stmt func_block
func_block -> func_def func_block | ϵ
"""
from Match_base import Match_base


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
        # TODO
        pass

    def is_decl_stmt(self, iid):
        # TODO
        pass

    def is_func_def(self, iid):
        # TODO
        pass


def main():
    handler = Match_program_stmt()
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
