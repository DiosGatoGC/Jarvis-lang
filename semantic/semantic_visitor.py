from .errors import SemanticError
from .symbol_table import SymbolTable
from gen.JarvisLangParser import JarvisLangParser
from gen.JarvisLangVisitor import JarvisLangVisitor


class SemanticVisitor(JarvisLangVisitor):
    def __init__(self):
        self.symtab = SymbolTable()
        self.errors: list[SemanticError] = []
        self._scope_counter = 0

    def _error(self, msg, ctx):
        error = SemanticError(msg, ctx.start.line)
        self.errors.append(error)
        return "error"

    def _new_scope(self, prefix, line):
        self._scope_counter += 1
        return f"{prefix}_L{line}_{self._scope_counter}"

    def _declare(self, name, type_, line, ctx, is_constant=False):
        try:
            return self.symtab.declare(
                name,
                type_,
                line,
                initialized=True,
                is_constant=is_constant,
            )
        except SemanticError as error:
            self.errors.append(error)
            return None

    def _require_assignable_number(self, name, ctx, operation):
        sym = self.symtab.lookup(name)
        if sym is None:
            self._error(f"variable '{name}' no declarada", ctx)
            return None
        sym.used = True

        if sym.is_constant:
            self._error(f"no se puede modificar la constante '{name}'", ctx)
            return None
        if sym.type_ != "numero":
            self._error(f"{operation} solo puede usarse con variables numero", ctx)
            return None
        return sym

    def visitProgram(self, ctx):
        for statement in ctx.statement():
            self.visit(statement)

    def visitVarDecl(self, ctx):
        name = ctx.ID().getText()
        declared_type = ctx.typeSpec().getText()
        expr_type = self.visit(ctx.expression())

        self._declare(name, declared_type, ctx.start.line, ctx)
        if expr_type != "error" and expr_type != declared_type:
            self._error(f"no se puede asignar {expr_type} a {declared_type}", ctx)

    def visitConstDecl(self, ctx):
        name = ctx.ID().getText()
        expr_type = self.visit(ctx.expression())
        if expr_type == "error":
            expr_type = "error"
        self._declare(name, expr_type, ctx.start.line, ctx, is_constant=True)

    def visitAssignment(self, ctx):
        name = ctx.ID().getText()
        sym = self.symtab.lookup(name)
        expr_type = self.visit(ctx.expression())

        if sym is None:
            self._error(f"variable '{name}' no declarada", ctx)
            return

        sym.used = True
        if sym.is_constant:
            self._error(f"no se puede modificar la constante '{name}'", ctx)
            return

        if expr_type != "error" and sym.type_ != expr_type:
            self._error(f"no se puede asignar {expr_type} a {sym.type_}", ctx)
            return

        sym.initialized = True

    def visitPrintStmt(self, ctx):
        self.visit(ctx.expression())

    def visitReadStmt(self, ctx):
        name = ctx.ID().getText()
        sym = self.symtab.lookup(name)
        if sym is None:
            self._error(f"variable '{name}' no declarada", ctx)
            return
        sym.used = True
        if sym.is_constant:
            self._error(f"no se puede modificar la constante '{name}'", ctx)

    def visitAddStmt(self, ctx):
        self._numeric_operation(ctx.ID().getText(), ctx.expression(), ctx, "Suma")

    def visitSubStmt(self, ctx):
        self._numeric_operation(ctx.ID().getText(), ctx.expression(), ctx, "Resta")

    def visitMulStmt(self, ctx):
        self._numeric_operation(ctx.ID().getText(), ctx.expression(), ctx, "Multiplica")

    def visitDivStmt(self, ctx):
        self._numeric_operation(ctx.ID().getText(), ctx.expression(), ctx, "Divide")

    def _numeric_operation(self, name, expr_ctx, ctx, operation):
        self._require_assignable_number(name, ctx, operation)
        expr_type = self.visit(expr_ctx)
        if expr_type != "error" and expr_type != "numero":
            self._error(f"la operacion {operation} requiere una expresion numero", ctx)

    def visitIncrementStmt(self, ctx):
        self._require_assignable_number(ctx.ID().getText(), ctx, "Aumenta")

    def visitDecrementStmt(self, ctx):
        self._require_assignable_number(ctx.ID().getText(), ctx, "Disminuye")

    def visitIfStmt(self, ctx):
        self.visit(ctx.comparison())

        self.symtab.enter_scope(self._new_scope("if", ctx.start.line))
        for statement in ctx.statement():
            self.visit(statement)
        self.symtab.exit_scope()

        if ctx.elseStmt():
            self.visit(ctx.elseStmt())

    def visitElseStmt(self, ctx):
        self.symtab.enter_scope(self._new_scope("else", ctx.start.line))
        for statement in ctx.statement():
            self.visit(statement)
        self.symtab.exit_scope()

    def visitRepeatStmt(self, ctx):
        repeat_type = self.visit(ctx.expression())
        if repeat_type != "error" and repeat_type != "numero":
            self._error("repite requiere una expresion de tipo numero", ctx)

        self.symtab.enter_scope(self._new_scope("repeat", ctx.start.line))
        for statement in ctx.statement():
            self.visit(statement)
        self.symtab.exit_scope()

    def visitComparison(self, ctx):
        left_type = self.visit(ctx.expression(0))
        right_type = self.visit(ctx.expression(1))
        if "error" in (left_type, right_type):
            return "error"

        if ctx.MAYOR() or ctx.MENOR():
            if left_type != "numero" or right_type != "numero":
                return self._error(
                    f"la comparacion requiere numero y recibio {left_type} con {right_type}",
                    ctx,
                )
            return "logico"

        if ctx.IGUAL() or ctx.DIFERENTE():
            if left_type != right_type:
                return self._error(f"no se puede comparar {left_type} con {right_type}", ctx)
            return "logico"
        return "logico"

    def visitExpression(self, ctx):
        return self.visit(ctx.additiveExpr())

    def visitAdditiveExpr(self, ctx):
        if ctx.ADDOP() is None:
            return self.visit(ctx.multiplicativeExpr())

        left_type = self.visit(ctx.additiveExpr())
        right_type = self.visit(ctx.multiplicativeExpr())
        if "error" in (left_type, right_type):
            return "error"

        if left_type != "numero" or right_type != "numero":
            return self._error(
                f"operacion aritmetica requiere numero y recibio {left_type} con {right_type}",
                ctx,
            )
        return "numero"

    def visitMultiplicativeExpr(self, ctx):
        if ctx.MULOP() is None:
            return self.visit(ctx.factor())

        left_type = self.visit(ctx.multiplicativeExpr())
        right_type = self.visit(ctx.factor())
        if "error" in (left_type, right_type):
            return "error"

        if left_type != "numero" or right_type != "numero":
            return self._error(
                f"operacion aritmetica requiere numero y recibio {left_type} con {right_type}",
                ctx,
            )
        return "numero"

    def visitFactor(self, ctx):
        if ctx.NUMBER_LIT():
            return "numero"
        if ctx.STRING_LIT():
            return "texto"
        if ctx.VERDADERO() or ctx.FALSO():
            return "logico"
        if ctx.expression():
            return self.visit(ctx.expression())

        name = ctx.ID().getText()
        sym = self.symtab.lookup(name)
        if sym is None:
            return self._error(f"variable '{name}' no declarada", ctx)
        sym.used = True
        return sym.type_
