class CommandInterpreter:
    def __init__(self):
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
        self._last_user_text = ""
        self._notes = []
        self._actions = self._build_actions()

    def _validate_result(self, result):
        if not isinstance(result, dict):
            return False
        required_keys = ["intent", "confidence", "entities", "raw", "normalized"]
        if not all(key in result for key in required_keys):
            return False
        if not isinstance(result["intent"], str):
            return False
        if not isinstance(result["confidence"], (int, float)) or not (0.0 <= result["confidence"] <= 1.0):
            return False
        if not isinstance(result["entities"], dict):
            return False
        return True

    def _validate_action(self, action):
        if not isinstance(action, dict):
            return False
        required_keys = ["aliases", "usage", "description"]
        if not all(key in action for key in required_keys):
            return False
        if not isinstance(action["aliases"], (list, tuple)):
            return False
        if not isinstance(action["usage"], str):
            return False
        if not isinstance(action["description"], str):
            return False
        return True

    def _build_actions(self):
        actions = {
            "help": {
                "aliases": ["help", "h", "commands", "menu", "/help", "what can you do", "options"],
                "usage": "help",
                "description": "Show all available actions and how to use them.",
            },
            "exit": {
                "aliases": ["exit", "quit", "q", "bye", "/exit", "/quit", "close"],
                "usage": "exit",
                "description": "Exit the assistant.",
            },
            "greet": {
                "aliases": ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"],
                "usage": "hello",
                "description": "Greet the assistant.",
            },
            "thanks": {
                "aliases": ["thanks", "thank you", "thx", "ty"],
                "usage": "thanks",
                "description": "Thank the assistant.",
            },
            "repeat": {
                "aliases": ["repeat", "say again"],
                "usage": "repeat",
                "description": "Repeat the last user input.",
            },
            "status": {
                "aliases": ["status", "ping", "health", "/status"],
                "usage": "status",
                "description": "Check if the assistant is running.",
            },
            "calc": {
                "aliases": ["calc", "calculate", "compute", "math", "/calc"],
                "usage": "calc <expression>",
                "description": "Calculate a mathematical expression. Example: calc 2+2",
            },
            "note_add": {
                "aliases": ["note", "add note", "remember"],
                "usage": "remember <text>",
                "description": "Save a note. Example: remember buy milk",
            },
            "note_list": {
                "aliases": ["notes", "list notes", "show notes"],
                "usage": "notes",
                "description": "List all saved notes.",
            },
            "note_clear": {
                "aliases": ["clear notes", "delete notes", "remove notes"],
                "usage": "clear notes",
                "description": "Clear all saved notes.",
            },
        }
        validated_actions = {}
        for key, action in actions.items():
            if self._validate_action(action):
                validated_actions[key] = action
        return validated_actions

    def _result(self, intent, confidence, entities, raw, normalized):
        result = {
            "intent": str(intent) if intent else "",
            "confidence": float(confidence) if isinstance(confidence, (int, float)) else 0.0,
            "entities": dict(entities) if isinstance(entities, dict) else {},
            "raw": str(raw) if raw is not None else "",
            "normalized": str(normalized) if normalized is not None else ""
        }
        if not self._validate_result(result):
            return {
                "intent": "error",
                "confidence": 0.0,
                "entities": {},
                "raw": str(raw) if raw is not None else "",
                "normalized": str(normalized) if normalized is not None else ""
            }
        return result

    def interpret(self, user_text):
        raw = user_text if user_text is not None else ""
        text = self._normalize(raw)
        self._last_user_text = raw

        if not text:
            return self._result("empty", 1.0, {}, raw, text)

        if text.startswith("/"):
            return self._interpret_slash_command(raw, text)

        alias_match = self._match_alias(text)
        if alias_match:
            return self._result(alias_match, 0.95, {}, raw, text)

        if self._contains_any(text, ["how do i", "how to", "what can you do", "what are you", "help me"]):
            return self._result("help", 0.85, {}, raw, text)

        if self._contains_any(text, ["i am leaving", "goodbye", "see you", "stop"]):
            return self._result("exit", 0.8, {}, raw, text)

        note_intent = self._interpret_notes(text, raw)
        if note_intent is not None:
            return note_intent

        calc_intent = self._interpret_calc(text, raw)
        if calc_intent is not None:
            return calc_intent

        return self._result("unknown_command", 0.7, {"command": text, "raw": raw}, raw, text)

    def handle(self, user_text):
        parsed = self.interpret(user_text)
        if not self._validate_result(parsed):
            return "Error processing command."
        
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
            note = entities.get("text", "").strip() if isinstance(entities, dict) else ""
            if not note:
                return "Please provide the note text. Example: remember buy milk"
            if isinstance(self._notes, list):
                self._notes.append(note)
            return "Saved note."
        if intent == "note_list":
            if not isinstance(self._notes, list) or not self._notes:
                return "No notes saved."
            out = ["Notes:"]
            for i, n in enumerate(self._notes, 1):
                out.append(str(i) + ". " + str(n))
            return "\n".join(out)
        if intent == "note_clear":
            self._notes = []
            return "All notes cleared."
        if intent == "calc":
            expr = entities.get("expression", "").strip() if isinstance(entities, dict) else ""
            ok, value_or_error = self._safe_eval_arithmetic(expr)
            return str(value_or_error) if ok else ("Calculation error: " + str(value_or_error))
        
        if intent == "unknown_command":
            cmd = entities.get("command", "").strip() if isinstance(entities, dict) else ""
            if not cmd:
                cmd = entities.get("raw", "").strip() if isinstance(entities, dict) else ""
            return self._unknown_command_message(cmd)

        message = entities.get("message", "") if isinstance(entities, dict) else ""
        return "I understood this as chat: " + str(message)

    def _normalize(self, s):
        s = (s or "").strip().lower()
        while "  " in s:
            s = s.replace("  ", " ")
        return s

    def _contains_any(self, text, phrases):
        if not isinstance(text, str) or not isinstance(phrases, (list, tuple)):
            return False
        for p in phrases:
            if isinstance(p, str) and p in text:
                return True
        return False

    def _match_alias(self, text):
        if not isinstance(text, str) or not isinstance(self.intent_aliases, dict):
            return None
        for intent, aliases in self.intent_aliases.items():
            if not isinstance(aliases, (set, list, tuple)):
                continue
            for a in aliases:
                if isinstance(a, str) and text == a:
                    return intent
        for intent, aliases in self.intent_aliases.items():
            if not isinstance(aliases, (set, list, tuple)):
                continue
            for a in aliases:
                if isinstance(a, str) and len(a) >= 5 and a in text:
                    return intent
        return None

    def _interpret_slash_command(self, raw, text):
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

        return self._result("unknown_command", 0.9, {"command": cmd, "arg": arg}, raw, text)

    def _interpret_notes(self, text, raw):
        if not isinstance(text, str) or not isinstance(raw, str):
            return None
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
        if not isinstance(text, str) or not isinstance(raw, str):
            return None
        if text.startswith("calculate "):
            expr = raw.strip()[len("calculate "):].strip()
            return self._result("calc", 0.9, {"expression": expr}, raw, text)

        if text.startswith("calc "):
            expr = raw.strip()[len("calc "):].strip()
            return self._result("calc", 0.9, {"expression": expr}, raw, text)

        if text.startswith("what is "):
            expr = raw.strip()[len("what is "):].strip()
            return self._result("calc", 0.85, {"expression": expr}, raw, text)

        if self._looks_like_arithmetic(text):
            return self._result("calc", 0.8, {"expression": raw.strip()}, raw, text)

        return None

    def _looks_like_arithmetic(self, text):
        if not isinstance(text, str):
            return False
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
        expr = (expr or "").strip()
        if not isinstance(expr, str) or not expr:
            return False, "No expression provided."

        allowed = "0123456789.+-*/()% "
        for ch in expr:
            if ch not in allowed:
                return False, "Unsupported character: " + ch

        if "_" in expr:
            return False, "Invalid expression."

        try:
            value = eval(expr, {"__builtins__": None}, {})
            return True, value
        except Exception as e:
            return False, str(e)

    def _help_text(self):
        if not isinstance(self._actions, dict):
            return "Help information unavailable."
        lines = []
        lines.append("Available actions:")
        lines.append("")
        keys = list(self._actions.keys())
        keys.sort()

        for name in keys:
            info = self._actions.get(name)
            if not isinstance(info, dict):
                continue
            aliases = info.get("aliases", [])
            usage = info.get("usage", "")
            description = info.get("description", "")
            if isinstance(aliases, (list, tuple)):
                alias_str = ", ".join(str(a) for a in aliases)
            else:
                alias_str = ""
            lines.append("- " + str(usage))
            lines.append("  " + str(description))
            lines.append("  Aliases: " + alias_str)
            lines.append("")

        lines.append("Examples:")
        lines.append("  help")
        lines.append("  calc 2+2")
        lines.append("  remember buy milk")
        lines.append("  notes")
        lines.append("  exit")
        lines.append("")
        lines.append("Tip: If a command is unknown, type 'help' to see valid commands.")
        return "\n".join(lines).rstrip()

    def _suggest_commands(self, unknown_cmd, limit=3):
        unknown_cmd = (unknown_cmd or "").lower().strip()
        if not isinstance(unknown_cmd, str) or not unknown_cmd:
            return []

        if not isinstance(self._actions, dict):
            return []

        candidates = []
        for name, info in self._actions.items():
            if isinstance(name, str):
                candidates.append(name)
            if isinstance(info, dict):
                aliases = info.get("aliases", [])
                if isinstance(aliases, (list, tuple)):
                    for a in aliases:
                        if isinstance(a, str):
                            cleaned = a.lower().lstrip("/")
                            if cleaned not in candidates:
                                candidates.append(cleaned)

        picks = []

        for c in candidates:
            if isinstance(c, str) and c.startswith(unknown_cmd):
                picks.append(c)

        if len(picks) < limit and unknown_cmd:
            first_char = unknown_cmd[0] if unknown_cmd else ""
            for c in candidates:
                if isinstance(c, str) and c and c[0] == first_char and c not in picks:
                    picks.append(c)

        if len(picks) < limit:
            for c in candidates:
                if isinstance(c, str) and unknown_cmd in c and c not in picks:
                    picks.append(c)

        final = []
        for p in picks:
            if p not in final:
                final.append(p)

        return final[:limit] if isinstance(limit, int) and limit > 0 else []

    def _unknown_command_message(self, cmd):
        if not isinstance(cmd, str):
            cmd = ""
        msg_lines = []
        msg_lines.append("Unknown command: '" + cmd + "'.")
        msg_lines.append("Type 'help' to see all available actions.")

        suggestions = self._suggest_commands(cmd)
        if isinstance(suggestions, list) and suggestions:
            suggestion_str = ", ".join(str(s) for s in suggestions)
            msg_lines.append("Did you mean: " + suggestion_str + " ?")

        return "\n".join(msg_lines)


if __name__ == "__main__":
    assistant = CommandInterpreter()
    print("Assistant ready. Type 'help' to see available actions.")
    while True:
        user = input("> ")
        response = assistant.handle(user)
        print(response)
        parsed = assistant.interpret(user)
        if isinstance(parsed, dict) and parsed.get("intent") == "exit":
            break

