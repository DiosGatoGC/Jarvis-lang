grammar JarvisLang;

// ========== REGLAS DEL PARSER ==========

program
    : statement* EOF
    ;

statement
    : varDecl
    | constDecl
    | assignment
    | printStmt
    | readStmt
    | addStmt
    | subStmt
    | mulStmt
    | divStmt
    | incrementStmt
    | decrementStmt
    | ifStmt
    | repeatStmt
    ;

varDecl
    : JARVIS COMMA CREA typeSpec ID CON expression
    ;

constDecl
    : JARVIS COMMA FIJA ID CON expression
    ;

assignment
    : JARVIS COMMA CAMBIA ID A expression
    ;

printStmt
    : DIME expression
    ;

readStmt
    : ESCUCHA ID
    ;

addStmt
    : SUMA expression A ID
    ;

subStmt
    : RESTA expression A ID
    ;

mulStmt
    : MULTIPLICA ID POR expression
    ;

divStmt
    : DIVIDE ID ENTRE expression
    ;

incrementStmt
    : AUMENTA ID
    ;

decrementStmt
    : DISMINUYE ID
    ;

ifStmt
    : JARVIS COMMA SI comparison COLON statement* elseStmt? TERMINA
    ;

elseStmt
    : SI_CAP NO COLON statement*
    ;

repeatStmt
    : JARVIS COMMA REPITE expression VECES COLON statement* TERMINA
    ;

typeSpec
    : NUMERO_TYPE
    | TEXTO_TYPE
    | LOGICO_TYPE
    ;

comparison
    : expression ES IGUAL A expression
    | expression ES DIFERENTE DE expression
    | expression ES MAYOR QUE expression
    | expression ES MENOR QUE expression
    | expression ES MAYOR O IGUAL QUE expression
    | expression ES MENOR O IGUAL QUE expression
    ;

expression
    : additiveExpr
    ;

additiveExpr
    : additiveExpr ADDOP multiplicativeExpr
    | multiplicativeExpr
    ;

multiplicativeExpr
    : multiplicativeExpr MULOP factor
    | factor
    ;

factor
    : NUMBER_LIT
    | STRING_LIT
    | VERDADERO
    | FALSO
    | ID
    | LPAREN expression RPAREN
    ;

// ========== REGLAS DEL LEXER ==========

JARVIS      : 'Jarvis';
CREA        : 'crea';
FIJA        : 'fija';
CON         : 'con';
CAMBIA      : 'cambia';
A           : 'a';
DIME        : 'Dime';
ESCUCHA     : 'Escucha';

SUMA        : 'Suma';
RESTA       : 'Resta';
MULTIPLICA  : 'Multiplica';
DIVIDE      : 'Divide';
AUMENTA     : 'Aumenta';
DISMINUYE   : 'Disminuye';

SI          : 'si';
SI_CAP      : 'Si';
NO          : 'no';
REPITE      : 'repite';
VECES       : 'veces';
TERMINA     : 'Termina';

NUMERO_TYPE : 'numero';
TEXTO_TYPE  : 'texto';
LOGICO_TYPE : 'logico';

VERDADERO   : 'verdadero';
FALSO       : 'falso';

ES          : 'es';
IGUAL       : 'igual';
DIFERENTE   : 'diferente';
DE          : 'de';
MAYOR       : 'mayor';
MENOR       : 'menor';
O           : 'o';
QUE         : 'que';
POR         : 'por';
ENTRE       : 'entre';

ADDOP       : '+' | '-';
MULOP       : '*' | '/';

COMMA       : ',';
COLON       : ':';
LPAREN      : '(';
RPAREN      : ')';

NUMBER_LIT  : [0-9]+ ('.' [0-9]+)?;
STRING_LIT  : '"' ~["\r\n]* '"';

ID          : [a-zA-Z_] [a-zA-Z_0-9]*;

LINE_COMMENT  : '//' ~[\r\n]* -> skip;
BLOCK_COMMENT : '/*' .*? '*/' -> skip;

WS          : [ \t\r\n]+ -> skip;
