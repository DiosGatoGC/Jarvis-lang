from .errors import SemanticError


class Symbol:
    def __init__(self, name, type_, scope, line, initialized=False, is_constant=False):
        self.name = name
        self.type_ = type_
        self.scope = scope
        self.line = line
        self.initialized = initialized
        self.used = False
        self.is_constant = is_constant

    def __repr__(self):
        kind = "const" if self.is_constant else "var"
        return f"Symbol({kind} {self.name}: {self.type_} @ {self.scope}, line {self.line})"


class SymbolTable:
    def __init__(self):
        self._table: dict[str, dict[str, Symbol]] = {"global": {}}
        self._scope_stack: list[str] = ["global"]

    @property
    def current_scope(self) -> str:
        return self._scope_stack[-1]

    def enter_scope(self, name: str):
        self._scope_stack.append(name)
        self._table.setdefault(name, {})

    def exit_scope(self):
        if len(self._scope_stack) > 1:
            self._scope_stack.pop()

    def declare(
        self,
        name: str,
        type_: str,
        line: int,
        initialized: bool = True,
        is_constant: bool = False,
    ) -> Symbol:
        scope = self.current_scope
        if name in self._table.setdefault(scope, {}):
            raise SemanticError(f"simbolo '{name}' ya declarado en este ambito", line)

        sym = Symbol(name, type_, scope, line, initialized, is_constant)
        self._table[scope][name] = sym
        return sym

    def lookup(self, name: str) -> Symbol | None:
        for scope in reversed(self._scope_stack):
            if name in self._table.get(scope, {}):
                return self._table[scope][name]
        return None

    def unused_warnings(self) -> list[str]:
        warns = []
        for scope_syms in self._table.values():
            for sym in scope_syms.values():
                if not sym.used and not sym.is_constant:
                    warns.append(
                        f"ADVERTENCIA: '{sym.name}' declarada en linea {sym.line} nunca fue usada."
                    )
        return warns
