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

    path1 = 'parser/forecastTable/grammer_LL(1).txt'
    path2 = 'parser/forecastTable/ff_set.txt'
    parser_anal = Parser_analyzer()
    parser_anal.load_analyzer(path1, path2)
    parser_anal.load_stack(token_list, 'program')
    # parser_anal.table_show()
    parser_anal.run(log=True)
    print(parser_anal.AST_Tree.show(stdout=False))
    parser_anal.create_dotPic('./treePic')


def main_ft_SMC():
    """
    预测分析+词法分析（生成中间代码）
    :return:
    """
    text = open('./input_temp.c', 'r', encoding='utf-8').read()
    # text = open('./testfiles/test9.txt', 'r', encoding='utf-8').read()

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
    SMC_anal.dfs_detect()


if __name__ == '__main__':
    # main_rd()
    main_ft()
    main_ft_SMC()
