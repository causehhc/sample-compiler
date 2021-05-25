class Parser_analyzer_op:
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

    def releft(self, str):
        strs = ''
        k = 0
        if len(str) == 3:
            for temp in self.Gdict:
                if temp in str[2]:
                    for i in range(2):
                        strs = strs + str[i]
                    strs = strs + k
                k = temp

        for i in range(2):
            for temp in self.Gdict:
                ch = temp
                for item in self.Gdict[temp]:
                    if len(item) != len(str):
                        continue
                    for i in range(len(str)):
                        if 65 <= ord(str[i]) <= 90:
                            if 65 <= ord(item[i]) <= 90:
                                pass
                                # print('')
                            else:
                                break
                        else:
                            if ord(str[i]) != ord(item[i]):
                                break
                    if str in item:
                        return ch
            if len(strs) == 3:
                str = ''
                for i in strs:
                    str = str + i
        return 0

    def run(self, log=False):
        anlsRes = ''
        anlsLog = ''
        self.get_firstVT()
        self.get_lastVT()
        self.get_opTable()
        # print(self.fvt)
        anlsRes+="{}\n".format(self.fvt)
        # print(self.lvt)
        anlsRes += "{}\n".format(self.lvt)
        for item in self.opTable:
            # print(item)
            anlsRes += "{}\n".format(item)

        token_list = list(self.stack_toke)
        token = token_list[-1]
        symbol = ['#', 'i']
        # print(sbuff)
        flag_gui = 0
        top = 0
        flag_re = 0
        guiyue = 0
        staus = 0
        catch = 0
        while token != '#' or (symbol[1] in self.vt or len(symbol) != 2):
            if catch == 0:
                symbol.pop()
            catch = catch + 1
            if flag_gui == 1 and (token_list[len(token_list) - 1 - top] != 'E'):
                token_list[len(token_list) - 1 - top] = self.releft(token_list[len(token_list) - 1 - top])
                flag_gui = 0
                token = token_list[len(token_list) - 1 - top]
            if symbol[top] in self.vt:
                j = top
            else:
                j = top - 1
            v = self.getOutvalue(symbol[j], token)
            while v != 1 and v != 2:
                q = symbol[j]
                if symbol[j - 1] in self.vt:
                    j = j - 1
                else:
                    j = j - 2
                v = self.getOutvalue(symbol[j], q)
                temp = ''
                time = 0
                if j + 1 == top:
                    temp += str(symbol[j + 1])
                    guiyue = 1
                else:
                    for i in range(2):
                        time = time + 1
                    temp += str(symbol[j + 1])
                    temp += str(symbol[j + 2])
                    temp += token
                temp = self.releft(str(temp))
                if temp != 0:
                    while time != 0:
                        time = time - 1
                        symbol.pop()
                    if guiyue == 0:
                        symbol.append(temp)
                        staus = 1
                    else:
                        if flag_re == 1:
                            symbol.append(temp)
                            staus = 3
                        else:
                            symbol[j + 1] = temp
                    guiyue = 0
                else:
                    staus = 0
                top = j + 1
            if v == 1 or v == 2:
                if staus == 0:
                    top = top + 1
                    symbol.append(token)
                token_list.pop()
                staus = 0
            if len(token_list) == 0:
                for i in range(len(symbol) - 1):
                    token_list.append(symbol[i])
                symbol = ['#']
                self.vn.pop()
                top = 0
                flag_gui = 1
                flag_re = 1
            token = token_list[-1]
            if log:
                # print(s)
                # print(sbuff)
                # print()
                anlsLog += '{}\n'.format(symbol)
                anlsLog += '{}\n'.format(token_list)
                anlsLog += '\n'

        return anlsRes, anlsLog


def main():
    t = Parser_analyzer_op()
    t.load_stack('i+i*i')
    res, log = t.run(log=True)
    # print(res)
    print(log)


if __name__ == '__main__':
    main()
