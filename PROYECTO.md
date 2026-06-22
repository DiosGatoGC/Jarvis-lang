# Jarvis-lang — Plan de trabajo completo

## Contexto del curso

- **Curso**: Teoría de Compiladores — 2026-2
- **Entregable**: Trabajo Parcial/Final
- **Herramientas obligatorias**: ANTLR4 + LLVM
- **Repositorio**: GitHub (URL a enviar en cada hito) + ZIP

---

## Descripción del lenguaje

**Jarvis-lang** es un lenguaje de programación con sintaxis en español natural.
El nombre proviene de la idea de dar instrucciones a un asistente ("Jarvis, crea...").

### Ejemplo de programa válido

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

---

## Estado actual del proyecto

### ✅ Completado — Front End

| Componente | Archivo | Estado |
|---|---|---|
| Gramática ANTLR4 | `JarvisLang.g4` | ✅ Completo |
| Lexer generado | `gen/JarvisLangLexer.py` | ✅ Generado |
| Parser generado | `gen/JarvisLangParser.py` | ✅ Generado |
| Análisis semántico | `semantic/semantic_visitor.py` | ✅ Completo |
| Tabla de símbolos | `semantic/symbol_table.py` | ✅ Completo |
| Manejo de errores | `semantic/errors.py` | ✅ Completo |
| Driver principal | `main.py` | ✅ Funcional |
| Tests | `tests/` | ✅ Básicos |

### ✅ Completado — Back End

| Componente | Archivo | Estado |
|---|---|---|
| Utilidades IR | `codegen/ir_builder.py` | ✅ Completo |
| Generador de LLVM IR | `codegen/ir_visitor.py` | ✅ Completo |
| Integración con clang | `main.py` | ✅ Integrado |

### ❌ Pendiente — Documentación

| Entregable | Estado |
|---|---|
| Informe en Markdown | ❌ No iniciado |
| Diagrama de arquitectura (SVG) | ❌ No iniciado |
| Plan de validación | ❌ No iniciado |
| Resultados de validación | ❌ No iniciado |
| Presentación | ❌ No iniciado |
| Video demo | ❌ No iniciado |

---

## Rúbrica de calificación

### Trabajo Parcial (Hito 1 — semana 7)

| Categoría | Bueno (4–6 pts) | Regular (3 pts) | Por mejorar (0–2 pts) |
|---|---|---|---|
| Código ANTLR4 | Cumple indicaciones, uso correcto de conceptos del curso | Cumple parcialmente | No cumple o usa conceptos no vistos |
| Exposición e Informe | Lenguaje formal, dominio del tema | Exposición inadecuada o sin dominio | No demuestra dominio |
| Preguntas | Responde correctamente | Responde parcialmente | No responde |

### Trabajo Final (Hito 3 — semana 15)

| Categoría | Bueno (4–6 pts) | Regular (3 pts) | Por mejorar (0–2 pts) |
|---|---|---|---|
| Código (Gramáticas, Arquitectura, Validación, LLVM) | Cumple indicaciones, uso correcto de conceptos | Cumple parcialmente | No cumple |
| Exposición e Informe | Lenguaje formal, dominio del tema | Exposición inadecuada | No demuestra dominio |
| Preguntas | 6–8 pts: Responde correctamente | 3–5 pts: Parcialmente | 0–2 pts: No responde |

**Criterio clave del código**: uso correcto de ANTLR4 **y** LLVM tal como se vio en clase.

---

## Hitos y entregables

### Hito 1 — Trabajo Parcial (semana 7) ✅ Base completada

- [x] Gramática ANTLR4 (`.g4`) funcional
- [x] Driver simple que parsea y analiza semánticamente
- [ ] **Informe** (máx. 4 páginas + carátula) en Markdown con:
  - [ ] Problemática y motivación
  - [ ] Objetivos del lenguaje
  - [ ] Gramática en ANTLR4 documentada
- [ ] **Video demo** de la gramática funcionando

### Hito 2 — Segundo Avance (semana 12)

- [ ] Informe actualizado con:
  - [ ] Todo lo del Hito 1
  - [ ] Gramática actualizada (si hubo cambios)
  - [ ] **Arquitectura del compilador** (diagrama SVG)
  - [ ] **Plan de validación** (casos de prueba planificados)
- [x] Repositorio con **back end implementado** (generación IR completa)

### Hito 3 — Trabajo Final (semana 15)

- [ ] Informe final con:
  - [ ] Todo lo anterior
  - [ ] **Resultados de la validación**
  - [ ] **Conclusiones**
