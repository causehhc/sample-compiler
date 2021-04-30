import uuid
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
            for temp_prod in item_prod:
                temp_first = temp_prod.split(' ')[0]
                if temp_first in ff_set:
                    temp_prod_ff = ff_set[temp_first]
                else:
                    eps_flag = 'false'
                    if temp_first == 'eps':
                        eps_flag = 'true'
                    temp_prod_ff = {
                        'eps_flag': eps_flag,
                        'fi_set': [temp_first],
                        'fo_set': []
                    }

                select_set = temp_prod_ff['fi_set']
                if 'eps' in select_set:
                    select_set.remove('eps')
                for non in select_set:
                    if non not in self.Vt:
                        self.Vt.append(non)
                        for n in range(len(self.Vn)):
                            self.table[n].append('')
                    self.table[self.Vn.index(item)][self.Vt.index(non)] = temp_prod
                if item_ff['eps_flag'] == 'true':
                    select_set = item_ff['fo_set']
                    for non in select_set:
                        if non not in self.Vt:
                            self.Vt.append(non)
                            for n in range(len(self.Vn)):
                                self.table[n].append('')
                        self.table[self.Vn.index(item)][self.Vt.index(non)] = 'eps'

    def load_stack(self, token_list):
        self.stack_anls = []
        self.stack_anls.append('#')
        self.stack_anls.append('program')

        self.stack_toke = []
        self.stack_toke.append('#')
        temp = list(reversed(token_list))
        self.stack_toke.extend(temp)

        self.err_info = []

    def table_show(self):
        print(self.Vt)
        idx = 0
        for item in self.table:
            print(self.Vn[idx], item)
            idx += 1

    def ans_show(self):
        print(self.stack_anls)
        for item in self.stack_toke:
            if item == '#':
                print('#', end=' ')
            else:
                print(item.val, end=' ')
        print()

    def run(self):
        toke = self.stack_toke.pop(-1)
        symbol = self.stack_anls.pop(-1)
        while symbol != '#':
            if symbol == toke.val:
                toke = self.stack_toke.pop(-1)
                if toke == '#':
                    break
            elif symbol in self.Vn:
                table_item = self.table[self.Vn.index(symbol)][self.Vt.index(toke.val)]
                table_item = table_item.split(' ')
                if table_item[0] == '':
                    self.err_info.append(
                        "row: {}, col: {}, token: '{}' cont match '{}'\n".format(toke.row, toke.col, toke.val, symbol))
                elif table_item[0] != 'eps':
                    # print('hello world2', symbol, toke.val)
                    temp = list(reversed(table_item))
                    self.stack_anls.extend(temp)
            symbol = self.stack_anls.pop(-1)

        self.ans_show()
        if len(self.err_info) == 0:
            print('match compete!')
        for item in self.err_info:
            print(item)


def main():
    path1 = './statement_LL(1).txt'
    path2 = './ff_set.txt'
    anls = Parser_analyzer()
    anls.load_analyzer(path1, path2)


if __name__ == '__main__':
    main()
