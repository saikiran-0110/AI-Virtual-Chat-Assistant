import json
import os


class CalcAssistant:
    def __init__(self):
        pass

    def handle(self, user_input):
        raw = self._clean(user_input)
        low = raw.lower()

        if not raw:
            return "Type 'help' to see commands."

        if low in ("help", "h", "?"):
            return (
                "Commands:\n"
                "- calc <expression>\n"
                "Supported: + - * / ( ) decimals\n"
                "Examples:\n"
                "  calc 2 + 3 * 4\n"
                "  calc (10 - 2) / 4"
            )

        if low.startswith("calc "):
            expr = raw[5:].strip()
            if not expr:
                return "Usage: calc <expression>"
            return self._calculate(expr)

        return "Unknown command. Type 'help' to see commands."

    def _calculate(self, expr):
        tokens = self._tokenize(expr)
        if tokens is None:
            return "Invalid expression."

        rpn = self._to_rpn(tokens)
        if rpn is None:
            return "Invalid expression."

        value, err = self._eval_rpn(rpn)
        if err:
            return err

        if self._is_int_like(value):
            return str(int(value))
        return self._format_number(value)

    def _tokenize(self, s):
        s = s.strip()
        tokens = []
        i = 0
        prev_type = "START"

        while i < len(s):
            ch = s[i]

            if ch == " " or ch == "\t":
                i += 1
                continue

            if ch == "(":
                tokens.append(("LPAREN", ch))
                prev_type = "LPAREN"
                i += 1
                continue
            if ch == ")":
                tokens.append(("RPAREN", ch))
                prev_type = "RPAREN"
                i += 1
                continue

            if ch in ["+", "*", "/"]:
                tokens.append(("OP", ch))
                prev_type = "OP"
                i += 1
                continue

            if ch == "-":
                if prev_type in ["START", "OP", "LPAREN"]:
                    tokens.append(("UOP", "NEG"))
                else:
                    tokens.append(("OP", "-"))
                prev_type = "OP"
                i += 1
                continue

            if ("0" <= ch <= "9") or ch == ".":
                j = i
                dot_count = 0
                while j < len(s):
                    cj = s[j]
                    if cj == ".":
                        dot_count += 1
                        if dot_count > 1:
                            return None
                    elif not ("0" <= cj <= "9"):
                        break
                    j += 1

                num_text = s[i:j]
                if num_text == ".":
                    return None
                num_val = self._to_float(num_text)
                if num_val is None:
                    return None

                tokens.append(("NUM", num_val))
                prev_type = "NUM"
                i = j
                continue

            return None

        return tokens

    def _to_rpn(self, tokens):
        output = []
        ops = []

        prec = {
            "NEG": 3,
            "*": 2,
            "/": 2,
            "+": 1,
            "-": 1
        }

        def is_left_assoc(op):
            return op != "NEG"

        for ttype, tval in tokens:
            if ttype == "NUM":
                output.append(("NUM", tval))
                continue

            if ttype == "UOP":
                while ops:
                    top_type, top_val = ops[-1]
                    if top_type in ["OP", "UOP"]:
                        top_op = top_val
                        if (prec[top_op] > prec["NEG"]) or (prec[top_op] == prec["NEG"] and is_left_assoc("NEG")):
                            output.append(ops.pop())
                            continue
                    break
                ops.append(("UOP", "NEG"))
                continue

            if ttype == "OP":
                op = tval
                while ops:
                    top_type, top_val = ops[-1]
                    if top_type in ["OP", "UOP"]:
                        top_op = top_val
                        if (prec[top_op] > prec[op]) or (prec[top_op] == prec[op] and is_left_assoc(op)):
                            output.append(ops.pop())
                            continue
                    break
                ops.append(("OP", op))
                continue

            if ttype == "LPAREN":
                ops.append(("LPAREN", "("))
                continue

            if ttype == "RPAREN":
                found = False
                while ops:
                    top = ops.pop()
                    if top[0] == "LPAREN":
                        found = True
                        break
                    output.append(top)
                if not found:
                    return None
                continue

            return None

        while ops:
            top = ops.pop()
            if top[0] == "LPAREN":
                return None
            output.append(top)

        return output

    def _eval_rpn(self, rpn):
        stack = []
        for ttype, tval in rpn:
            if ttype == "NUM":
                stack.append(tval)
                continue

            if ttype == "UOP" and tval == "NEG":
                if len(stack) < 1:
                    return 0, "Invalid expression."
                a = stack.pop()
                stack.append(-a)
                continue

            if ttype == "OP":
                if len(stack) < 2:
                    return 0, "Invalid expression."
                b = stack.pop()
                a = stack.pop()

                if tval == "+":
                    stack.append(a + b)
                elif tval == "-":
                    stack.append(a - b)
                elif tval == "*":
                    stack.append(a * b)
                elif tval == "/":
                    if b == 0:
                        return 0, "Cannot divide by zero."
                    stack.append(a / b)
                else:
                    return 0, "Invalid expression."
                continue

            return 0, "Invalid expression."

        if len(stack) != 1:
            return 0, "Invalid expression."
        return stack[0], ""

    def _clean(self, s):
        return (s or "").strip()

    def _to_float(self, text):
        try:
            return float(text)
        except Exception:
            return None

    def _is_int_like(self, x):
        try:
            i = int(x)
        except Exception:
            return False
        return x == i

    def _format_number(self, x):
        s = str(x)
        if s in ("-0.0", "-0"):
            return "0"
        return s


