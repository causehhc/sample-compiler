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
                    if temp_first == 'eps' and len(temp_shit)>1:
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
            print('{}'.format(self.Vn[idx]), end='\t')
            idx2 = 0
            for jt in item:
                print('\'{}\'({})'.format(jt, self.Vt[idx2]), end=' ')
                idx2 += 1
            print()
            idx += 1

    def ans_show(self):
        print(self.stack_anls)
        print(self.stack_toke)
        print()

    def run(self, log=False):
        toke = self.stack_toke.pop(-1)
        symbol = self.stack_anls.pop(-1)
        while symbol != '#':
            if log:
                print("symb:\'{}\'----stack:{}".format(symbol, list(reversed(self.stack_anls))))
                print("toke:{}----stack:{}".format(toke, list(reversed(self.stack_toke))))
            if symbol == toke.val or symbol == toke.type:
                if log:
                    print('\t*HIT: {}\t<-\t{}'.format(symbol, toke))
                toke = self.stack_toke.pop(-1)
                if toke == '#':
                    break
            elif symbol in self.Vn:
                if toke.type in ['var', 'num']:
                    table_item = self.table[self.Vn.index(symbol)][self.Vt.index(toke.type)]
                else:
                    table_item = self.table[self.Vn.index(symbol)][self.Vt.index(toke.val)]
                table_item = table_item.split(' ')
                if table_item[0] == '':
                    print('\t*ERROR: {}\t<-\t{}'.format(symbol, toke))
                    self.err_info.append(
                        "row: {}, col: {}, token: '{}' cont match '{}'\n".format(toke.row, toke.col, toke, symbol))
                elif table_item[0] == 'eps':
                    if len(table_item) > 1:
                        temp = list(reversed(table_item))
                        self.stack_anls.extend(temp)
                        self.stack_anls.pop(-1)
                else:
                    temp = list(reversed(table_item))
                    self.stack_anls.extend(temp)
            symbol = self.stack_anls.pop(-1)
            if log:
                print()

        self.ans_show()
        if len(self.err_info) == 0:
            print('match compete!')
        for item in self.err_info:
            print(item)


def main():
    path1 = './grammer_LL(1).txt'
    path2 = './ff_set.txt'
    anls = Parser_analyzer()
    anls.load_analyzer(path1, path2)
    anls.table_show()


if __name__ == '__main__':
    main()
