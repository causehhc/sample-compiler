from someFunc.parser.forecastTable.Grammar import Parser_analyzer


class SMC_analyzer(Parser_analyzer):
    def __init__(self):
        super().__init__()

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
    pass


if __name__ == '__main__':
    main()

