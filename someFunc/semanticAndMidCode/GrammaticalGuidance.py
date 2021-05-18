from someFunc.parser.forecastTable.Grammar import Parser_analyzer


class Symbol:
    def __init__(self, node, scope):
        self.node = node
        self.scope = scope

    def __repr__(self):
        return "{}".format(self.node.data)


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
        if len(self.op) > 2:
            t1_num = 1
        if len(self.a1) > 2:
            t2_num = 1
        if len(self.a2) > 2:
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

    def decl_statement_processing(self, node):
        if node.tag == "decl_stmt'":
            child = self.AST_Tree.children(node.identifier)
            sym = Symbol(child[0], child[0].data.scope)
            self.symbol_table[sym.node.data.tag] = sym

    def give_statement_processing(self, node):
        if node.tag == "=":
            # get left_value
            left_value = self.AST_Tree.parent(node.identifier)
            left_value = self.AST_Tree.siblings(left_value.identifier)
            # get expr_leaves
            expr_node = self.AST_Tree.siblings(node.identifier)[0]
            expr_subtree = self.AST_Tree.subtree(expr_node.identifier)
            expr_leaves = expr_subtree.leaves()
            # gen_op
            self.symbol_table[left_value[0].data.tag].node.data.value = expr_leaves[0].data.value
            new_op = Quaternion('=', expr_leaves[0].data.value, '-',
                                "{}({})".format(left_value[0].data.tag, self.symbol_table[left_value[0].data.tag]))
            self.op_stack.append(new_op)

    def control_statement_if_processing(self, node):
        if node.tag == "if":
            siblings = self.AST_Tree.siblings(node.identifier)
            ctrl_0 = siblings[1]  # 跳转条件
            ctrl_0_subtree = self.AST_Tree.subtree(ctrl_0.identifier)
            ctrl_0_subtree_leaves = ctrl_0_subtree.leaves()
            temp = Symbol(None, -1)
            if ctrl_0_subtree_leaves[1].data.tag == self.symbol_table[ctrl_0_subtree_leaves[2].data.tag].node.data.value:
                temp.value = 1
            else:
                temp.value = 0
            self.temp_stack.append(temp)
            new_op1 = Quaternion('=', '{}'.format(temp.value), '-', "{}({})".format("T{}".format(self.temp_stack.index(temp)),
                                                                              self.temp_stack.index(temp)))
            new_op2 = Quaternion('jnz', "T{}".format(self.temp_stack.index(temp)), '-',
                                 "{}({})".format('None', len(self.op_stack) + 3))
            new_op3 = Quaternion('jump', "-", '-', "{}({})".format('None', 'None'))
            self.op_stack.extend([new_op1, new_op2, new_op3])
            self.jump_stack.extend([self.op_stack.index(new_op3)])
        elif node.tag == '}':
            end_parent = self.get_parent(node, 3)
            if end_parent is not None:
                siblings = self.AST_Tree.siblings(end_parent.identifier)
                aim_node = siblings[0]
                if aim_node.tag == "if":
                    new_op = Quaternion('jump', "-", '-', "{}({})".format('None', 'None'))
                    self.op_stack.extend([new_op])
                    self.jump_queue.extend([self.op_stack.index(new_op)])

    def check_backfill_processing(self, node):
        if node.tag == '{':
            end_parent = self.get_parent(node, 3)
            if end_parent is not None:
                siblings = self.AST_Tree.siblings(end_parent.identifier)
                aim_node = siblings[0]
                if aim_node.tag == 'else':
                    if len(self.jump_stack) != 0:
                        idx = self.jump_stack.pop(-1)
                        self.op_stack[idx].res = "{}({})".format('None', len(self.op_stack))
        elif node.tag == '}':
            end_parent = self.get_parent(node, 3)
            if end_parent is not None:
                siblings = self.AST_Tree.siblings(end_parent.identifier)
                aim_node = siblings[0]
                if aim_node.tag == 'else':
                    if len(self.jump_queue) != 0:
                        idx = self.jump_queue.pop(0)
                        self.op_stack[idx].res = "{}({})".format('None', len(self.op_stack))

    def dfs_detect(self):
        stack = [self.AST_Tree_root]
        while stack:
            node = stack.pop(-1)
            # print(node.tag)

            # TODO
            # decl statement processing
            self.decl_statement_processing(node)
            # give statement processing
            self.give_statement_processing(node)
            # control statement processing
            self.control_statement_if_processing(node)
            # check backfill processing
            self.check_backfill_processing(node)

            stack.extend(list(reversed(self.AST_Tree.children(node.identifier))))
        for item in self.symbol_table:
            print(item)
        for item in self.op_stack:
            print("{}\t{}".format(self.op_stack.index(item), item))


def main():
    pass


if __name__ == '__main__':
    main()
