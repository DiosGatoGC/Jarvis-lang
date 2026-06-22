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
    
    print("Iniciando la generación de código intermedio (LLVM IR)...")
    
    from codegen.ir_visitor import IRVisitor
    import subprocess

    # 1. Instanciar el visitor de código intermedio y recorrer el AST
    ir_visitor = IRVisitor()
    llvm_ir = ir_visitor.visit(tree)

    # 2. Guardar el LLVM IR generado en un archivo de texto plano
    output_ll = "salida.ll"
    with open(output_ll, "w") as f:
        f.write(llvm_ir)
    print(f"Archivo de representación intermedia guardado como: {output_ll}")

    # 3. Invocar a Clang mediante un subproceso para crear el binario ejecutable
    try:
        nombre_ejecutable = "./ejecutable"
        # Ejecuta el comando nativo: clang salida.ll -o ./ejecutable
        subprocess.run(["clang", output_ll, "-o", nombre_ejecutable], check=True)
        print(f"¡Compilación nativa completada con éxito! Ejecutable creado: 	  {nombre_ejecutable}")
    except subprocess.CalledProcessError as e:
        print("Error durante la compilación nativa con Clang:", e)
    except FileNotFoundError:
        print("Error: No se encontró 'clang' instalado en el sistema operativo.")
   

    warns = visitor.symtab.unused_warnings()
    if warns:
        print("\n=== ADVERTENCIAS ===")
        for warning in warns:
            print(warning)

#Ejecutar main
main()
