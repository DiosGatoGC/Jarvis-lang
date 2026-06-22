from gen.JarvisLangVisitor import JarvisLangVisitor
from .ir_builder import IRBuilder


class IRVisitor(JarvisLangVisitor):
    def __init__(self):
        self.builder = IRBuilder()
        self.variables = {}   # name -> alloca ptr reg (e.g. "%x")
        self.var_types = {}   # name -> "numero" | "texto" | "logico"

        # Strings de formato para printf/scanf (se pre-registran como globales)
        self.fmt_numero   = "%.6g\n"
        self.fmt_texto    = "%s\n"
        self.fmt_logico   = "%d\n"
        self.fmt_scan_num = "%lf"
        for s in [self.fmt_numero, self.fmt_texto, self.fmt_logico, self.fmt_scan_num]:
            self.builder.add_global_string(s)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _llvm_type(self, tipo):
        return {"numero": "double", "texto": "i8*", "logico": "i1"}.get(tipo, "double")

    def _llvm_ptr_type(self, tipo):
        return {"numero": "double*", "texto": "i8**", "logico": "i1*"}.get(tipo, "double*")

    def _emit_store(self, tipo, val_reg, ptr):
        lt = self._llvm_type(tipo)
        pt = self._llvm_ptr_type(tipo)
        self.builder.emit(f"store {lt} {val_reg}, {pt} {ptr}")

    def _emit_load(self, tipo, ptr):
        lt = self._llvm_type(tipo)
        pt = self._llvm_ptr_type(tipo)
        reg = self.builder.next_temp()
        self.builder.emit(f"{reg} = load {lt}, {pt} {ptr}")
        return reg

    # ------------------------------------------------------------------
    # Programa
    # ------------------------------------------------------------------

    def visitProgram(self, ctx):
        for stmt in ctx.statement():
            self.visit(stmt)
        return self.builder.get_full_ir()

    # ------------------------------------------------------------------
    # Declaraciones
    # ------------------------------------------------------------------

    def visitVarDecl(self, ctx):
        name = ctx.ID().getText()
        tipo = ctx.typeSpec().getText()
        val_reg, _ = self.visit(ctx.expression())

        ptr = f"%{name}"
        self.variables[name] = ptr
        self.var_types[name] = tipo

        lt = self._llvm_type(tipo)
        self.builder.emit(f"{ptr} = alloca {lt}")
        self._emit_store(tipo, val_reg, ptr)

    def visitConstDecl(self, ctx):
        name = ctx.ID().getText()
        val_reg, tipo = self.visit(ctx.expression())

        ptr = f"%{name}"
        self.variables[name] = ptr
        self.var_types[name] = tipo

        lt = self._llvm_type(tipo)
        self.builder.emit(f"{ptr} = alloca {lt}")
        self._emit_store(tipo, val_reg, ptr)

    def visitAssignment(self, ctx):
        name = ctx.ID().getText()
        ptr = self.variables[name]
        tipo = self.var_types[name]
        val_reg, _ = self.visit(ctx.expression())
        self._emit_store(tipo, val_reg, ptr)

    # ------------------------------------------------------------------
    # Entrada / Salida
    # ------------------------------------------------------------------

    def visitPrintStmt(self, ctx):
        val_reg, tipo = self.visit(ctx.expression())
        if tipo == "numero":
            gep = self.builder.gep_global_str(self.fmt_numero)
            self.builder.emit(
                f"call i32 (i8*, ...) @printf({gep}, double {val_reg})"
            )
        elif tipo == "texto":
            gep = self.builder.gep_global_str(self.fmt_texto)
            self.builder.emit(
                f"call i32 (i8*, ...) @printf({gep}, i8* {val_reg})"
            )
        else:  # logico
            ext = self.builder.next_temp()
            self.builder.emit(f"{ext} = zext i1 {val_reg} to i32")
            gep = self.builder.gep_global_str(self.fmt_logico)
            self.builder.emit(
                f"call i32 (i8*, ...) @printf({gep}, i32 {ext})"
            )

    def visitReadStmt(self, ctx):
        name = ctx.ID().getText()
        ptr = self.variables[name]
        # Solo soportamos leer numeros con scanf %lf -> double
        gep = self.builder.gep_global_str(self.fmt_scan_num)
        self.builder.emit(
            f"call i32 (i8*, ...) @scanf({gep}, double* {ptr})"
        )

    # ------------------------------------------------------------------
    # Operaciones aritméticas sobre variables
    # ------------------------------------------------------------------

    def _arith_op_on_var(self, name, expr_ctx, ir_op):
        ptr = self.variables[name]
        val_reg, _ = self.visit(expr_ctx)
        cur  = self._emit_load("numero", ptr)
        res  = self.builder.next_temp()
        self.builder.emit(f"{res} = {ir_op} double {cur}, {val_reg}")
        self._emit_store("numero", res, ptr)

    def visitAddStmt(self, ctx):
        self._arith_op_on_var(ctx.ID().getText(), ctx.expression(), "fadd")

    def visitSubStmt(self, ctx):
        self._arith_op_on_var(ctx.ID().getText(), ctx.expression(), "fsub")

    def visitMulStmt(self, ctx):
        self._arith_op_on_var(ctx.ID().getText(), ctx.expression(), "fmul")

    def visitDivStmt(self, ctx):
        self._arith_op_on_var(ctx.ID().getText(), ctx.expression(), "fdiv")

    def visitIncrementStmt(self, ctx):
        ptr = self.variables[ctx.ID().getText()]
        cur = self._emit_load("numero", ptr)
        res = self.builder.next_temp()
        self.builder.emit(f"{res} = fadd double {cur}, 1.0")
        self._emit_store("numero", res, ptr)

    def visitDecrementStmt(self, ctx):
        ptr = self.variables[ctx.ID().getText()]
        cur = self._emit_load("numero", ptr)
        res = self.builder.next_temp()
        self.builder.emit(f"{res} = fsub double {cur}, 1.0")
        self._emit_store("numero", res, ptr)

    # ------------------------------------------------------------------
    # Control de flujo
    # ------------------------------------------------------------------

    def visitIfStmt(self, ctx):
        cond_reg = self.visit(ctx.comparison())

        has_else = ctx.elseStmt() is not None
        lbl_true  = self.builder.next_label("if_true")
        lbl_false = self.builder.next_label("if_false") if has_else else None
        lbl_end   = self.builder.next_label("if_end")

        dest_false = f"%{lbl_false}" if has_else else f"%{lbl_end}"
        self.builder.emit(f"br i1 {cond_reg}, label %{lbl_true}, label {dest_false}")

        # Bloque then
        self.builder.emit_label(lbl_true)
        for stmt in ctx.statement():
            self.visit(stmt)
        self.builder.emit(f"br label %{lbl_end}")

        # Bloque else (opcional)
        if has_else:
            self.builder.emit_label(lbl_false)
            self.visit(ctx.elseStmt())
            self.builder.emit(f"br label %{lbl_end}")

        self.builder.emit_label(lbl_end)

    def visitElseStmt(self, ctx):
        for stmt in ctx.statement():
            self.visit(stmt)

    def visitRepeatStmt(self, ctx):
        limit_reg, _ = self.visit(ctx.expression())

        # Contador interno del loop (alloca en el bloque actual)
        counter_ptr = self.builder.next_temp()
        self.builder.emit(f"{counter_ptr} = alloca double")
        self.builder.emit(f"store double 0.0, double* {counter_ptr}")

        lbl_check = self.builder.next_label("loop_check")
        lbl_body  = self.builder.next_label("loop_body")
        lbl_end   = self.builder.next_label("loop_end")

        self.builder.emit(f"br label %{lbl_check}")

        # Verificación de condición
        self.builder.emit_label(lbl_check)
        cur_count = self._emit_load("numero", counter_ptr)
        cond_reg  = self.builder.next_temp()
        self.builder.emit(f"{cond_reg} = fcmp olt double {cur_count}, {limit_reg}")
        self.builder.emit(f"br i1 {cond_reg}, label %{lbl_body}, label %{lbl_end}")

        # Cuerpo del loop
        self.builder.emit_label(lbl_body)
        for stmt in ctx.statement():
            self.visit(stmt)
        # Incrementar contador
        cur2 = self._emit_load("numero", counter_ptr)
        new_count = self.builder.next_temp()
        self.builder.emit(f"{new_count} = fadd double {cur2}, 1.0")
        self._emit_store("numero", new_count, counter_ptr)
        self.builder.emit(f"br label %{lbl_check}")

        self.builder.emit_label(lbl_end)

    # ------------------------------------------------------------------
    # Comparaciones
    # ------------------------------------------------------------------

    def visitComparison(self, ctx):
        left_reg, _  = self.visit(ctx.expression(0))
        right_reg, _ = self.visit(ctx.expression(1))
        result = self.builder.next_temp()

        has_mayor    = ctx.MAYOR()  is not None
        has_menor    = ctx.MENOR()  is not None
        has_igual    = ctx.IGUAL()  is not None
        has_diferente= ctx.DIFERENTE() is not None
        has_o        = ctx.O()      is not None  # "mayor/menor O igual"

        if has_mayor and has_o:
            op = "oge"
        elif has_menor and has_o:
            op = "ole"
        elif has_mayor:
            op = "ogt"
        elif has_menor:
            op = "olt"
        elif has_igual:
            op = "oeq"
        else:  # diferente
            op = "one"

        self.builder.emit(f"{result} = fcmp {op} double {left_reg}, {right_reg}")
        return result

    # ------------------------------------------------------------------
    # Expresiones
    # ------------------------------------------------------------------

    def visitExpression(self, ctx):
        return self.visit(ctx.additiveExpr())

    def visitAdditiveExpr(self, ctx):
        if ctx.ADDOP() is None:
            return self.visit(ctx.multiplicativeExpr())

        left_reg, _  = self.visit(ctx.additiveExpr())
        right_reg, _ = self.visit(ctx.multiplicativeExpr())
        reg = self.builder.next_temp()
        op  = "fadd" if ctx.ADDOP().getText() == "+" else "fsub"
        self.builder.emit(f"{reg} = {op} double {left_reg}, {right_reg}")
        return reg, "numero"

    def visitMultiplicativeExpr(self, ctx):
        if ctx.MULOP() is None:
            return self.visit(ctx.factor())

        left_reg, _  = self.visit(ctx.multiplicativeExpr())
        right_reg, _ = self.visit(ctx.factor())
        reg = self.builder.next_temp()
        op  = "fmul" if ctx.MULOP().getText() == "*" else "fdiv"
        self.builder.emit(f"{reg} = {op} double {left_reg}, {right_reg}")
        return reg, "numero"

    def visitFactor(self, ctx):
        if ctx.NUMBER_LIT():
            return str(float(ctx.NUMBER_LIT().getText())), "numero"

        if ctx.STRING_LIT():
            raw = ctx.STRING_LIT().getText()[1:-1]  # quitar comillas
            str_id = self.builder.add_global_string(raw)
            reg    = self.builder.next_temp()
            size   = len(raw) + 1
            # Forma instrucción: sin paréntesis (los paréntesis son solo para expresión constante)
            self.builder.emit(
                f"{reg} = getelementptr inbounds "
                f"[{size} x i8], [{size} x i8]* {str_id}, i32 0, i32 0"
            )
            return reg, "texto"

        if ctx.VERDADERO():
            return "1", "logico"

        if ctx.FALSO():
            return "0", "logico"

        if ctx.expression():
            return self.visit(ctx.expression())

        # ID: cargar desde la variable
        name  = ctx.ID().getText()
        ptr   = self.variables[name]
        tipo  = self.var_types[name]
        reg   = self._emit_load(tipo, ptr)
        return reg, tipo
