from antlr4 import Lexer
from antlr4.error.ErrorListener import ErrorListener


class CompilationError:
    def __init__(self, kind: str, message: str, line: int = 0):
        self.kind = kind
        self.message = message
        self.line = line

    def __str__(self):
        return f"[Error {self.kind}, línea {self.line}] {self.message}"


class SemanticError(Exception):
    def __init__(self, message: str, line: int = 0):
        super().__init__(f"[Error Semántico, línea {line}] {message}")
        self.line = line


class CustomErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()
        self.errors: list[CompilationError] = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        if isinstance(recognizer, Lexer):
            self.errors.append(CompilationError("Léxico", self._lexer_message(msg), line))
            return

        token_text = getattr(offendingSymbol, "text", None)
        self.errors.append(CompilationError("Sintáctico", self._parser_message(msg, token_text), line))

    def _lexer_message(self, msg: str) -> str:
        marker = "token recognition error at: "
        if marker in msg:
            text = msg.split(marker, 1)[1].strip("'")
            return f"simbolo no reconocido: '{text}'"
        return msg

    def _parser_message(self, msg: str, token_text: str | None) -> str:
        if token_text == "<EOF>":
            return "entrada incompleta o falta 'Termina' para cerrar el bloque"
        if "missing ':'" in msg:
            return "falta ':' al final de la instruccion"
        if "missing ','" in msg:
            return "falta ',' despues de Jarvis"
        if token_text:
            return f"entrada inesperada cerca de '{token_text}'"
        return msg
