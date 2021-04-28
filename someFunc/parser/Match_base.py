import uuid
from treelib import Tree


class Match_base:
    def __init__(self):
        self.arr = None
        self.i = 0
        self.token = ''
        self.tree = Tree()
        # self.tree.create_node(tag='main', identifier='root')
        self.anls = []
        self.res = True
        self.info = ''

    def set_tokenList(self, arr):
        self.arr = arr
        self.i = 0
        self.token = self.arr[self.i]
        self.tree = Tree()
        # self.tree.create_node(tag='main', identifier='root')
        self.anls = []
        self.res = True
        self.info = ''

    def get_next(self, parent):
        tmp = self.i - len(self.anls)
        if tmp < 0:
            tmp = 0
            self.i += 1
        for i in range(tmp + 1):
            if self.i - tmp + i < len(self.arr):
                self.anls.append(self.arr[self.i - tmp + i])
        if self.token is not None:
            self.tree.create_node(tag=self.token, identifier=str(uuid.uuid1()), parent=parent)

        if self.i >= len(self.arr) - 1:
            self.i += 1
            self.token = '#'
            self.anls.append(self.token)
            return self.token
        else:
            self.i += 1
            self.token = self.arr[self.i]
            return self.token

    def error(self, error, summer):
        # self.res = False
        self.info = 'error{}: {}'.format(error, summer)

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
        if self.token in {"void", "main", "short", "long", "int", "double", "float", "while", "if", "else", "for", "break", "return"}:
            res = False
        return res

    def is_const(self):
        return self.token.isdigit()

    def run(self, flag):
        self.res = self.func_main('root')
        if self.res is True:
            if len(self.arr) > len(self.anls):
                self.error(2, 'unmatched characters')
                if flag:
                    self.res = False
        if self.i == 0:
            self.i += 1
        return self.res, self.i - 1, self.tree
