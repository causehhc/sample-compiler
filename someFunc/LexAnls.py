import re
import subprocess


class LexAnls:
    """
    关键字: c语言
    运算符: = + - * / & | ! && || < <= => == !=
    界符: , ; { } " " [ ]
    标识符:
    值:十进制整数 浮点数
    """

    def __init__(self):
        # self.p_key = re.compile()
        # self.p_op = re.compile()
        # self.p_limit = re.compile()
        self.p_id = re.compile(r'[a-zA-Z][a-zA-Z0-9]*')
        self.p_int = re.compile(r'[0-9]+')
        self.p_float = re.compile(r'[0-9]+[.][0-9]+')
        self.p_none = re.compile(r'..')

    def find_all(self, s):
        m_id = self.p_id.findall(s)
        print(m_id)
        m_int = self.p_int.findall(s)
        print(m_int)
        m_float = self.p_float.findall(s)
        print(m_float)
        m_none = self.p_none.findall(s)
        print(m_none)

    def find_all_exec(self, s):
        if s == '':
            return "Empty string"
        cmd = '{} "{}"'.format('test5.exe', s)
        out = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        text = out.stdout.read().decode(encoding='ISO-8859-1')

        res = []
        text_s1 = text.split('\n')
        for text_s2 in text_s1:
            kv = text_s2.split(':')
            if len(kv) > 1:
                temp = [kv[0], kv[1].replace('\r', '')]
                res.append(temp)
        return res


def main():
    anls = LexAnls()
    # anls.find_all('0a12.x3b')
    res = anls.find_all_exec('1x1')
    print(res)
    pass


if __name__ == '__main__':
    main()
