import sys

from antlr4 import CommonTokenStream, FileStream

from gen.JarvisLangLexer import JarvisLangLexer
from gen.JarvisLangParser import JarvisLangParser
from semantic.errors import CustomErrorListener
from semantic.semantic_visitor import SemanticVisitor


def main():
    if len(sys.argv) != 2:
        print("Uso: python3 main.py archivo.txt")
        return

    archivo = sys.argv[1]
    input_stream = FileStream(archivo, encoding="utf-8")

    error_listener = CustomErrorListener()

    lexer = JarvisLangLexer(input_stream)
    lexer.removeErrorListeners()
    lexer.addErrorListener(error_listener)

    stream = CommonTokenStream(lexer)
    parser = JarvisLangParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)

    tree = parser.program()

    if error_listener.errors:
        for error in error_listener.errors:
            print(error)
        return

    visitor = SemanticVisitor()
    visitor.visit(tree)

    if visitor.errors:
        for error in visitor.errors:
            print(error)
        return

    print("Código aceptado correctamente.")

    warns = visitor.symtab.unused_warnings()
    if warns:
        print("\n=== ADVERTENCIAS ===")
        for warning in warns:
            print(warning)

#Ejecutar main
main()
