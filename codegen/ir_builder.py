class IRBuilder:
    def __init__(self):
        self.lines = []
        self.temp_counter = 0
        self.label_counter = 0
        self.global_strings = {}  # value -> @str_N

    def next_temp(self):
        self.temp_counter += 1
        return f"%t{self.temp_counter}"

    def next_label(self, prefix="label"):
        self.label_counter += 1
        return f"{prefix}_{self.label_counter}"

    def emit(self, instruction):
        self.lines.append(f"    {instruction}")

    def emit_label(self, label):
        self.lines.append(f"{label}:")

    def add_global_string(self, value):
        if value not in self.global_strings:
            self.global_strings[value] = f"@str_{len(self.global_strings)}"
        return self.global_strings[value]

    def gep_global_str(self, value):
        """Genera la expresión getelementptr para un string global."""
        str_id = self.global_strings[value]
        size = len(value) + 1  # +1 para el null terminator
        return f"i8* getelementptr inbounds ([{size} x i8], [{size} x i8]* {str_id}, i32 0, i32 0)"

    def get_full_ir(self):
        header = [
            '; ModuleID = "JarvisLangPrograma"',
            'target triple = "x86_64-pc-linux-gnu"',
            'target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"',
            '',
            'declare i32 @printf(i8*, ...)',
            'declare i32 @scanf(i8*, ...)',
            '',
        ]

        globals_lines = []
        for val, str_id in self.global_strings.items():
            escaped = val.replace("\\", "\\5C").replace("\n", "\\0A").replace('"', "\\22")
            escaped += "\\00"
            length = len(val) + 1
            globals_lines.append(
                f'{str_id} = private unnamed_addr constant [{length} x i8] c"{escaped}"'
            )

        main_header = [
            '',
            'define i32 @main() {',
            'entry:',
        ]

        main_footer = [
            '    ret i32 0',
            '}',
        ]

        return "\n".join(header + globals_lines + main_header + self.lines + main_footer)
