class Analyzer:
    def __init__(self):
        pass

    def getvalue(self, dict_fuh, dict_temp, x):
        if x.isdigit():
            result_x = int(x)
        elif x in dict_fuh.keys():
            result_x = dict_fuh[x]
        else:
            result_x = dict_temp[x]
        return int(result_x)

    def jieshiqi(self, dict_fuh, list_four, list_hs):
        anlsRes = ''
        i = int(0)
        j = len(list_four)
        list_para = []
        dict_temp = {
            'temp': 0,
        }
        jum = int(0)
        result = None
        while i < j:
            print('step',i)
            if list_four[i][0] == 'main':
                i += 1
                continue
            elif list_four[i][0] == 'sys':
                break
            elif list_four[i][0] == 'call':
                if list_four[i][1] == 'read':
                    dict_temp[list_four[i][3]] = input('请输入参数')
                elif list_four[i][1] == 'write':
                    print('输出')
                    anlsRes += "Output: \n"
                    for va in list_para:
                        print(va)
                        anlsRes += "{} ".format(va)
                else:
                    if result is None:
                        cs = 1
                        for va in list_para:
                            for hs in list_hs:
                                if hs[0] == list_four[i][1]:
                                    dict_fuh[hs[cs]] = int(va)
                                    cs += 1
                        mark = 0
                        for four in list_four:
                            if four[0] == list_four[i][1]:
                                break
                            mark += 1
                        jum = i
                        i = mark + 1
                        list_para.clear()
                        result = None
                        continue
                    else:
                        dict_fuh[list_four[i][3]] = int(result)
                        result = None
                list_para.clear()
            elif list_four[i][0] == '=':
                if list_four[i][1].isdigit():
                    dict_fuh[list_four[i][3]] = int(list_four[i][1])
                elif list_four[i][1] in dict_fuh.keys():
                    dict_fuh[list_four[i][3]] = dict_fuh[list_four[i][1]]
                else:
                    dict_fuh[list_four[i][3]] = dict_temp[list_four[i][1]]
            elif list_four[i][0] == '+':
                x = self.getvalue(dict_fuh, dict_temp, list_four[i][1])
                y = self.getvalue(dict_fuh, dict_temp, list_four[i][2])
                dict_temp[list_four[i][3]] = x + y
            elif list_four[i][0] == '-':
                x = self.getvalue(dict_fuh, dict_temp, list_four[i][1])
                y = self.getvalue(dict_fuh, dict_temp, list_four[i][2])
                dict_temp[list_four[i][3]] = x - y
            elif list_four[i][0] == '*':
                x = self.getvalue(dict_fuh, dict_temp, list_four[i][1])
                y = self.getvalue(dict_fuh, dict_temp, list_four[i][2])
                dict_temp[list_four[i][3]] = x * y
            elif list_four[i][0] == '/':
                x = self.getvalue(dict_fuh, dict_temp, list_four[i][1])
                y = self.getvalue(dict_fuh, dict_temp, list_four[i][2])
                dict_temp[list_four[i][3]] = x / y
            elif list_four[i][0] == '%':
                x = self.getvalue(dict_fuh, dict_temp, list_four[i][1])
                y = self.getvalue(dict_fuh, dict_temp, list_four[i][2])
                dict_temp[list_four[i][3]] = x % y
            elif list_four[i][0] == '>=':
                x = self.getvalue(dict_fuh, dict_temp, list_four[i][1])
                y = self.getvalue(dict_fuh, dict_temp, list_four[i][2])
                if x >= y:
                    dict_temp[list_four[i][3]] = 1
                else:
                    dict_temp[list_four[i][3]] = 0
            elif list_four[i][0] == '>':
                x = self.getvalue(dict_fuh, dict_temp, list_four[i][1])
                y = self.getvalue(dict_fuh, dict_temp, list_four[i][2])
                if x > y:
                    dict_temp[list_four[i][3]] = 1
                else:
                    dict_temp[list_four[i][3]] = 0
            elif list_four[i][0] == '<=':
                x = self.getvalue(dict_fuh, dict_temp, list_four[i][1])
                y = self.getvalue(dict_fuh, dict_temp, list_four[i][2])
                if x <= y:
                    dict_temp[list_four[i][3]] = 1
                else:
                    dict_temp[list_four[i][3]] = 0
            elif list_four[i][0] == '<':
                x = self.getvalue(dict_fuh, dict_temp, list_four[i][1])
                y = self.getvalue(dict_fuh, dict_temp, list_four[i][2])
                if x < y:
                    dict_temp[list_four[i][3]] = 1
                    print(dict_temp[list_four[i][3]])
                    anlsRes += "{}\n".format(dict_temp[list_four[i][3]])
                else:
                    dict_temp[list_four[i][3]] = 0
                    print(dict_temp[list_four[i][3]])
                    anlsRes += "{}\n".format(dict_temp[list_four[i][3]])
            elif list_four[i][0] == '==':
                x = self.getvalue(dict_fuh, dict_temp, list_four[i][1])
                y = self.getvalue(dict_fuh, dict_temp, list_four[i][2])
                if x == y:
                    dict_temp[list_four[i][3]] = 1
                else:
                    dict_temp[list_four[i][3]] = 0
            elif list_four[i][0] == '!=':
                x = self.getvalue(dict_fuh, dict_temp, list_four[i][1])
                y = self.getvalue(dict_fuh, dict_temp, list_four[i][2])
                if x != y:
                    dict_temp[list_four[i][3]] = 1
                else:
                    dict_temp[list_four[i][3]] = 0
            elif list_four[i][0] == 'jz':
                if dict_temp[list_four[i][1]] == 0:
                    i = int(list_four[i][3])
                    continue
            elif list_four[i][0] == 'jnz':
                if dict_temp[list_four[i][1]] != 0:
                    i = int(list_four[i][3])
                    continue
            elif list_four[i][0] == 'j':
                i = int(list_four[i][3])
                continue
            elif list_four[i][0] == 'para':
                val = self.getvalue(dict_fuh, dict_temp, list_four[i][1])
                list_para.append(val)
            elif list_four[i][0] == 'ret':
                if list_four[i][1] != '':
                    result = dict_fuh[list_four[i][1]]
                    i = jum
                    continue
                else:
                    i = jum + 1
                    continue
            if list_four[i][3] in dict_fuh.keys():
                print(list_four[i][3], '\t', dict_fuh[list_four[i][3]])
                anlsRes += "{}\t{}\n".format(list_four[i][3], dict_fuh[list_four[i][3]])
            i += 1
        return anlsRes
