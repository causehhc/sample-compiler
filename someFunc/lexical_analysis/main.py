class Analyzer:
    def __init__(self, text):
        self.text = text
        self.token = []
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
        keyword = {"void", "main", "short", "long", "int", "double", "float", "while", "if", "else", "for", "break",
                   "return"}
        if s in keyword:
            return True
        return False

    def run(self):
        """
        1-标识符
        2-保留字
        3-运算符
        4-界符
        5-整数
        6-实数
        :return:
        """
        ch = self.get_next()
        while ch:
            if ch in [',', ';', '(', ')', '{', '}']:  # 识别分界符 4
                tmp_dict = {'src': ch, 'token': '4', 'row': self.row_idx, 'col': self.col_idx}
                self.token.append(tmp_dict)
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
                            tmp_dict = {'src': tmp_s, 'token': '6', 'row': self.row_idx, 'col': self.col_idx}  # 常实数
                            self.token.append(tmp_dict)
                            break
                        else:
                            tmp_dict = {'src': tmp_s, 'token': 'error', 'row': self.row_idx, 'col': self.col_idx}  # 如果小数点后没有数字，则报错
                            self.token.append(tmp_dict)
                    if ch.isdigit() is False:
                        tmp_dict = {'src': tmp_s, 'token': '5', 'row': self.row_idx, 'col': self.col_idx}  # 常整数
                        self.token.append(tmp_dict)
                        break
            elif ch.isalpha() or ch == '_':  # 识别标识符 1 / 保留字 2
                tmp_s = ''
                while ch and (ch.isalpha() or ch.isdigit() or ch == '_'):
                    tmp_s += ch
                    ch = self.get_next()
                if self.lookup(tmp_s):  # 在keyword表中查找s是否是保留字
                    tmp_dict = {'src': tmp_s, 'token': '2', 'row': self.row_idx, 'col': self.col_idx}  # 保留字
                    self.token.append(tmp_dict)
                else:
                    tmp_dict = {'src': tmp_s, 'token': '1', 'row': self.row_idx, 'col': self.col_idx}  # 标识符
                    self.token.append(tmp_dict)
            elif ch == '>':  # 后面都是运算符 3
                tmp_s = ''
                tmp_s += ch
                ch = self.get_next()
                if ch == '=':  # ">="
                    tmp_s += ch
                    ch = self.get_next()
                tmp_dict = {'src': tmp_s, 'token': '3', 'row': self.row_idx, 'col': self.col_idx}
                self.token.append(tmp_dict)
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
                tmp_dict = {'src': tmp_s, 'token': '3', 'row': self.row_idx, 'col': self.col_idx}
                self.token.append(tmp_dict)
            elif ch == '=':
                tmp_s = ''
                tmp_s += ch
                ch = self.get_next()
                if ch == '=':  # "=="
                    tmp_s += ch
                    ch = self.get_next()
                tmp_dict = {'src': tmp_s, 'token': '3', 'row': self.row_idx, 'col': self.col_idx}
                self.token.append(tmp_dict)
            elif ch == '&':
                tmp_s = ''
                tmp_s += ch
                ch = self.get_next()
                if ch == '&':  # "&&"
                    tmp_s += ch
                    ch = self.get_next()
                tmp_dict = {'src': tmp_s, 'token': '3', 'row': self.row_idx, 'col': self.col_idx}
                self.token.append(tmp_dict)
            elif ch == '|':
                tmp_s = ''
                tmp_s += ch
                ch = self.get_next()
                if ch == '|':  # "||"
                    tmp_s += ch
                    ch = self.get_next()
                tmp_dict = {'src': tmp_s, 'token': '3', 'row': self.row_idx, 'col': self.col_idx}
                self.token.append(tmp_dict)
            elif ch in ['+', '-', '*', '/', '%']:
                tmp_dict = {'src': ch, 'token': '3', 'row': self.row_idx, 'col': self.col_idx}
                self.token.append(tmp_dict)
                ch = self.get_next()
            else:  # 跳过当前单词
                ch = self.get_next()

    def get_token(self):
        self.run()
        return self.token


def main():
    text = open('./input.txt', 'r', encoding='utf-8').read()
    # print(text)
    anal = Analyzer(text)
    token = anal.get_token()
    for item in token:
        print(item)


if __name__ == '__main__':
    main()
