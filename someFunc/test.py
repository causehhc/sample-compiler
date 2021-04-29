from someFunc.lexical.Automata import Lex_analyzer
from someFunc.parser.Statement import Match_program_stmt


def create_dotPic(parser_anal):
    import graphviz
    root_dir = './treePic'
    parser_anal.tree.to_graphviz(filename='{}/tree.dot'.format(root_dir))
    string = open('{}/tree.dot'.format(root_dir)).read()
    dot = graphviz.Source(string)
    dot.render('{}/tree'.format(root_dir), format='png')


def main():
    text = open('./input.c', 'r', encoding='utf-8').read()
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
    # print(parser_anal.tree.show(stdout=False))
    # create_dotPic(parser_anal)


if __name__ == '__main__':
    main()
