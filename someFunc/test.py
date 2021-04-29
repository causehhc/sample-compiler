from someFunc.lexical.Automata import Lex_analyzer
from someFunc.parser.Statement import Match_program_stmt


def main():
    # text = open('./input.c', 'r', encoding='utf-8').read()
    text = open('./testfiles/test9.txt', 'r', encoding='utf-8').read()

    lex_anal = Lex_analyzer()
    lex_anal.set_text(text)
    token_list = lex_anal.get_token()
    for item in token_list:
        print('{}\t{}\t{}\t{}\t{}'.format(token_list.index(item), item.val, item.type, item.row, item.col))

    parser_anal = Match_program_stmt()
    parser_anal.set_tokenList(token_list)
    res, idx, tree = parser_anal.run(True)
    print(res)
    if res is False:
        print('error info:', parser_anal.info)
        print('error idx:', idx + 1)
    parser_anal.tree.show()


if __name__ == '__main__':
    main()