- [x] Repositorio completo (front end + back end funcionando)
- [ ] **Presentación** (slides)
- [ ] **Video demo** del proyecto completo (máx. 10 min)
- [ ] **Sustentación presencial** — vestimenta formal profesional

---

## Decisiones técnicas

### Tipo `numero` → `double` en LLVM IR

La gramática acepta literales decimales (`3.14`), por lo tanto:

| Tipo Jarvis | Tipo LLVM | Aritmética IR | Format string printf |
|---|---|---|---|
| `numero` | `double` | `fadd`, `fsub`, `fmul`, `fdiv` | `%.6g` |
| `texto` | `i8*` | — (puntero a string) | `%s` |
| `logico` | `i1` | `and`, `or` | `%d` |

### Pipeline de compilación

```
archivo.jarvis
    → Lexer (ANTLR4)
    → Parser (ANTLR4)
    → Semantic Visitor (Python)
    → IR Visitor (Python) → archivo.ll
    → clang archivo.ll -o ejecutable
    → ./ejecutable
```

### Estrategia de generación IR

- Generar **LLVM IR textual** (archivos `.ll`) — no usar llvmlite
- Llamar `clang` desde Python con `subprocess` para compilar el `.ll`
- Satisface el requisito "uso de LLVM" del curso

---

## ✅ Back End implementado

### `codegen/ir_builder.py` — Utilidades base

- [x] Contador de registros temporales (`%t1`, `%t2`, ...)
- [x] Contador de labels (`if_true_1`, `loop_check_2`, ...)
- [x] Buffer de líneas IR con `emit()` y `emit_label()`
- [x] Declaraciones de funciones externas (`printf`, `scanf`)
- [x] Strings globales para literales texto y format strings
- [x] Helper `gep_global_str()` para getelementptr con tamaño correcto

### `codegen/ir_visitor.py` — Generador principal

| Paso | Método | IR generado | Estado |
|---|---|---|---|
| 1 | `visitVarDecl` | `alloca` + `store` (double / i8* / i1) | ✅ |
| 2 | `visitConstDecl` | `alloca` + `store` (tipo inferido) | ✅ |
| 3 | `visitAssignment` | `store` | ✅ |
| 4 | `visitFactor` / `visitAdditiveExpr` / `visitMultiplicativeExpr` | `fadd`, `fsub`, `fmul`, `fdiv` | ✅ |
| 5 | `visitPrintStmt` (numero) | `call printf` con `"%.6g\n"` | ✅ |
| 6 | `visitPrintStmt` (texto) | `call printf` con `"%s\n"` | ✅ |
| 7 | `visitPrintStmt` (logico) | `zext i1 → i32` + `call printf` con `"%d\n"` | ✅ |
| 8 | `visitAddStmt` / `SubStmt` / `MulStmt` / `DivStmt` | `load` + `fadd/fsub/fmul/fdiv` + `store` | ✅ |
| 9 | `visitIncrementStmt` / `DecrementStmt` | `load` + `fadd/fsub 1.0` + `store` | ✅ |
| 10 | `visitIfStmt` + `visitElseStmt` | `fcmp` + `br` + labels `if_true/if_false/if_end` | ✅ |
| 11 | `visitRepeatStmt` | loop con `alloca` contador + `br` condicional | ✅ |
| 12 | `visitReadStmt` | `call scanf` con `%lf` | ✅ |
| 13 | `visitComparison` | `fcmp` (`oeq`, `one`, `ogt`, `olt`, `oge`, `ole`) | ✅ |

### Integración en `main.py`

- [x] Instanciar `IRVisitor` después del análisis semántico
- [x] Escribir el `.ll` generado a disco (`salida.ll`)
- [x] Invocar `clang salida.ll -o ejecutable` con `subprocess`
- [x] Manejar errores de clang y FileNotFoundError

---

## Estructura del repositorio

