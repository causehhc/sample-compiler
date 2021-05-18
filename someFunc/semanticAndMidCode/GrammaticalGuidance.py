from someFunc.parser.forecastTable.Grammar import Parser_analyzer


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
        self.symbol_table = []
        self.op_stack = []
        self.temp_stack = []

        self.jump_stack = []
        self.jump_queue = []

    def decl_statement_processing(self, node):
        if node.tag == "decl_stmt'":
            child = self.AST_Tree.children(node.identifier)
            sym = {
                'node_id': child[0].identifier,
                'node': child[0],
                'scope': child[0].data.scope,
                'value': None
            }
            self.symbol_table.append(sym)

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
            new_op = Quaternion(
                '=',
                expr_leaves[0].data.value,
                '-',
                "{}({})".format(left_value[0].data.tag, left_value[0].identifier))
            self.op_stack.append(new_op)

    def control_statement_processing(self, node):
        if node.tag == "if":
            siblings = self.AST_Tree.siblings(node.identifier)
            ctrl_0 = siblings[1]  # 跳转条件
            ctrl_1 = siblings[3]  # 跳转为真
            ctrl_2 = siblings[4]  # 跳转为假
            temp = ctrl_0
            self.temp_stack.append(temp)
            new_op1 = Quaternion(
                '=',
                ctrl_0.data,
                '-',
                "{}({})".format("T{}".format(self.temp_stack.index(temp)), self.temp_stack.index(temp)))
            new_op2 = Quaternion(
                'jnz',
                "T{}".format(self.temp_stack.index(temp)),
                '-',
                "{}({})".format('None', len(self.op_stack) + 3))
            new_op3 = Quaternion(
                'jump',
                "-",
                '-',
                "{}({})".format('None', 'None'))
            self.op_stack.extend([new_op1, new_op2, new_op3])
            self.jump_stack.extend([self.op_stack.index(new_op3)])
        elif node.tag == '}':
            end_parent = node
            for i in range(3):
                end_parent = self.AST_Tree.parent(end_parent.identifier)
                end_parent = self.AST_Tree.get_node(end_parent.identifier)
            siblings = self.AST_Tree.siblings(end_parent.identifier)
            aim_node = siblings[0]
            node_siblings = self.AST_Tree.siblings(node.identifier)
            flag = False
            for item in node_siblings:
                if item.tag == '}':
                    flag = True
                    break
            if aim_node.tag == "if" or flag:
                new_op = Quaternion(
                    'jump',
                    "-",
                    '-',
                    "{}({})".format('None', 'None'))
                self.op_stack.extend([new_op])
                self.jump_queue.extend([self.op_stack.index(new_op)])

    def check_backfill_processing(self, node):
        if node.tag == '{':
            end_parent = node
            for i in range(3):
                end_parent = self.AST_Tree.parent(end_parent.identifier)
                if end_parent is None:
                    return None
                end_parent = self.AST_Tree.get_node(end_parent.identifier)
            siblings = self.AST_Tree.siblings(end_parent.identifier)
            aim_node = siblings[0]
            if aim_node.tag == 'else':
                if len(self.jump_stack) != 0:
                    idx = self.jump_stack.pop(-1)
                    self.op_stack[idx].res = "{}({})".format('None', len(self.op_stack))
        elif node.tag == '}':
            end_parent = node
            for i in range(3):
                end_parent = self.AST_Tree.parent(end_parent.identifier)
                if end_parent is None:
                    return None
                end_parent = self.AST_Tree.get_node(end_parent.identifier)
            siblings = self.AST_Tree.siblings(end_parent.identifier)
            aim_node = siblings[0]
            if aim_node.tag == 'else':
                if len(self.jump_queue) != 0:
                    idx = self.jump_queue.pop(0)
                    self.op_stack[idx].res = "{}({})".format('None', len(self.op_stack))


    def bfs_detect(self):
        queue = [self.AST_Tree_root]
        while queue:
            node = queue.pop(0)
            print(node)

            # TODO
            # # decl statement processing
            # self.decl_statement_processing(node)
            # # give statement processing
            # self.give_statement_processing(node)
            # # control statement processing
            # self.control_statement_processing(node)

            queue.extend(self.AST_Tree.children(node.identifier))
        for item in self.symbol_table:
            print(item)

    def dfs_detect(self):
        stack = [self.AST_Tree_root]
        while stack:
            node = stack.pop(-1)

            # TODO
            # decl statement processing
            self.decl_statement_processing(node)
            # give statement processing
            self.give_statement_processing(node)
            # control statement processing
            self.control_statement_processing(node)
            # check backfill processing
            self.check_backfill_processing(node)

            stack.extend(list(reversed(self.AST_Tree.children(node.identifier))))
        for item in self.op_stack:
            print("{}\t{}".format(self.op_stack.index(item), item))


def main():
    pass


if __name__ == '__main__':
    main()
