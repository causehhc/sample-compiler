from someFunc.parser.forecastTable.Grammar import Parser_analyzer


class SMC_analyzer(Parser_analyzer):
    def __init__(self):
        super().__init__()
        self.qu = "op: {}\ta1: {}\ta2: {}\tres: {}"
        self.symbol_table = []
        self.op_stack = []

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
            op = self.qu.format('=', expr_leaves[0].data.value, '-', "{}({})".format(left_value[0].data.tag, left_value[0].identifier))
            self.op_stack.append(op)
            print(op)

    def control_statement_processing(self, node):
        if node.tag == "if":
            siblings = self.AST_Tree.siblings(node.identifier)
            ctrl_0 = siblings[1]
            ctrl_1 = siblings[3]
            ctrl_2 = siblings[4]
            print(ctrl_0)
            print(ctrl_1)
            print(ctrl_2)

    def bfs_detect(self):
        queue = [self.AST_Tree_root]
        while queue:
            node = queue.pop(0)

            # TODO
            # decl statement processing
            self.decl_statement_processing(node)
            # give statement processing
            self.give_statement_processing(node)
            # control statement processing
            self.control_statement_processing(node)

            queue.extend(self.AST_Tree.children(node.identifier))
        # for item in self.symbol_table:
        #     print(item)


def main():
    pass


if __name__ == '__main__':
    main()
