from ..parser_expr.Expression_all import Match_expr


def main():
    handler = Match_expr()
    handler.set_tokenList('')
    res, i = handler.run(False)


if __name__ == '__main__':
    main()
