import uuid
from treelib import Tree


class Match_base:
    def __init__(self):
        self.token_list = None
        self.index = 0
        self.token = ''
        self.token_node = None
        self.tree = Tree()
        self.anls_proc = []
        self.res = True
        # self.info = []
        self.info = ''

    def set_tokenList(self, token_list):
        self.token_list = token_list
        self.index = 0
        self.token = self.token_list[self.index].val
        self.token_node = self.token_list[self.index]
        self.tree = Tree()
        self.anls_proc = []
        self.res = True
        # self.info = []
        self.info = ''

    def get_next(self, parent):
        tmp = self.index - len(self.anls_proc)
        if tmp < 0:
            tmp = 0
            self.index += 1
        for i in range(tmp + 1):
            if self.index - tmp + i < len(self.token_list):
                self.anls_proc.append(self.token_list[self.index - tmp + i].val)
        if self.token is not None:
            self.tree.create_node(tag=self.token, identifier=str(uuid.uuid1()), parent=parent)

        if self.index >= len(self.token_list) - 1:
            self.index += 1
            self.token = '#'
            self.anls_proc.append(self.token)
            return self.token
        else:
            self.index += 1
            self.token = self.token_list[self.index].val
            self.token_node = self.token_list[self.index]
            return self.token

    def reset_token(self, re_num=-1):
        if re_num == -1:
            self.index = 0
            self.anls_proc.clear()
            self.token = self.token_list[self.index].val
            self.token_node = self.token_list[self.index]
        else:
            self.index -= re_num
            for i in range(re_num):
                self.anls_proc.pop(len(self.anls_proc)-1)
            self.token = self.token_list[self.index].val
            self.token_node = self.token_list[self.index]

    def creat_node(self, name, parent):
        iid = str(uuid.uuid1())
        if self.tree.size() == 0:
            self.tree.create_node(tag='{}'.format(name), identifier=iid)
        else:
            self.tree.create_node(tag='{}'.format(name), identifier=iid, parent=parent)
        return iid

    def func_main(self, parent):
        return False

    def is_var(self):
        res = self.token.isidentifier()
        if self.token in {"void", "main", "short", "long", "int", "double", "float", "while", "if", "else", "for",
                          "break", "return"}:
            res = False
        return res

    def is_const(self):
        return self.token.isdigit()

    def run(self, flag):
        self.res = self.func_main('root')
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
        if len(self.info) == 0:
            self.info = 'all ok'
        return self.res, self.index - 1, self.tree, self.info
