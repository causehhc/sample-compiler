class Parser_analyzer:
    def __init__(self):
        self.Gdict = {  # 算术表达式文法
            'G': ['#E#'],
            'E': ['E+T', 'T'],
            'T': ['T*F', 'F'],
            'F': ['(E)', 'i'],
        }
        self.vt = ['+', '*', 'i', '(', ')', '#']  # 终结符
        self.vn = ['G', 'E', 'T', 'F']  # 非终结符

        self.fvt = None
        self.lvt = None
        self.opTable = None

        self.stack_anls = []
        self.stack_toke = []
        self.err_info = []

    def getFirstVTset(self, x, f):
        for s in self.Gdict[x]:
            i = 0
            for i in range(len(s)):
                if s[i] in self.vt:
                    f.append(s[i])
                    break
            if i == len(s) and s[0] in self.vn:
                self.getFirstVTset(s[0], f)

    def get_firstVT(self):
        a = []
        x = []
        y = []
        for c in self.vn:
            f = []
            self.getFirstVTset(c, f)
            a += f
        x.append(a[0])
        y.append(x)
        for i in range(1, len(a)):
            b = a[i:]
            y.append(b)

        i = 0
        firstVTdict = {}
        for c in self.vn:
            if c not in firstVTdict:
                firstVTdict[c] = y[i]
                i += 1
        self.fvt = firstVTdict

    def getLastVTset(self, x, f):
        for s in self.Gdict[x]:
            i = len(s) - 1
            for i in range(0, len(s))[::-1]:
                if s[i] in self.vt:
                    f.append(s[i])
                    break
            if i == 0 and s[0] in self.vn:
                self.getLastVTset(s[0], f)

    def get_lastVT(self):
        lastVTdict = {}
        for c in self.vn:
            f = []
            if c not in lastVTdict:
                self.getLastVTset(c, f)
                lastVTdict[c] = f
        self.lvt = lastVTdict

    def addopgtable(self, lst, ch, tmp):
        if tmp == 2:  # <关系
            for i in range(1, len(self.vt) + 1):
                if self.opTable[i][0] == ch:
                    for j in range(1, len(self.vt) + 1):
                        if self.opTable[0][j] in lst:
                            self.opTable[i][j] = 2
        elif tmp == 3:  # >关系
            for i in range(1, len(self.vt) + 1):
                if self.opTable[i][0] in lst:
                    for j in range(1, len(self.vt) + 1):
                        if self.opTable[0][j] == ch:
                            self.opTable[i][j] = 3

    def get_opTable(self):
        self.opTable = []
        for i in range(len(self.vt) + 1):  # 初始化算符优先表
            a = None
            temp_dict = {1: '+', 2: '*', 3: 'i', 4: '(', 5: ')', 6: '#'}
            if i == 0:
                a = [''] + self.vt
            elif i in temp_dict:
                a = [temp_dict[i], '', '', '', '', '', '']
            self.opTable.append(a)
        for c in self.vn:
            for s in self.Gdict[c]:
                if len(s) > 1:
                    for i in range(len(s) - 1):
                        if s[i] in self.vt and s[i + 1] in self.vn:  # 小于关系
                            self.addopgtable(self.fvt[s[i + 1]], s[i], 2)
                        elif s[i] in self.vn and s[i + 1] in self.vt:  # >关系
                            self.addopgtable(self.lvt[s[i]], s[i + 1], 3)
                        if i < len(s) - 2 and s[i] in self.vt and s[i + 2] in self.vt:
                            for x in range(1, len(self.vt) + 1):
                                if self.opTable[x][0] == s[i]:
                                    for j in range(1, len(self.vt) + 1):
                                        if self.opTable[0][j] == s[i]:
                                            self.opTable[x][j] = 1

    def load_stack(self, token_list):
        self.stack_anls = []
        self.stack_anls.append('#')

        self.stack_toke = []
        self.stack_toke.append('#')
        temp = list(reversed(token_list))
        self.stack_toke.extend(temp)

    def getOutvalue(self, x, y):  # 比较优先关系
        for i in range(1, len(self.vt) + 1):
            if self.opTable[i][0] == x:
                for j in range(1, len(self.vt) + 1):
                    if self.opTable[0][j] == y:
                        return self.opTable[i][j]

    def run(self, log=False):
        self.get_firstVT()
        self.get_lastVT()
        self.get_opTable()
        print(self.fvt)
        print(self.lvt)
        for item in self.opTable:
            print(item)

        n = ''
        sbuff = list(self.stack_toke)
        print(sbuff)
        top = 1
        s = ['', '#']
        a = sbuff[-1]
        while a != '#':
            if s[top] in self.vt:
                j = top
            else:
                j = top - 1
            v = self.getOutvalue(s[j], a)
            while v == 3:
                q = s[j]
                if s[j - 1] in self.vt:
                    j = j - 1
                else:
                    j = j - 2
                v = self.getOutvalue(s[j], q)
                tp = s[j + 1:top + 1]
                for i in range(len(tp)):
                    c = s.pop()
                    temp_dict = {'i': 'F', '*': 'T', '+': 'E'}
                    n = temp_dict[c]
                s.append(n)
                top = j + 1
            if v == 2 or v == 1:
                top = top + 1
                s.append(a)
                sbuff.pop()
            else:
                self.err_info.append('Error!')
                break
            a = sbuff[-1]
            if log:
                print(s)
                print(sbuff)
                print()
        print(self.err_info)


def main():
    t = Parser_analyzer()
    t.load_stack('i+i*i')
    t.run(log=True)


if __name__ == '__main__':
    main()
