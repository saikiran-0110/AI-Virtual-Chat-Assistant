# Pure Python (no imports) typed-command interpreter for a simple assistant.
# Goal: interpret what the user types into a structured "intent" + "entities"
# so the assistant can respond naturally.

class CommandInterpreter:
    def __init__(self):
        # Simple synonym/alias map for common intents
        self.intent_aliases = {
            "help": {"help", "h", "commands", "menu", "what can you do", "options"},
            "exit": {"exit", "quit", "q", "bye", "close"},
            "greet": {"hi", "hello", "hey", "good morning", "good afternoon", "good evening"},
            "thanks": {"thanks", "thank you", "thx", "ty"},
            "repeat": {"repeat", "say again"},
            "status": {"status", "health", "ping"},
            "calc": {"calc", "calculate", "compute", "math"},
            "note_add": {"note", "add note", "remember"},
            "note_list": {"notes", "list notes", "show notes"},
            "note_clear": {"clear notes", "delete notes", "remove notes"},
        }

        # Minimal memory for "repeat" and "notes"
        self._last_user_text = ""
        self._notes = []

    # ---------- public API ----------
    def interpret(self, user_text):
        """
        Returns a dict:
        {
          "intent": <string>,
          "confidence": <0..1>,
          "entities": <dict>,
          "raw": <original text>,
          "normalized": <normalized text>
        }
        """
        raw = user_text if user_text is not None else ""
        text = self._normalize(raw)
        self._last_user_text = raw

        if not text:
            return self._result("empty", 1.0, {}, raw, text)

        # 1) Direct slash-commands: /help, /exit, /calc 2+2
        if text.startswith("/"):
            return self._interpret_slash_command(raw, text)

        # 2) Exact/near-exact alias matches
        alias_match = self._match_alias(text)
        if alias_match:
            return self._result(alias_match, 0.95, {}, raw, text)

        # 3) Keyword/pattern rules (more natural)
        # Help-ish questions
        if self._contains_any(text, ["how do i", "how to", "what can you do", "what are you", "help me"]):
            return self._result("help", 0.85, {}, raw, text)

        # Exit-ish phrases
        if self._contains_any(text, ["i am leaving", "goodbye", "see you", "stop"]):
            return self._result("exit", 0.8, {}, raw, text)

        # Notes
        note_intent = self._interpret_notes(text, raw)
        if note_intent is not None:
            return note_intent

        # Calculation: "2+2", "calculate 10 / 2", "what is 7*9"
        calc_intent = self._interpret_calc(text, raw)
        if calc_intent is not None:
            return calc_intent

        # Fallback: treat as chat
        return self._result("chat", 0.6, {"message": raw.strip()}, raw, text)

    def handle(self, user_text):
        """
        Example handler that turns an interpreted command into a response string.
        In a real assistant, you would route intents to other modules/tools.
        """
        parsed = self.interpret(user_text)
        intent = parsed["intent"]
        entities = parsed["entities"]

        if intent == "empty":
            return "Please type a command or message."
        if intent == "help":
            return self._help_text()
        if intent == "exit":
            return "Exiting. Bye!"
        if intent == "greet":
            return "Hello! Type 'help' to see commands."
        if intent == "thanks":
            return "You are welcome."
        if intent == "repeat":
            return "You last said: " + (self._last_user_text or "")
        if intent == "status":
            return "OK"
        if intent == "note_add":
            note = entities.get("text", "").strip()
            if not note:
                return "Please provide the note text. Example: remember buy milk"
            self._notes.append(note)
            return "Saved note."
        if intent == "note_list":
            if not self._notes:
                return "No notes saved."
            out = ["Notes:"]
            for i, n in enumerate(self._notes, 1):
                out.append(str(i) + ". " + n)
            return "\n".join(out)
        if intent == "note_clear":
            self._notes = []
            return "All notes cleared."
        if intent == "calc":
            expr = entities.get("expression", "")
            ok, value_or_error = self._safe_eval_arithmetic(expr)
            return str(value_or_error) if ok else ("Calculation error: " + value_or_error)

        # chat fallback
        return "I understood this as chat: " + entities.get("message", "")

    # ---------- internal helpers ----------
    def _normalize(self, s):
        s = (s or "").strip().lower()
        # collapse repeated spaces
        while "  " in s:
            s = s.replace("  ", " ")
        return s

    def _contains_any(self, text, phrases):
        for p in phrases:
            if p in text:
                return True
        return False

    def _match_alias(self, text):
        # Try exact match and simple contains match for multi-word aliases
        for intent, aliases in self.intent_aliases.items():
            for a in aliases:
                if text == a:
                    return intent
        for intent, aliases in self.intent_aliases.items():
            for a in aliases:
                if len(a) >= 5 and a in text:
                    return intent
        return None

    def _interpret_slash_command(self, raw, text):
        # /calc 2+2  or /help
        parts = text[1:].split(" ", 1)
        cmd = parts[0].strip()
        arg = parts[1].strip() if len(parts) > 1 else ""

        if cmd in ("h", "help", "commands"):
            return self._result("help", 1.0, {}, raw, text)
        if cmd in ("q", "quit", "exit"):
            return self._result("exit", 1.0, {}, raw, text)
        if cmd in ("calc", "calculate", "math"):
            if not arg:
                return self._result("calc", 0.9, {"expression": ""}, raw, text)
            return self._result("calc", 0.95, {"expression": arg}, raw, text)

        # Unknown slash command
        return self._result("unknown_command", 0.9, {"command": cmd, "arg": arg}, raw, text)

    def _interpret_notes(self, text, raw):
        # Add note:
        # "remember buy milk" / "note buy milk" / "add note buy milk"
        # List: "notes", "list notes", "show notes"
        # Clear: "clear notes"
        if text.startswith("remember "):
            return self._result("note_add", 0.95, {"text": raw.strip()[len("remember "):]}, raw, text)
        if text.startswith("add note "):
            return self._result("note_add", 0.95, {"text": raw.strip()[len("add note "):]}, raw, text)
        if text.startswith("note "):
            return self._result("note_add", 0.9, {"text": raw.strip()[len("note "):]}, raw, text)

        if text in ("notes", "list notes", "show notes"):
            return self._result("note_list", 0.95, {}, raw, text)
        if text in ("clear notes", "delete notes", "remove notes"):
            return self._result("note_clear", 0.95, {}, raw, text)

        return None

    def _interpret_calc(self, text, raw):
        # Accept:
        # "calculate 2+2"
        # "what is 2+2"
        # "2+2"
        # "7 * 9"
        if text.startswith("calculate "):
            expr = raw.strip()[len("calculate "):].strip()
            return self._result("calc", 0.9, {"expression": expr}, raw, text)

        if text.startswith("calc "):
            expr = raw.strip()[len("calc "):].strip()
            return self._result("calc", 0.9, {"expression": expr}, raw, text)

        if text.startswith("what is "):
            expr = raw.strip()[len("what is "):].strip()
            return self._result("calc", 0.85, {"expression": expr}, raw, text)

        # If the entire message looks like an arithmetic expression, treat it as calc.
        if self._looks_like_arithmetic(text):
            return self._result("calc", 0.8, {"expression": raw.strip()}, raw, text)

        return None

    def _looks_like_arithmetic(self, text):
        allowed = "0123456789.+-*/() %"
        if not text:
            return False
        has_digit = False
        has_op = False
        for ch in text:
            if ch not in allowed:
                return False
            if ch.isdigit():
                has_digit = True
            if ch in "+-*/%":
                has_op = True
        return has_digit and has_op

    def _safe_eval_arithmetic(self, expr):
        """
        Very small safe evaluator for arithmetic with digits and + - * / % ( )
        Returns (ok: bool, value_or_error: str|number)
        No imports used. Uses Python's eval with strict character whitelist.
        """
        expr = (expr or "").strip()
        if not expr:
            return False, "No expression provided."

        allowed = "0123456789.+-*/()% "
        for ch in expr:
            if ch not in allowed:
                return False, "Unsupported character: " + ch

        # Disallow double-underscore or names (already blocked by whitelist, but keep it strict)
        if "_" in expr:
            return False, "Invalid expression."

        try:
            # Evaluate with no builtins and no variables
            value = eval(expr, {"__builtins__": None}, {})
            return True, value
        except Exception as e:
            return False, str(e)

    def _help_text(self):
        return (
            "Commands:\n"
            "- help\n"
            "- exit\n"
            "- calc <expression>  (example: calc 12/4)\n"
            "- remember <text>    (save a note)\n"
            "- notes              (list notes)\n"
            "- clear notes\n"
            "You can also use /help, /exit, /calc <expr>."
        )

    def _result(self, intent, confidence, entities, raw, normalized):
        return {
            "intent": intent,
            "confidence": float(confidence),
            "entities": dict(entities or {}),
            "raw": raw,
            "normalized": normalized
        }


# ---------- Example CLI usage ----------
if __name__ == "__main__":
    assistant = CommandInterpreter()
    print("Type 'help' for commands. Type 'exit' to quit.")
    while True:
        user = input("> ")
        response = assistant.handle(user)
        print(response)
        if assistant.interpret(user)["intent"] == "exit":
            break