class DefinitionAssistant:
    def __init__(self, file_path="glossary.json"):
        self._file_path = file_path
        self._built_in = self._default_dictionary()
        self._custom = {}
        self._load_custom()

    def _default_dictionary(self):
        return {
            "algorithm": "A step-by-step method to solve a problem or complete a task.",
            "variable": "A named place to store a value that can change.",
            "function": "A reusable block of code that does a specific job.",
            "loop": "A way to repeat a set of steps until a condition is met.",
            "debug": "To find and fix problems in code.",
            "syntax": "The rules for writing code in a language.",
            "compile": "To translate code into another form that a computer can run.",
            "execute": "To run a program or a set of instructions.",
            "integer": "A whole number without decimals.",
            "float": "A number that can have decimals.",
        }

    def _clean(self, s):
        s = (s or "").strip()
        while "  " in s:
            s = s.replace("  ", " ")
        return s

    def _normalize_word(self, w):
        w = self._clean(w).lower()
        out = []
        for ch in w:
            ok = ("a" <= ch <= "z") or ("0" <= ch <= "9") or ch == "-"
            if ok:
                out.append(ch)
        return "".join(out).strip()

    def _load_custom(self):
        if not os.path.exists(self._file_path):
            self._save_custom()
            return

        try:
            with open(self._file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    for word, definition in data.items():
                        word_norm = self._normalize_word(word)
                        if word_norm and definition and isinstance(definition, str):
                            self._custom[word_norm] = definition.strip()
        except Exception:
            pass

    def _save_custom(self):
        try:
            with open(self._file_path, "w", encoding="utf-8") as f:
                json.dump(self._custom, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def _lookup(self, word):
        if word in self._custom:
            return self._custom[word], "custom"
        if word in self._built_in:
            return self._built_in[word], "built-in"
        return "", ""

    def handle(self, user_input):
        raw = self._clean(user_input)
        low = raw.lower()

        if not raw:
            return "Type 'help' to see commands."

        if low in ("help", "h", "?"):
            return (
                "Commands:\n"
                "- calc <expression>\n"
                "- define <word>\n"
                "- addword <word> | <definition>\n"
                "- listwords\n"
                "Examples:\n"
                "  calc 2 + 3 * 4\n"
                "  define algorithm\n"
                "  addword api | A set of rules to communicate between programs\n"
                "  listwords"
            )

        if low.startswith("calc "):
            calc = CalcAssistant()
            return calc.handle(user_input)

        if low.startswith("define "):
            return self._define(raw[7:])

        if low.startswith("addword "):
            return self._addword(raw[8:])

        if low == "listwords":
            return self._listwords()

        return "Unknown command. Type 'help' to see commands."

    def _define(self, word_text):
        word = self._normalize_word(word_text)
        if not word:
            return "Usage: define <word>"

        definition, src = self._lookup(word)
        if not definition:
            return "No definition found for: " + word + ". Use: addword <word> | <definition>"

        return word + " (" + src + "): " + definition

    def _addword(self, rest):
        rest = rest.strip()
        bar = rest.find("|")
        if bar == -1:
            return "Usage: addword <word> | <definition>"

        word = self._normalize_word(rest[:bar])
        definition = rest[bar + 1:].strip()

        if not word:
            return "Word cannot be empty."
        if not definition:
            return "Definition cannot be empty."

        self._custom[word] = definition
        self._save_custom()
        return "Saved definition for: " + word

    def _listwords(self):
        all_words = []
        for w in self._built_in:
            all_words.append(w)
        for w in self._custom:
            if w not in self._built_in:
                all_words.append(w)
        all_words.sort()

        if not all_words:
            return "No words available."

        lines = ["Words:"]
        for w in all_words:
            tag = "custom" if w in self._custom else "built-in"
            lines.append("- " + w + " (" + tag + ")")
        return "\n".join(lines)


class HelpfulFallbackAssistant:
    def __init__(self):
        self._calc = CalcAssistant()
        self._defs = DefinitionAssistant(file_path="glossary.json")

    def _clean(self, s):
        s = (s or "").strip()
        while "  " in s:
            s = s.replace("  ", " ")
        return s

    def _lower(self, s):
        return (s or "").strip().lower()

    def _contains_any(self, text, words):
        for w in words:
            if w in text:
                return True
        return False

    def handle(self, user_input):
        raw = self._clean(user_input)
        low = self._lower(raw)

        if not raw:
            return "Type 'help' to see what can be done."

        if low == "help":
            return (
                "Available commands:\n"
                "- calc <expression>\n"
                "- define <word>\n"
                "- addword <word> | <definition>\n"
                "- listwords\n"
                "Examples:\n"
                "  calc 12 + 3 * 2\n"
                "  define algorithm\n"
                "  addword api | A set of rules to communicate between programs"
            )

        if low.startswith("calc "):
            return self._calc.handle(user_input)

        if low.startswith("define "):
            return self._defs.handle(user_input)

        if low.startswith("addword "):
            return self._defs.handle(user_input)

        if low == "listwords":
            return self._defs.handle(user_input)

        return self._fallback_response(raw)

    def _fallback_response(self, raw):
        low = self._lower(raw)

        if self._contains_any(low, ["calculate", "sum", "add", "minus", "multiply", "divide", "+", "-", "*", "/"]):
            return (
                "That request is not matched to a command, but it looks like a calculation.\n"
                "Try: calc 12 + 3 * 2\n"
                "Type 'help' to see all commands."
            )

        if self._contains_any(low, ["meaning", "definition", "define", "what is", "explain"]):
            return (
                "That request is not matched to a command, but it looks like a definition request.\n"
                "Try: define algorithm\n"
                "Type 'help' to see all commands."
            )

        return (
            "That command is not recognized.\n"
            "Type 'help' to see available commands.\n"
            "Examples:\n"
            "- calc 10 + 5\n"
            "- define algorithm\n"
            "- addword api | A set of rules to communicate between programs"
        )


if __name__ == "__main__":
    app = HelpfulFallbackAssistant()
    print("Helpful Assistant ready. Type 'help' for commands. Type 'exit' to quit.")
    while True:
        user = input("> ")
        if user.strip().lower() in ("exit", "quit"):
            print("Bye!")
            break
        print(app.handle(user))

