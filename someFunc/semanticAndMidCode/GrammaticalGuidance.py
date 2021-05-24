from someFunc.parser.forecastTable.Grammar import Parser_analyzer


class Symbol:
    def __init__(self, node, type, scope):
        self.node = node
        self.type = type
        self.scope = scope

    def __repr__(self):
        return "tag: {},\ttype: {},\tvalue: {},\tscope: {}".format(self.node.data.tag, self.type, self.node.data.value,
                                                                   self.scope)


class Quaternion:
    def __init__(self, op, a1, a2, res):
        self.op = op
        self.a1 = a1
        self.a2 = a2
        self.res = res

    def __repr__(self):
        t1_num = 2
        t2_num = 2
        t3_num = 2

        if self.op and len(self.op) > 2:
            t1_num = 1
        if self.a1 and len(self.a1) > 2:
            t2_num = 1
        if self.a2 and len(self.a2) > 2:
            t3_num = 1
        return "op: {},{}a1: {},{}a2: {},{}res: {}".format(self.op, '\t' * t1_num,
                                                           self.a1, '\t' * t2_num,
                                                           self.a2, '\t' * t3_num,
                                                           self.res)


class SMC_analyzer(Parser_analyzer):
    def __init__(self):
        super().__init__()
        self.symbol_table = {}
        self.op_stack = []
        self.temp_stack = []

        self.jump_stack = []
        self.jump_queue = []

    def get_parent(self, node, itnum):
        end_parent = node
        for i in range(itnum):
            end_parent = self.AST_Tree.parent(end_parent.identifier)
            if end_parent is None:
                return None
            end_parent = self.AST_Tree.get_node(end_parent.identifier)
        return end_parent

    def arith_mid(self, postexp):
        postexp = postexp[::-1]
        op = {'+', '-', '*', '/'}
        opnd = []
        T = None
        for i in range(len(postexp)):
            if postexp[i] not in op:
                opnd.append(postexp[i])
            else:
                a = opnd.pop(-1)
                b = opnd.pop(-1)
                if postexp[i] in {'-', '/'}:
                    a, b = b, a
                T = "T{}".format(len(self.temp_stack))
                self.temp_stack.append(T)
                opnd.append(T)
                new_op = Quaternion(
                    '{}'.format(postexp[i]),
                    a,
                    b,
                    T
                )
                self.op_stack.append(new_op)
        return T

    def expr_processing(self, node):
        expr_subtree = self.AST_Tree.subtree(node.identifier)
        expr_leaves = expr_subtree.leaves()
        expr_list = []
        for item in expr_leaves:
            if item.tag == 'num':
                temp = item.data.tag
            elif item.tag == 'var':
                temp = item.data.tag
            else:
                temp = item.tag
            expr_list.append(temp)

        if expr_list[0] == '>':
            temp = Symbol(None, 'bool', -1)
            self.temp_stack.append(temp)
            new_op1 = Quaternion('>', '{}'.format(expr_list[2]), '{}'.format(expr_list[1]),
                                 "T{}".format(self.temp_stack.index(temp)))
            self.op_stack.extend([new_op1])
        elif expr_list[0] == '==':
            temp = Symbol(None, 'bool', -1)
            self.temp_stack.append(temp)
            new_op1 = Quaternion('==', '{}'.format(expr_list[2]), '{}'.format(expr_list[1]),
                                 "T{}".format(self.temp_stack.index(temp)))
            self.op_stack.extend([new_op1])
        else:
            res = ''
            for item in expr_list:
                res += item
            T = self.arith_mid(res)
            if T is None:
                T = res
            return T

    def decl_statement_processing(self, node):
        res = True
        info = []
        if node.tag == "decl_stmt'":
            type_node = self.AST_Tree.siblings(node.identifier)[0]
            type = type_node.tag
            child = self.AST_Tree.children(node.identifier)
            sym = Symbol(child[0], type, child[0].data.scope)
            if sym.node.data.tag not in self.symbol_table:
                self.symbol_table[sym.node.data.tag] = sym
            else:
                res = False
                info.append("{}".format(sym.node.data))
        return res, info

    def give_statement_processing(self, node):
        res = True
        info = []
        if node.tag == "=":
            # get left_value
            left_value = self.AST_Tree.parent(node.identifier)
            left_value = self.AST_Tree.siblings(left_value.identifier)
            # get expr_leaves
            expr_node = self.AST_Tree.siblings(node.identifier)[0]
            res = self.expr_processing(expr_node)
            if left_value[0].data.tag in self.symbol_table:
                self.symbol_table[left_value[0].data.tag].node.data.value = res
            else:
                res = False
                info.append("{}".format(left_value[0].data))
                return res, info
            # gen_op
            # new_op = Quaternion('=', res, '-',
            #                     "{}({})".format(left_value[0].data.tag, self.symbol_table[left_value[0].data.tag]))
            new_op = Quaternion('=', res, '-',
                                "{}".format(left_value[0].data.tag))
            self.op_stack.append(new_op)
        return res, info

    def control_statement_if_processing(self, node):
        if node.tag == "if":
            siblings = self.AST_Tree.siblings(node.identifier)
            ctrl_0 = siblings[1]  # 跳转条件
            self.expr_processing(ctrl_0)
            # new_op2 = Quaternion('jnz', "T{}".format(len(self.temp_stack) - 1), '-',
            #                      "{}({})".format('None', len(self.op_stack) + 2))
            new_op2 = Quaternion('jnz', "T{}".format(len(self.temp_stack) - 1), '-',
                                 "{}".format(len(self.op_stack) + 2))
            # new_op3 = Quaternion('j', "-", '-', "{}({})".format('None', 'None'))
            new_op3 = Quaternion('j', "-", '-', "{}".format('None', 'None'))
            self.op_stack.extend([new_op2, new_op3])
            self.jump_stack.extend([self.op_stack.index(new_op3)])
        elif node.tag == 'while':
            siblings = self.AST_Tree.siblings(node.identifier)
            ctrl_0 = siblings[1]  # 跳转条件
            self.expr_processing(ctrl_0)
            # new_op2 = Quaternion('jnz', "T{}".format(len(self.temp_stack) - 1), '-',
            #                      "{}({})".format('None', len(self.op_stack) + 2))
            new_op2 = Quaternion('jnz', "T{}".format(len(self.temp_stack) - 1), '-',
                                 "{}".format(len(self.op_stack) + 2))
            # new_op3 = Quaternion('j', "-", '-', "{}({})".format('None', 'None'))
            new_op3 = Quaternion('j', "-", '-', "{}".format('None'))
            self.op_stack.extend([new_op2, new_op3])
            self.jump_stack.extend([self.op_stack.index(new_op3)])
        elif node.tag == '}':
            end_parent = self.get_parent(node, 3)
            if end_parent is not None:
                siblings = self.AST_Tree.siblings(end_parent.identifier)
                aim_node = siblings[0]
                if aim_node.tag == "if":
                    # new_op = Quaternion('j', "-", '-', "{}({})".format('None', 'None'))
                    new_op = Quaternion('j', "-", '-', "{}".format('None'))
                    self.op_stack.extend([new_op])
                    self.jump_queue.extend([self.op_stack.index(new_op)])
                elif aim_node.tag == "while":
                    # new_op = Quaternion('j', "-", '-', "{}({})".format('None', 'None'))
                    new_op = Quaternion('j', "-", '-', "{}".format('None'))
                    self.op_stack.extend([new_op])
                    self.jump_queue.extend([self.op_stack.index(new_op)])

    def check_backfill_processing(self, node):
        if node.tag == '{':
            end_parent = self.get_parent(node, 3)
            if end_parent is not None:
                siblings = self.AST_Tree.siblings(end_parent.identifier)
                if siblings[0].tag == 'else':
                    if len(self.jump_stack) != 0:
                        idx = self.jump_stack.pop(-1)
                        # self.op_stack[idx].res = "{}({})".format('None', len(self.op_stack))
                        self.op_stack[idx].res = "{}".format(len(self.op_stack))
        elif node.tag == '}':
            end_parent = self.get_parent(node, 3)
            if end_parent is not None:
                siblings = self.AST_Tree.siblings(end_parent.identifier)
                if siblings[0].tag == 'else':
                    if len(self.jump_queue) != 0:
                        idx = self.jump_queue.pop(0)
                        # self.op_stack[idx].res = "{}({})".format('None', len(self.op_stack))
                        self.op_stack[idx].res = "{}".format(len(self.op_stack))
                elif siblings[0].tag == 'while':
                    if len(self.jump_queue) != 0:
                        idx = self.jump_queue.pop(0)
                        # self.op_stack[idx].res = "{}({})".format('None', self.jump_stack[-1] - 2)
                        self.op_stack[idx].res = "{}".format(self.jump_stack[-1] - 2)
                    if len(self.jump_stack) != 0:
                        idx = self.jump_stack.pop(-1)
                        # self.op_stack[idx].res = "{}({})".format('None', len(self.op_stack))
                        self.op_stack[idx].res = "{}".format(len(self.op_stack))

    def dfs_detect(self):
        res1 = False
        info1 = []
        res2 = False
        info2 = []
        stack = [self.AST_Tree_root]
        while stack:
            node = stack.pop(-1)
            # print(node.tag)

            # TODO
            # decl statement processing
            res1, info1 = self.decl_statement_processing(node)
            if res1:
                # give statement processing
                res2, info2 = self.give_statement_processing(node)
                if res2:
                    # control statement processing
                    self.control_statement_if_processing(node)
                    # check backfill processing
                    self.check_backfill_processing(node)

                    stack.extend(list(reversed(self.AST_Tree.children(node.identifier))))
            if res1 is False or res2 is False:
                if res1 is False:
                    print("Error: Variable definition")
                    print(info1)
                if res2 is False:
                    print("Error: Variable is not defined")
                    print(info2)
                break
        if res1 and res2:
            return self.symbol_table, self.op_stack
        else:
            return None


def main():
    pass


if __name__ == '__main__':
    main()
