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


if __name__ == "__main__":
    app = CalcAssistant()
    print("Calc Assistant ready. Type 'help' for commands. Type 'exit' to quit.")
    while True:
        user = input("> ")
        if user.strip().lower() in ("exit", "quit"):
            print("Bye!")
            break
        print(app.handle(user))