```
Jarvis-lang/
├── JarvisLang.g4                   # Gramática ANTLR4
├── main.py                         # Driver principal (pipeline completo)
├── Makefile                        # Comandos de build
├── PROYECTO.md                     # Plan y seguimiento del proyecto
├── README.md                       # Instrucciones de uso
├── gen/                            # Código generado por ANTLR4
│   ├── JarvisLangLexer.py
│   ├── JarvisLangParser.py
│   ├── JarvisLangVisitor.py
│   └── JarvisLangListener.py
├── semantic/                       # Análisis semántico
│   ├── errors.py
│   ├── semantic_visitor.py
│   └── symbol_table.py
├── codegen/                        # Generación de código LLVM IR
│   ├── __init__.py
│   ├── ir_builder.py
│   └── ir_visitor.py
├── tests/                          # Casos de prueba (31 archivos)
│   ├── valido_1.txt                # Válido general: if/else, repeat, texto
│   ├── valido_2.txt                # Válido general: constantes, operaciones
│   ├── lexico_valido_1.txt         # Literales numéricos
│   ├── lexico_valido_2.txt         # Comentarios y tipos lógico/texto
│   ├── lexico_valido_3.txt         # Identificadores con _ y dígitos
│   ├── error_lexico_1.txt          # Error: símbolo '@'
│   ├── error_lexico_2.txt          # Error: símbolo '$'
│   ├── sintactico_valido_1.txt     # Declaración y print
│   ├── sintactico_valido_2.txt     # If sin else
│   ├── sintactico_valido_3.txt     # Todas las ops aritméticas
│   ├── sintactico_valido_4.txt     # Todos los operadores de comparación
│   ├── sintactico_valido_5.txt     # Anidamiento: if dentro de repeat
│   ├── error_sintactico_1.txt      # Error: falta coma tras Jarvis
│   ├── error_sintactico_2.txt      # Error: falta ':'
│   ├── error_sintactico_3.txt      # Error: falta 'Termina'
│   ├── semantico_valido_1.txt      # Variables de los tres tipos
│   ├── semantico_valido_2.txt      # Constante usada correctamente
│   ├── semantico_valido_3.txt      # Reasignación con tipo correcto
│   ├── semantico_valido_4.txt      # Expresión aritmética con variables
│   ├── semantico_valido_5.txt      # Variables en scopes de if y repeat
│   ├── error_semantico_1.txt       # Error: variable no declarada
│   ├── error_semantico_2.txt       # Error: tipo incompatible en asignación
│   ├── error_semantico_3.txt       # Error: modificar constante
│   ├── error_semantico_4.txt       # Error: comparar tipos distintos
│   ├── ir_1.txt                    # IR: aritmética, salida: 8 / 15
│   ├── ir_2.txt                    # IR: printf tres tipos, salida: 42 / Hola / 1
│   ├── ir_3.txt                    # IR: if/else, salida: grande
│   ├── ir_4.txt                    # IR: loop acumulador, salida: 40
│   ├── ir_5.txt                    # IR: potencia con repeat, salida: 8
│   ├── e2e_1.txt                   # E2E: suma 1..5, salida: 15
│   ├── e2e_2.txt                   # E2E: área rectángulo, salida: 24 / grande
│   └── e2e_3.txt                   # E2E: Celsius a Fahrenheit, salida: 212
└── docs/                           # Documentación (pendiente)
    ├── informe.md
    └── arquitectura.svg
```

---

## Plan de validación (a completar en Hito 2)

### Categorías de casos de prueba

| Categoría | Descripción | Cantidad mínima |
|---|---|---|
| Léxicos válidos | Tokens correctamente reconocidos | 3 |
| Léxicos con error | Caracteres/tokens inválidos | 2 |
| Sintácticos válidos | Estructuras gramaticales correctas | 5 |
| Sintácticos con error | Falta de palabras clave, estructura rota | 3 |
| Semánticos válidos | Tipos correctos, variables declaradas | 5 |
| Semánticos con error | Tipos incompatibles, variable no declarada, constante modificada | 4 |
| Generación IR | Programas que compilan y ejecutan correctamente | 5 |
| Integración end-to-end | Programas completos con resultado verificable | 3 |

---

## Instrucciones de instalación (a documentar)

```bash
# Dependencias
pip install antlr4-python3-runtime

# Generar lexer/parser desde la gramática
antlr4 -Dlanguage=Python3 -visitor JarvisLang.g4 -o gen/

# Ejecutar el compilador
python3 main.py tests/valido_1.txt

# (Futuro) Compilar a ejecutable
python3 main.py tests/valido_1.txt --compile
./output
```

---

## Conceptos del curso que deben reflejarse en el código

Para la rúbrica ("uso correcto de los conceptos vistos en clase"):

- **Análisis léxico**: reconocimiento de tokens con ANTLR4 ✅
- **Análisis sintáctico**: gramática LL con ANTLR4 ✅
- **Análisis semántico**: tabla de símbolos con scopes, chequeo de tipos ✅
- **Generación de IR**: LLVM IR textual con `alloca`/`store`/`load` ✅
- **Bloques básicos**: estructura de labels y `br` para control de flujo ✅
- **Lenguaje objetivo**: generar ejecutable mediante `clang` ✅

---

## Notas importantes

- Todos los documentos escritos deben estar en **formato Markdown**
- Las imágenes/diagramas deben estar en **formato SVG**
- El trabajo debe ser original — cualquier sospecha de no autoría anula el trabajo (nota 0)
- La sustentación es presencial en la semana 15 con **vestimenta formal profesional**
