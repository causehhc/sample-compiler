# """
# <赋值表达式> -> <标识符>=<表达式>
# =============================================================
# g_expr -> var = expr
# """
# import uuid
# from treelib import Tree
# # from expr_main import Match_expr
#
#
# class Match_g_expr:
#     def __init__(self):
#         self.arr = None
#         self.i = 0
#         self.token = ''
#         self.tree = Tree()
#         self.tree.create_node(tag='main', identifier='root')
#         self.anls = []
#         self.res = True
#         self.info = ''
#
#     def set_tokenList(self, arr):
#         self.arr = arr
#         self.i = 0
#         self.token = self.arr[self.i]
#         self.tree = Tree()
#         self.tree.create_node(tag='main', identifier='root')
#         self.anls = []
#         self.res = True
#         self.info = ''
#
#     def get_next(self, parent):
#         tmp = self.i - len(self.anls)
#         for i in range(tmp + 1):
#             self.anls.append(self.arr[self.i - tmp + i])
#         self.tree.create_node(tag=self.token, identifier=str(uuid.uuid1()), parent=parent)
#
#         if self.i == len(self.arr) - 1:
#             self.i += 1
#             self.token = None
#             return self.token
#         else:
#             self.i += 1
#             self.token = self.arr[self.i]
#             return self.token
#
#     def error(self, error, summer):
#         # self.res = False
#         self.info = 'error{}: {}'.format(error, summer)
#
#     def creat_node(self, name, parent):
#         iid = str(uuid.uuid1())
#         self.tree.create_node(tag='{}'.format(name), identifier=iid, parent=parent)
#         return iid
#
#     def func_g_expr(self, parent):
#         iid = self.creat_node('g_expr', parent)
#
#         if self.is_var():
#             if self.get_next(iid) is None:
#                 return True
#             if self.token == '=':
#                 if self.get_next(iid) is None:
#                     return True
#                 if self.is_expr():
#                     if self.get_next(iid) is None:
#                         return True
#                     return True
#         return False
#
#     def is_var(self):
#         return self.token.isidentifier()
#
#     def is_expr(self):
#         # handler = Match_expr()
#         # handler.set_tokenList(self.arr[self.i:])
#         # res, i = handler.run(False)
#         # self.i += i
#         # return res
#         return True
#
#     def run(self, flag):
#         self.res = self.func_g_expr('root')
#         if self.i == len(self.arr) - 1:
#             tmp = self.arr[:self.i + 1]
#         else:
#             tmp = self.arr[:self.i]
#         if self.res is True:
#             if tmp != self.anls or len(self.arr) > len(self.anls):
#                 self.error(2, 'unmatched characters')
#                 if flag:
#                     self.res = False
#         return self.res, self.i - 1
#
#
# def main():
#     handler = Match_g_expr()
#     arr = [['V', '=', 'E']]
#     for item in arr:
#         print('Detected string: ', item)
#         handler.set_tokenList(item)
#         res = handler.run()
#         print('Compliance with the rules: ', res)
#         if res is False:
#             print(handler.info)
#         handler.tree.show()
#         print()
#     pass
#
#
# if __name__ == '__main__':
#     main()
