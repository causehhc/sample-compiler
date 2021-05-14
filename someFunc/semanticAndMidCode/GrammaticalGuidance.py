from someFunc.parser.forecastTable.Grammar import Parser_analyzer


class SMC_analyzer(Parser_analyzer):
    def __init__(self):
        super().__init__()

    def run(self, log=False):
        toke = self.stack_toke.pop(-1)
        symbol = self.stack_anls.pop(-1)
        while symbol != '#':
            if symbol == toke.val or symbol == toke.type:
                toke = self.stack_toke.pop(-1)
                # 创建节点并新增
                self.creat_node(symbol, self.node_parent_dict[symbol][-1])
                if len(self.node_parent_dict[symbol]) == 0:
                    self.node_parent_dict.pop(symbol)
                if log:
                    print('\t*HIT: {}\t<-\t{}'.format(symbol, toke))
                if toke == '#':
                    break
            elif symbol in self.Vn:
                if toke.type in ['var', 'num']:  # 变量-数字转换
                    table_item = self.table[self.Vn.index(symbol)][self.Vt.index(toke.type)]
                else:
                    table_item = self.table[self.Vn.index(symbol)][self.Vt.index(toke.val)]
                table_item = table_item.split(' ')
                if table_item[0] == '':  # 错误分析
                    print('\t*ERROR: {}\t<-\t{}'.format(symbol, toke))
                    self.err_info.append(
                        "row: {}, col: {}, token: '{}' cont match '{}'\n".format(toke.row, toke.col, toke, symbol))
                elif table_item[0] == 'eps':  # 无效回溯
                    if len(table_item) > 1:  # 有效分析
                        temp = list(reversed(table_item))[0:-1]
                        self.stack_anls.extend(temp)
                        # 添加节点-父节点Hash表
                        for item in temp:
                            if item not in self.node_parent_dict:
                                self.node_parent_dict[item] = []
                            self.node_parent_dict[item].append(self.parent_uid)
                else:  # 有效分析
                    temp = list(reversed(table_item))
                    self.stack_anls.extend(temp)
                    # 创建节点并新增
                    self.parent_uid = self.creat_node(symbol, self.node_parent_dict[symbol][-1])
                    self.node_parent_dict[symbol].pop(-1)
                    if len(self.node_parent_dict[symbol]) == 0:
                        self.node_parent_dict.pop(symbol)
                    # 添加节点-父节点Hash表
                    for item in temp:
                        if item not in self.node_parent_dict:
                            self.node_parent_dict[item] = []
                        self.node_parent_dict[item].append(self.parent_uid)
                    if log:
                        print()
                        print("symb:\'{}\'----stack:{}".format(symbol, list(reversed(self.stack_anls))))
                        print("toke:{}----stack:{}".format(toke, list(reversed(self.stack_toke))))
            symbol = self.stack_anls.pop(-1)
        self.node_parent_dict.clear()
        # self.ans_show()
        if len(self.err_info) == 0:
            print('match compete!')
        for item in self.err_info:
            print(item)


def main():
    pass


if __name__ == '__main__':
    main()
