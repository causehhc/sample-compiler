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
        self.temp_symbol_stack = []

        self.op_stack = []
        self.temp_op_stack = []

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

    def arith_mid(self, postexp, temp_flag=False):
        postexp = postexp.split(' ')
        postexp = postexp[::-1]
        postexp.pop(0)
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
                T = "T{}".format(len(self.temp_symbol_stack))
                self.temp_symbol_stack.append(T)
                opnd.append(T)
                new_op = Quaternion(
                    '{}'.format(postexp[i]),
                    a,
                    b,
                    T
                )
                if temp_flag:
                    self.temp_op_stack.append(new_op)
                else:
                    self.op_stack.append(new_op)
        return T

    def expr_processing(self, node, temp_flag=False):
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
        ops = None
        res = None
        if expr_list[0] in {'>', '<', '>=', '<=', '!=', '=='}:
            temp = Symbol(None, 'bool', -1)
            self.temp_symbol_stack.append(temp)
            new_op1 = Quaternion('{}'.format(expr_list[0]), '{}'.format(expr_list[2]), '{}'.format(expr_list[1]),
                                 "T{}".format(self.temp_symbol_stack.index(temp)))
            # self.op_stack.extend([new_op1])
            ops = [new_op1]
        elif '(' in expr_list and ')' in expr_list:
            temp = Symbol(None, 'bool', -1)
            self.temp_symbol_stack.append(temp)
            new_op1 = Quaternion('call', '{}'.format(expr_list[2]), '-',
                                 "T{}".format(self.temp_symbol_stack.index(temp)))
            # self.op_stack.extend([new_op1])
            ops = [new_op1]
            res = "T{}".format(self.temp_symbol_stack.index(temp))
        else:
            res = ''
            for item in expr_list:
                res += "{} ".format(item)
            T = self.arith_mid(res, temp_flag=temp_flag)
            if T is None:
                T = res[:-1]
            res = T
        if ops is not None:
            if temp_flag:
                self.temp_op_stack.extend(ops)
            else:
                self.op_stack.extend(ops)
        return res

    def decl_statement_processing(self, node):
        res = True
        info = []
        if node.tag == "decl_stmt'":
            type_node = self.AST_Tree.siblings(node.identifier)[0]
            type = type_node.tag
            child = self.AST_Tree.children(node.identifier)
            var_decl_table_node = child[1]
            table_child = self.AST_Tree.children(var_decl_table_node.identifier)
            if len(table_child) > 1 and table_child[1].tag == 'expr':
                self.AST_Tree.remove_node(table_child[1].identifier)
            var_decl_table_tree = self.AST_Tree.subtree(var_decl_table_node.identifier)
            var_decl_table = var_decl_table_tree.leaves()
            var = [child[0]]
            for item in var_decl_table:
                if item.tag == 'var':
                    var.append(item)
            for item in var:
                sym = Symbol(item, type, child[0].data.scope)
                if sym.node.data.tag not in self.symbol_table:
                    self.symbol_table[sym.node.data.tag] = sym
                else:
                    res = False
                    info.append("{}".format(sym.node.data))
        return res, info

    def give_statement_processing(self, node, temp_flag=False):
        res = True
        info = []
        if node.tag == "=":
            # get left_value
            left_value = self.AST_Tree.parent(node.identifier)
            left_value = self.AST_Tree.siblings(left_value.identifier)
            # get expr_leaves
            expr_node = self.AST_Tree.siblings(node.identifier)[0]
            res = self.expr_processing(expr_node, temp_flag=temp_flag)
            if left_value[0].data.tag in self.symbol_table:
                self.symbol_table[left_value[0].data.tag].node.data.value = res
            else:
                res = False
                info.append("{}".format(left_value[0].data))
                return res, info

            # gen_op
            new_op = Quaternion('=', res, '-', "{}".format(left_value[0].data.tag))
            if temp_flag:
                self.temp_op_stack.append(new_op)
            else:
                self.op_stack.append(new_op)
        return res, info

    def control_statement_if_processing(self, node):
        if node.tag == "if":
            siblings = self.AST_Tree.siblings(node.identifier)
            ctrl_0 = siblings[1]  # 跳转条件
            flag = self.expr_processing(ctrl_0)
            if flag is None:
                new_op2 = Quaternion('jnz', "T{}".format(len(self.temp_symbol_stack) - 1), '-',
                                     "{}".format(len(self.op_stack) + 2))
            else:
                new_op2 = Quaternion('jnz', "{}".format(flag), '-',
                                     "{}".format(len(self.op_stack) + 2))
            new_op3 = Quaternion('j', "-", '-', "{}".format('None', 'None'))
            self.op_stack.extend([new_op2, new_op3])
            self.jump_stack.extend([self.op_stack.index(new_op3)])
        elif node.tag == 'while':
            siblings = self.AST_Tree.siblings(node.identifier)
            ctrl_0 = siblings[1]  # 跳转条件
            self.expr_processing(ctrl_0)
            new_op2 = Quaternion('jnz', "T{}".format(len(self.temp_symbol_stack) - 1), '-',
                                 "{}".format(len(self.op_stack) + 2))
            new_op3 = Quaternion('j', "-", '-', "{}".format('None'))
            self.op_stack.extend([new_op2, new_op3])
            self.jump_stack.extend([self.op_stack.index(new_op3)])
        elif node.tag == "for":
            siblings = self.AST_Tree.siblings(node.identifier)
            # 条件初始化
            ctrl_1 = siblings[1]
            child = self.AST_Tree.children(ctrl_1.identifier)
            child = self.AST_Tree.children(child[1].identifier)
            self.give_statement_processing(child[0])
            self.AST_Tree.remove_node(ctrl_1.identifier)
            # 跳转条件
            ctrl_2 = siblings[3]
            self.expr_processing(ctrl_2)
            new_op2 = Quaternion('jnz', "T{}".format(len(self.temp_symbol_stack) - 1), '-',
                                 "{}".format(len(self.op_stack) + 2))
            new_op3 = Quaternion('j', "-", '-', "{}".format('None'))
            self.op_stack.extend([new_op2, new_op3])
            self.jump_stack.extend([self.op_stack.index(new_op3)])
            # 累加条件
            ctrl_3 = siblings[5]
            child = self.AST_Tree.children(ctrl_3.identifier)
            child = self.AST_Tree.children(child[1].identifier)
            self.give_statement_processing(child[0], temp_flag=True)
            self.AST_Tree.remove_node(ctrl_3.identifier)
        elif node.tag == '}':
            end_parent = self.get_parent(node, 3)
            if end_parent is not None:
                siblings = self.AST_Tree.siblings(end_parent.identifier)
                aim_node = siblings[0]
                if aim_node.tag == "if":
                    child = self.AST_Tree.siblings(aim_node.identifier)
                    if len(child) == 5 and self.AST_Tree.children(child[4].identifier)[0].tag == 'else':  # 有else才产生特殊j
                        new_op = Quaternion('j', "-", '-', "{}".format('None'))
                        self.op_stack.extend([new_op])
                        self.jump_queue.extend([self.op_stack.index(new_op)])
                elif aim_node.tag == "while":
                    new_op = Quaternion('j', "-", '-', "{}".format('None'))
                    self.op_stack.extend([new_op])
                    self.jump_queue.extend([self.op_stack.index(new_op)])
                elif aim_node.tag == "for":
                    new_op = Quaternion('j', "-", '-', "{}".format('None'))
                    self.op_stack.extend(self.temp_op_stack)
                    self.temp_op_stack.clear()
                    self.op_stack.extend([new_op])
                    self.jump_queue.extend([self.op_stack.index(new_op)])
        elif node.tag == "stmt_list'''":
            func_name = self.AST_Tree.siblings(node.identifier)[0].data.tag
            child = self.AST_Tree.children(node.identifier)
            flag = child[0].tag
            if flag == '(':
                args_list_node = child[1]
                args_subtree = self.AST_Tree.subtree(args_list_node.identifier)
                args_leaves = args_subtree.leaves()
                for item in args_leaves:
                    if item.tag != ',':
                        new_op = Quaternion('para', "{}".format(item.data.tag), '-', "-")
                        self.op_stack.extend([new_op])
                temp = Symbol(None, 'bool', -1)
                self.temp_symbol_stack.append(temp)
                new_op1 = Quaternion('call', '{}'.format(func_name), '-',
                                     "T{}".format(self.temp_symbol_stack.index(temp)))
                self.op_stack.extend([new_op1])
        elif node.tag == "program":
            new_op = Quaternion('main', '-', '-', "-")
            self.op_stack.append(new_op)

    def check_backfill_processing(self, node):
        if node.tag == '}':
            end_parent = self.get_parent(node, 3)
            if end_parent is not None:
                siblings = self.AST_Tree.siblings(end_parent.identifier)
                if siblings[0].tag == 'else':
                    if len(self.jump_queue) != 0:
                        idx = self.jump_queue.pop(0)
                        self.op_stack[idx].res = "{}".format(len(self.op_stack))
                elif siblings[0].tag == 'if':
                    if len(self.jump_stack) != 0:
                        idx = self.jump_stack.pop(-1)
                        self.op_stack[idx].res = "{}".format(len(self.op_stack))
                elif siblings[0].tag == 'while':
                    if len(self.jump_queue) != 0:
                        idx = self.jump_queue.pop(0)
                        self.op_stack[idx].res = "{}".format(self.jump_stack[-1] - 2)
                    if len(self.jump_stack) != 0:
                        idx = self.jump_stack.pop(-1)
                        self.op_stack[idx].res = "{}".format(len(self.op_stack))
                elif siblings[0].tag == 'for':
                    if len(self.jump_queue) != 0:
                        idx = self.jump_queue.pop(0)
                        self.op_stack[idx].res = "{}".format(self.jump_stack[-1] - 2)
                    if len(self.jump_stack) != 0:
                        idx = self.jump_stack.pop(-1)
                        self.op_stack[idx].res = "{}".format(len(self.op_stack))

    def dfs_detect(self):
        anlsRes = ''
        anlsLog = ''
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
                    if node.identifier in self.AST_Tree:
                        stack.extend(list(reversed(self.AST_Tree.children(node.identifier))))
            if res1 is False or res2 is False:
                if res1 is False:
                    # print("Error: Variable definition")
                    anlsRes+="Error: Variable definition\n"
                    # print(info1)
                    anlsLog+="{}\n".format(info1)
                if res2 is False:
                    # print("Error: Variable is not defined")
                    anlsRes += "Error: Variable is not defined\n"
                    # print(info2)
                    anlsLog += "{}\n".format(info2)
                break
        if res1 and res2:
            new_op = Quaternion('sys', '-', '-', "-")
            self.op_stack.append(new_op)
            return self.symbol_table, self.op_stack, True
        else:
            return anlsRes, anlsLog, False


def main():
    pass


if __name__ == '__main__':
    main()
