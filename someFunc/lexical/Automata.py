class TokenNode:
    def __init__(self, val, type, row, col):
        self.val = val
        self.type = type
        self.row = row
        self.col = col

    def __repr__(self):
        return '\'{}\'({})[{}, {}]'.format(self.val, self.type, self.row, self.col)


class Lex_analyzer:
    def __init__(self):
        self.text = None
        self.token = []
        self.info = []
        self.idx = 0
        self.row_idx = 0
        self.col_idx = 0

    def set_text(self, text):
        self.text = text
        self.token = []
        self.info = []
        self.idx = 0
        self.row_idx = 0
        self.col_idx = 0

    def get_next(self):
        res = None
        if self.idx != len(self.text):
            res = self.text[self.idx]
            self.idx += 1
            self.col_idx += 1
            if res == '\n':
                self.row_idx += 1
                self.col_idx = 0
            return res
        return res

    def lookup(self, s):
        keyword = {
            'char',
            'const',
            'float',
            'int',
            'void',
            'do',
            'for',
            'if',
            'return',
            'while',
            'break',
            'continue',
            'int_t',
            'else',
        }
        if s in keyword:
            return True
        return False

    def run(self):
        """
        var-标识符
        2-关键字
        3-运算符
        4-界符
        num-整数
        num-实数
        :return:
        """
        ch = self.get_next()
        while ch:
            if ch in [',', ';', '(', ')', '{', '}']:  # 识别分界符 4
                self.token.append(TokenNode(ch, '4', self.row_idx, self.col_idx))
                ch = self.get_next()
            elif ch.isdigit():  # 识别整数 5 / 实数 6
                tmp_s = ''
                while ch and ch.isdigit():
                    tmp_s += ch
                    ch = self.get_next()
                    if ch == '.':  # 出现小数点，有可能是常实数
                        tmp_s += ch
                        ch = self.get_next()
                        if ch.isdigit():
                            while ch and ch.isdigit():
                                tmp_s += ch
                                ch = self.get_next()
                            self.token.append(TokenNode(tmp_s, 'num', self.row_idx, self.col_idx))
                            break
                        else:
                            self.token.append(TokenNode(tmp_s, 'error', self.row_idx, self.col_idx))
                    if ch.isdigit() is False:
                        self.token.append(TokenNode(tmp_s, 'num', self.row_idx, self.col_idx))
                        break
            elif ch.isalpha() or ch == '_':  # 识别标识符 1 / 保留字 2
                tmp_s = ''
                while ch and (ch.isalpha() or ch.isdigit() or ch == '_'):
                    tmp_s += ch
                    ch = self.get_next()
                if self.lookup(tmp_s):  # 在keyword表中查找s是否是保留字
                    self.token.append(TokenNode(tmp_s, '2', self.row_idx, self.col_idx))
                else:
                    self.token.append(TokenNode(tmp_s, 'var', self.row_idx, self.col_idx))
            elif ch == '>':  # 后面都是运算符 3
                tmp_s = ''
                tmp_s += ch
                ch = self.get_next()
                if ch == '=':  # ">="
                    tmp_s += ch
                    ch = self.get_next()
                self.token.append(TokenNode(tmp_s, '3', self.row_idx, self.col_idx))
            elif ch == '<':
                tmp_s = ''
                tmp_s += ch
                ch = self.get_next()
                if ch == '=':  # "<="
                    tmp_s += ch
                    ch = self.get_next()
                elif ch == '>':  # "<>"
                    tmp_s += ch
                    ch = self.get_next()
                self.token.append(TokenNode(tmp_s, '3', self.row_idx, self.col_idx))
            elif ch == '=':
                tmp_s = ''
                tmp_s += ch
                ch = self.get_next()
                if ch == '=':  # "=="
                    tmp_s += ch
                    ch = self.get_next()
                self.token.append(TokenNode(tmp_s, '3', self.row_idx, self.col_idx))
            elif ch == '&':
                tmp_s = ''
                tmp_s += ch
                ch = self.get_next()
                if ch == '&':  # "&&"
                    tmp_s += ch
                    ch = self.get_next()
                self.token.append(TokenNode(tmp_s, '3', self.row_idx, self.col_idx))
            elif ch == '|':
                tmp_s = ''
                tmp_s += ch
                ch = self.get_next()
                if ch == '|':  # "||"
                    tmp_s += ch
                    ch = self.get_next()
                self.token.append(TokenNode(tmp_s, '3', self.row_idx, self.col_idx))
            elif ch in ['+', '-', '*', '/', '%']:
                if ch == '/':
                    ch = self.get_next()
                    if ch == '/':  # "//"
                        while ch != '\n':
                            ch = self.get_next()
                        ch = self.get_next()
                    elif ch == '*':  # "/*"
                        ch = self.get_next()
                        while ch != '*':
                            ch = self.get_next()
                        ch = self.get_next()
                        if ch == '/':
                            ch = self.get_next()
                        else:
                            # print('lex error: Incorrect comment format')
                            self.info.append('lex error: Incorrect comment format')
                    else:
                        self.token.append(TokenNode(ch, '3', self.row_idx, self.col_idx))
                else:
                    self.token.append(TokenNode(ch, '3', self.row_idx, self.col_idx))
                    ch = self.get_next()
            else:  # 跳过当前单词
                if ch not in ['\n', '\t', ' ']:
                    # print('lex error: Unrecognized character {}'.format(ch))
                    self.info.append('lex error: Unrecognized character {}'.format(ch))
                ch = self.get_next()

    def get_token_info(self):
        self.run()
        if len(self.info) == 0:
            self.info.append('all ok')
        return self.token, self.info


def main():
    text = open('./input.c', 'r', encoding='utf-8').read()
    # print(text)
    anal = Lex_analyzer()
    anal.set_text(text)
    token_list, info_list = anal.get_token_info()
    for item in token_list:
        print(item.val)


if __name__ == '__main__':
    main()
