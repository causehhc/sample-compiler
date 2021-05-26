from someFunc.Interpreter.InterpreterAnls import Analyzer
from someFunc.lexical.Automata import Lex_analyzer
from someFunc.parser.forecastTable.Grammar import Parser_analyzer
from someFunc.parser.recursiveDescent.Statement import Match_program_stmt
from someFunc.semanticAndMidCode.GrammaticalGuidance import SMC_analyzer


def main_rd():
    """
    递归下降
    :return:
    """
    text = open('./input_temp.c', 'r', encoding='utf-8').read()
    # text = open('./testfiles/test1.txt', 'r', encoding='utf-8').read()

    lex_anal = Lex_analyzer()
    lex_anal.set_text(text)
    token_list, info_list = lex_anal.get_token_info()
    # for item in token_list:
    #     print('{}\t{}\t{}\t{}\t{}'.format(token_list.index(item), item.val, item.type, item.row, item.col))

    parser_anal = Match_program_stmt()
    parser_anal.set_tokenList(token_list)
    res, idx, tree, error_list = parser_anal.run(True)
    print(res)
    print(idx)
    print(error_list)
    print(parser_anal.tree.show(stdout=False))
    parser_anal.create_dotPic('./treePic')


def main_ft():
    """
    预测分析
    :return:
    """
    text = open('./input_temp.c', 'r', encoding='utf-8').read()
    # text = open('./testfiles/test9.txt', 'r', encoding='utf-8').read()

    lex_anal = Lex_analyzer()
    lex_anal.set_text(text)
    token_list, info_list = lex_anal.get_token_info()

    anlsRes = ''
    anlsLog = ''
    path1 = 'parser/forecastTable/grammer_LL(1).txt'
    path2 = 'parser/forecastTable/ff_set.txt'
    parser_anal = Parser_analyzer()
    parser_anal.load_analyzer(path1, path2)
    parser_anal.load_stack(token_list, 'program')
    anlsLog += parser_anal.table_show()
    anlsRes, log = parser_anal.run(log=True)
    anlsLog += log
    anlsLog += parser_anal.AST_Tree.show(stdout=False)
    # parser_anal.create_dotPic('./treePic')
    print(anlsRes)
    # print(anlsLog)


def main_ft_SMC():
    """
    预测分析+词法分析（生成中间代码）
    :return:
    """
    # text = open('./input_temp.c', 'r', encoding='utf-8').read()
    text = open('./testfiles/test4_1.txt', 'r', encoding='utf-8').read()

    lex_anal = Lex_analyzer()
    lex_anal.set_text(text)
    token_list, info_list = lex_anal.get_token_info()

    path1 = 'parser/forecastTable/grammer_LL(1).txt'
    path2 = 'parser/forecastTable/ff_set.txt'
    SMC_anal = SMC_analyzer()
    SMC_anal.load_analyzer(path1, path2)
    SMC_anal.load_stack(token_list, 'program')
    # parser_anal.table_show()
    SMC_anal.run(log=True)
    print(SMC_anal.AST_Tree.show(stdout=False))
    SMC_anal.create_dotPic('./treePic')

    # 宋哥必看
    symbol_table, op_stack, flag = SMC_anal.dfs_detect()  # 返回符号表及四元式组
    if flag:
        symbol_table_new = []
        op_stack_new = []
        print('符号表')
        for item in symbol_table.items():
            temp = item[0]
            symbol_table_new.append(temp)
            print(temp)
        print('中间代码')
        for item in op_stack:
            temp = [item.op, item.a1, item.a2, item.res]
            op_stack_new.append(temp)
            print(op_stack.index(item), temp)
    else:
        print(symbol_table)
        print(op_stack)


def main():
    """
    预测分析+词法分析（生成中间代码）+解释器
    :return:
    """
    text = open('./input_temp.c', 'r', encoding='utf-8').read()
    # text = open('./testfiles/test1.txt', 'r', encoding='utf-8').read()

    lex_anal = Lex_analyzer()
    lex_anal.set_text(text)
    token_list, info_list = lex_anal.get_token_info()

    path1 = 'parser/forecastTable/grammer_LL(1).txt'
    path2 = 'parser/forecastTable/ff_set.txt'
    SMC_anal = SMC_analyzer()
    SMC_anal.load_analyzer(path1, path2)
    SMC_anal.load_stack(token_list, 'program')
    # parser_anal.table_show()
    SMC_anal.run(log=True)
    # print(SMC_anal.AST_Tree.show(stdout=False))
    # SMC_anal.create_dotPic('./treePic')

    # 宋哥必看
    symbol_table, op_stack, flag = SMC_anal.dfs_detect()  # 返回符号表及四元式组
    symbol_table_new = []
    op_stack_new = []
    list_hs = []
    for item in symbol_table.items():
        temp = item[0]
        symbol_table_new.append(temp)
    for item in op_stack:
        temp = [item.op, item.a1, item.a2, item.res]
        op_stack_new.append(temp)
        print(op_stack_new.index(temp), temp)


    inter_anls = Analyzer()
    dict_fuh = {
        'temp': 0,
    }
    for fuh in symbol_table_new:
        dict_fuh[fuh] = 0
    inter_anls.jieshiqi(dict_fuh, op_stack_new, list_hs)


if __name__ == '__main__':
    # main_rd()
    # main_ft()
    # main_ft_SMC()
    main()

