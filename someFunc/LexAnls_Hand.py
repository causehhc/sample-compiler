class Control:
    def __init__(self):
        self.key_word = self.__load_keyword()
        self.sta = None

    def __load_keyword(self):
        key_lines = open("./someFunc/keyword.txt", 'r').readlines()
        key_word = set()
        for key in key_lines:
            key_word.add(key.replace('\n', ''))
        return key_word

    def __check_identifier(self, s):
        self.sta = 0
        for i in range(len(s)):
            if self.sta == 0:
                if s[i].isalpha():
                    self.sta = 1
                else:
                    self.sta = -1
                    break
            elif self.sta == 1:
                if s[0:i + 1] in self.key_word:
                    self.sta = 3
                    break
                elif s[i].isalnum() or s[i] == '_':
                    self.sta = 1
                else:
                    self.sta = 2
                    break
        return self.sta

    def __check_integer(self, s):
        self.sta = 0
        for ch in s:
            if self.sta == 0:
                if ch.isdigit():
                    if 1 <= int(ch) <= 9:
                        self.sta = 1
                    elif int(ch) == 0:
                        self.sta = 3
                else:
                    self.sta = -1
                    break
            elif self.sta == 1:
                if ch.isdigit():
                    self.sta = 1
                else:
                    self.sta = 2
                    break
            elif self.sta == 3:
                if ch.isdigit():
                    if 0 <= int(ch) <= 7:
                        self.sta = 3
                elif ch == 'x' or ch == 'X':
                    self.sta = 5
                else:
                    self.sta = 4
                    break
            elif self.sta == 5:
                if ch.isdigit() or 'a' <= ch <= 'f' or 'A' <= ch <= 'F':
                    self.sta = 6
                else:
                    self.sta = -1
                    break
            elif self.sta == 6:
                if ch.isdigit() or 'a' <= ch <= 'f' or 'A' <= ch <= 'F':
                    self.sta = 6
                else:
                    self.sta = 7
                    break
        return self.sta

    def __check_note(self, s):
        self.sta = 0
        for i in range(len(s)):
            if self.sta == 0:
                if s[i] == '/':
                    self.sta = 1
                else:
                    self.sta = -1
                    break
            elif self.sta == 1:
                if s[i] == '/':
                    self.sta = 2
                elif s[i] == '*':
                    self.sta = 3
                else:
                    self.sta = 4
                    break
            elif self.sta == 2:
                if s[i] == '\n':
                    self.sta = 5
                    break
            elif self.sta == 3:
                if s[i] == '*':
                    self.sta = 6
            elif self.sta == 6:
                if s[i] == '/':
                    self.sta = 5
                    break
        return self.sta

    def check_type_old(self, s):
        id_sta = self.__check_identifier(s)
        if id_sta == 0:
            id_res = '开头不是字母'
        elif id_sta == 1:
            id_res = '符合标识符'
        elif id_sta == 2:
            id_res = '存在其他字符'
        elif id_sta == 3:
            id_res = '符合c关键字'
        else:
            id_res = 'error'

        in_sta = self.__check_integer(s)
        if in_sta == 0:
            in_res = '开头不是数字'
        elif in_sta == 1:
            in_res = '十进制'
        elif in_sta == 2:
            in_res = '十进制其他'
        elif in_sta == 3:
            in_res = '八进制'
        elif in_sta == 4:
            in_res = '八进制其他'
        elif in_sta == 5:
            in_res = '十六进制定义'
        elif in_sta == 6:
            in_res = '十六进制'
        elif in_sta == 7:
            in_res = '十六进制其他'
        else:
            in_res = 'error'

        note_sta = self.__check_note(s)
        if note_sta == 0:
            note_res = '开头不是斜杠'
        elif note_sta == 1:
            note_res = '/未闭合'
        elif note_sta == 2:
            note_res = '//未闭合'
        elif note_sta == 3:
            note_res = '/*未闭合'
        elif note_sta == 4:
            note_res = '/错误字符'
        elif note_sta == 5:
            note_res = '符合注释'
        elif note_sta == 6:
            note_res = '/**未闭合'
        else:
            note_res = 'error'

        res = '{}测试用例：{}\n'.format('=' * 4, s)
        res += '标识符状态：{} 状态信息：{}\n'.format(id_sta, id_res)
        res += '整数状态：{} 状态信息：{}\n'.format(in_sta, in_res)
        res += '注释状态：{} 状态信息：{}\n'.format(note_sta, note_res)
        return res

    def check_type(self, s):
        res = '''
标识符\tabc
整数10\t12
浮点数\t1.2
浮点数\t1.2e2+3
整数16\t0x34
整数8\t0912
运算符\t++
运算符\t+=
关键字\tvoid
关键字\tmain
界符\t{
关键字\tint
标识符\ta
运算符\t=
整数10\t0
界符\t;
界符\t}
'''
        return res
        id_sta = self.__check_identifier(s)  # 3
        in_sta = self.__check_integer(s)  # 1/3/6
        note_sta = self.__check_note(s)  # 5
        if id_sta == 3:
            res = '{}\t{}\n'.format('标识符', s)
            return res
        else:
            res = '{}\t{}\n'.format('error', s)

        if in_sta == 1 or in_sta == 3 or in_sta == 6:
            if in_sta == 1:
                res = '{}\t{}\n'.format('整数10', s)
            if in_sta == 3:
                res = '{}\t{}\n'.format('整数8', s)
            if in_sta == 6:
                res = '{}\t{}\n'.format('整数16', s)
            return res
        else:
            res = '{}\t{}\n'.format('error', s)

        if note_sta == 5:
            res = '{}\t{}\n'.format('注释', s)
            return res
        else:
            res = '{}\t{}\n'.format('error', s)
        return res

    def create_report(self, content):
        report = ''
        report += '{}'.format(self.check_type(content))
        return report
        for line in content.splitlines():
            testCase = line.split(' ')
            while '' in testCase:
                testCase.remove('')
            if testCase is not None:
                for item in testCase:
                    report += '{}'.format(self.check_type(item))
                    break
        return report


def main():
    ct = Control()

    content = """
        test te34 1234 12st te/34\n
        ttt 10234 10a1 0123 01a1 0x 0xa1 0xaz1\n
        """

    content = """
        void
        """

    content = '/*这是实验一的\n测试用例*/\n//大家把测试界面截图放文件中\nabc\n12' \
              '\n1.2\n12a\n1.2e2+3\n00.234e3\n0x34\n0x3g\n0912\n++\n+=\n>==3' \
              '\n\nvoid main()\n{\n	int a=0;\n}\n'

    print(content)

    # report = ct.create_report(content)
    # print(report)


if __name__ == '__main__':
    main()
