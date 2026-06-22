# Jarvis-lang

Jarvis-lang es un lenguaje de programación con sintaxis en español natural. El nombre refleja la idea de dar instrucciones a un asistente: el programador le habla a "Jarvis" y este ejecuta las órdenes.

Es un proyecto académico del curso **Teoría de Compiladores** que implementa un compilador completo utilizando **ANTLR4** para el análisis léxico/sintáctico y **LLVM IR** como lenguaje intermedio, produciendo ejecutables nativos mediante **clang**.

## Ejemplo de programa

```
Jarvis, crea numero x con 10
Jarvis, crea texto msg con "Hola"
Dime msg
Jarvis, si x es mayor que 5:
    Dime "x es grande"
Si no:
    Dime "x es chico"
Termina
Jarvis, repite 3 veces:
    Suma 1 a x
Termina
Dime x
```

## Pipeline de compilación

```
archivo.jarvis
    → Lexer (ANTLR4)
    → Parser (ANTLR4)
    → Análisis Semántico
    → Generación de LLVM IR  →  salida.ll
    → clang                  →  ./ejecutable
```

## Requisitos

- Python 3.10 o superior
- Java (para ejecutar ANTLR4, solo si se regenera el lexer/parser)
- clang

```bash
pip install antlr4-python3-runtime
sudo apt-get install -y clang
```

## Ejecución

```bash
python3 main.py <archivo.jarvis>
```

El compilador realiza los cuatro pasos automáticamente: analiza el código, genera el archivo `salida.ll` con el IR de LLVM, llama a clang para producir el ejecutable `./ejecutable` y muestra el resultado.

**Ejemplo:**

```bash
python3 main.py tests/e2e_3.txt
./ejecutable
```

Salida:
```
Temperatura en Fahrenheit:
212
```

## Regenerar el Lexer y Parser (opcional)

Solo es necesario si se modifica la gramática `JarvisLang.g4`:

```bash
antlr4 -Dlanguage=Python3 -visitor JarvisLang.g4 -o gen/
```

## Tipos de datos

| Tipo Jarvis | Descripción       | Ejemplo                          |
|-------------|-------------------|----------------------------------|
| `numero`    | Punto flotante    | `Jarvis, crea numero x con 3.14` |
| `texto`     | Cadena de texto   | `Jarvis, crea texto s con "Hola"`|
| `logico`    | Booleano          | `Jarvis, crea logico b con verdadero` |

## Referencia rápida del lenguaje

| Instrucción                          | Descripción                     |
|--------------------------------------|---------------------------------|
| `Jarvis, crea <tipo> <id> con <expr>`| Declarar variable               |
| `Jarvis, fija <id> con <expr>`       | Declarar constante              |
| `Jarvis, cambia <id> a <expr>`       | Reasignar variable              |
| `Dime <expr>`                        | Imprimir valor                  |
| `Escucha <id>`                       | Leer número del usuario         |
| `Suma <expr> a <id>`                 | `id = id + expr`                |
| `Resta <expr> a <id>`                | `id = id - expr`                |
| `Multiplica <id> por <expr>`         | `id = id * expr`                |
| `Divide <id> entre <expr>`           | `id = id / expr`                |
| `Aumenta <id>`                       | `id = id + 1`                   |
| `Disminuye <id>`                     | `id = id - 1`                   |
| `Jarvis, si <cond>: ... Termina`     | Condicional                     |
| `Si no: ...`                         | Rama else (opcional)            |
| `Jarvis, repite <n> veces: ...Termina`| Bucle n iteraciones            |

## Ejecutar los tests

```bash
# Un test individual
python3 main.py tests/valido_1.txt

# Todos los tests válidos (deben compilar y ejecutar)
for f in tests/valido_*.txt tests/lexico_valido_*.txt tests/sintactico_valido_*.txt \
          tests/semantico_valido_*.txt tests/ir_*.txt tests/e2e_*.txt; do
    echo "=== $f ===" && python3 main.py "$f"
done

# Tests de error (deben mostrar el error correspondiente)
for f in tests/error_*.txt; do
    echo "=== $f ===" && python3 main.py "$f"
done
```
