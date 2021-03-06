import graphviz
from treelib import Tree


class Parser_analyzer:
    """
    语句LL(1)文法：
    NEED：expr, 各种终止符
    NOTE：int_t为无法解决：
        A -> B int
        B -> int b | ϵ
    类型的回溯问题采用的特殊方案, 出现在int_t main()位置。
    """

    def __init__(self):
        self.Vn = []  # 非终结符
        self.Vt = []  # 终结符
        self.table = None  # 预测分析表
        self.stack_anls = []
        self.stack_toke = []

        self.err_info = []

        self.AST_Tree = Tree()
        self.AST_Tree_root = None
        self.parent_uid = None
        self.node_parent_dict = None

        self.current_anal_scope = 0

    def load_analyzer(self, prod_path, ff_path):
        prod_set = {}
        prod_set_ori = open(prod_path, 'r', encoding='utf-8').readlines()
        temp_prod = ''
        for item in prod_set_ori:
            item = item.strip()
            if item[0] != '|':
                temp = item.split(' ')
                temp_prod = temp[0]
                res = ''
                for ii in temp[2:]:
                    res += '{} '.format(ii)
                res = res.strip()
                prod_set[temp_prod] = []
                prod_set[temp_prod].append(res)
                if temp_prod not in self.Vn:
                    self.Vn.append(temp_prod)
            else:
                temp = item.split(' ')
                res = ''
                for ii in temp[1:]:
                    res += '{} '.format(ii)
                res = res.strip()
                prod_set[temp_prod].append(res)

        ff_set = {}
        ff_set_ori = open(ff_path, 'r', encoding='utf-8').readlines()
        for item in ff_set_ori:
            item = item.replace('\n', '')
            item = item.split('\t')

            end_symbol = item[0]
            eps_flag = item[1]
            fi_set = item[2].split(' ')
            if len(item) == 4:
                fo_set = item[3].split(' ')
            else:
                fo_set = []

            ff_set[end_symbol] = {
                'eps_flag': eps_flag,
                'fi_set': fi_set,
                'fo_set': fo_set
            }

        self.table = [[] for row in range(len(self.Vn))]  # 预测分析表

        for item in self.Vn:
            item_prod = prod_set[item]
            item_ff = ff_set[item]

            if item_ff['eps_flag'] == 'true':
                item_ff['fi_set'].remove('eps')
            for non in item_ff['fi_set']:
                if non not in self.Vt:
                    self.Vt.append(non)
                    for n in range(len(self.Vn)):
                        self.table[n].append('')
                aim_prod = None
                aim2_prod = None
                for temp_prod in item_prod:
                    temp_shit = temp_prod.split(' ')
                    temp_first = temp_shit[0]
                    if temp_first == 'eps' and len(temp_shit) > 1:
                        aim2_prod = temp_prod
                    if non == temp_first:
                        aim_prod = temp_prod
                        break
                    elif temp_first in ff_set:
                        if non in ff_set[temp_first]['fi_set'] or ff_set[temp_first]['eps_flag'] == 'true':
                            aim_prod = temp_prod
                            break

                if aim_prod is None:
                    aim_prod = aim2_prod
                self.table[self.Vn.index(item)][self.Vt.index(non)] = aim_prod
            if item_ff['eps_flag'] == 'true':
                for non in item_ff['fo_set']:
                    if non not in self.Vt:
                        self.Vt.append(non)
                        for n in range(len(self.Vn)):
                            self.table[n].append('')
                    self.table[self.Vn.index(item)][self.Vt.index(non)] = 'eps'

    def load_stack(self, token_list, start):
        self.stack_anls = []
        self.stack_anls.append('#')
        self.stack_anls.append(start)

        self.stack_toke = []
        self.stack_toke.append('#')
        temp = list(reversed(token_list))
        self.stack_toke.extend(temp)

        self.err_info = []

        self.node_parent_dict = {start: [None]}

    def table_show(self):
        res = ''
        # print(self.Vt)
        res += "{}\n".format(str(self.Vt))
        idx = 0
        for item in self.table:
            # print('{}'.format(self.Vn[idx]), end='\t')
            res += "{}\t".format(self.Vn[idx])
            idx2 = 0
            for jt in item:
                # print('\'{}\'({})'.format(jt, self.Vt[idx2]), end=' ')
                res += "'{}'({}) ".format(jt, self.Vt[idx2])
                idx2 += 1
            # print()
            res += '\n'
            idx += 1
        return res

    def ans_show(self):
        print(self.stack_anls)
        print(self.stack_toke)
        print()

    def creat_node(self, tag, parent, data):
        if self.AST_Tree.size() == 0:
            node = self.AST_Tree.create_node(tag='{}'.format(tag), data=data)
            self.AST_Tree_root = node
        else:
            node = self.AST_Tree.create_node(tag='{}'.format(tag), parent=parent, data=data)
        return node.identifier

    def create_dotPic(self, root_dir):
        # root_dir = './treePic'
        self.AST_Tree.to_graphviz(filename='{}/tree.dot'.format(root_dir))
        string = open('{}/tree.dot'.format(root_dir)).read()
        dot = graphviz.Source(string)
        dot.render('{}/tree'.format(root_dir), format='png')

    def run(self, log=False):
        anlsRes = ''
        anlsLog = ''
        toke = self.stack_toke.pop(-1)
        symbol = self.stack_anls.pop(-1)
        while symbol != '#':
            if symbol in [toke.tag, toke.type]:
                # 刷新作用域
                if symbol == '{':
                    self.current_anal_scope += 1
                elif symbol == '}':
                    self.current_anal_scope -= 1
                else:
                    toke.set_scope(self.current_anal_scope)
                # 刷新真值
                if toke.type == 'num':
                    toke.set_value(toke.tag)
                # 创建节点并新增
                self.creat_node(symbol, self.node_parent_dict[symbol][-1], toke)
                self.node_parent_dict[symbol].pop(-1)
                if len(self.node_parent_dict[symbol]) == 0:
                    self.node_parent_dict.pop(symbol)
                toke = self.stack_toke.pop(-1)
                if log:
                    # print('\t*HIT: {}\t<-\t{}'.format(symbol, toke))
                    anlsLog += "\t*HIT: {}\t<-\t{}\n".format(symbol, toke)
                if toke == '#':
                    break
            elif symbol in self.Vn:
                if toke.type in ['var', 'num']:  # 变量-数字转换
                    table_item = self.table[self.Vn.index(symbol)][self.Vt.index(toke.type)]
                else:
                    table_item = self.table[self.Vn.index(symbol)][self.Vt.index(toke.tag)]
                table_item = table_item.split(' ')
                if table_item[0] == '':  # 错误分析
                    # print('\t*ERROR: {}\t<-\t{}'.format(symbol, toke))
                    anlsLog += "\t*ERROR: {}\t<-\t{}\n".format(symbol, toke)
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
                    self.parent_uid = self.creat_node(symbol, self.node_parent_dict[symbol][-1], symbol)
                    self.node_parent_dict[symbol].pop(-1)
                    if len(self.node_parent_dict[symbol]) == 0:
                        self.node_parent_dict.pop(symbol)
                    # 添加节点-父节点Hash表
                    for item in temp:
                        if item not in self.node_parent_dict:
                            self.node_parent_dict[item] = []
                        self.node_parent_dict[item].append(self.parent_uid)
                    if log:
                        # print()
                        # print("symb:\'{}\'----stack:{}".format(symbol, list(reversed(self.stack_anls))))
                        # print("toke:{}----stack:{}".format(toke, list(reversed(self.stack_toke))))
                        anlsLog += "\n"
                        anlsLog += "symb:\'{}\'----stack:{}\n".format(symbol, list(reversed(self.stack_anls)))
                        anlsLog += "toke:{}----stack:{}\n".format(toke, list(reversed(self.stack_toke)))
            symbol = self.stack_anls.pop(-1)
        self.node_parent_dict.clear()
        # self.ans_show()
        if len(self.err_info) == 0:
            # print('match compete!')
            anlsRes += "match compete!\n"
        for item in self.err_info:
            anlsRes += "{}".format(item)
        return anlsRes, anlsLog


def main():
    path1 = './grammer_LL(1).txt'
    path2 = './ff_set.txt'
    anls = Parser_analyzer()
    anls.load_analyzer(path1, path2)
    anls.table_show()


if __name__ == '__main__':
    main()
