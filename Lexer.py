class Lexer:
    """Converte texto-fonte MicroC em uma sequência de tokens."""

    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.linha = 1
        self.coluna = 1

        self.keywords = {
            "int": TokenKind.KW_INT, "bool": TokenKind.KW_BOOL,
            "void": TokenKind.KW_VOID, "true": TokenKind.KW_TRUE,
            "false": TokenKind.KW_FALSE, "if": TokenKind.KW_IF,
            "else": TokenKind.KW_ELSE, "while": TokenKind.KW_WHILE,
            "return": TokenKind.KW_RETURN, "print": TokenKind.KW_PRINT
        }

    def acabou_string(self):
        return self.pos >= len(self.source)

    def verificar_caractere(self) -> str:
        if self.acabou_string():
            return ""
        return self.source[self.pos]

    def avançar(self) -> str:
        if self.acabou_string():
            return ""

        char = self.source[self.pos]
        self.pos += 1

        if char == '\n':
            self.linha += 1
            self.coluna = 1
        else:
            self.coluna += 1

        return char

    def identificador_ou_keyword(self, primeiro_caractere:str,linha: int, coluna:int) -> Token:
        lexema=primeiro_caractere
        while not self.acabou_string() and((self.verificar_caractere().isascii() and self.verificar_caractere().isalnum()) or self.verificar_caractere() == '_'):
            lexema += self.avançar()

        tipo= self.keywords.get(lexema, TokenKind.IDENTIFIER)

        valor= lexema if tipo==TokenKind.IDENTIFIER else (True if tipo == TokenKind.KW_TRUE else(False if tipo == TokenKind.KW_FALSE else None))

        return Token(tipo, lexema, valor, linha, coluna)

    def numero(self, primeiro_caractere:str,linha: int, coluna:int) -> Token:
        lexema=primeiro_caractere
        while not self.acabou_string() and self.verificar_caractere().isdigit():
            lexema += self.avançar()

        return Token(TokenKind.INT_LITERAL, lexema, int(lexema), linha, coluna)

    def tokens(self) -> Iterator[Token]:
        """Produza todos os tokens significativos e um único EOF ao final."""
        while not self.acabou_string():
            char = self.verificar_caractere()

            if char.isspace():
                self.avançar()
                continue

            linha_começo= self.linha
            coluna_começo= self.coluna
            c= self.avançar()

            if (c.isascii() and c.isalpha()) or c== '_':
                yield self.identificador_ou_keyword(c,linha_começo,coluna_começo)
            elif c.isdigit():
                yield self.numero(c, linha_começo,coluna_começo)
            else:
                raise  LexerError(f"Caractere invalido: {c}", linha_começo, coluna_começo)

        yield Token(TokenKind.EOF,"", None, self.linha, self.coluna)

    def scan(self) -> list[Token]:
        return list(self.tokens())