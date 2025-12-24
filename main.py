class Assistant:
    def __init__(self):
        self._actions = self._build_actions()
        self._history = []

    def _validate_action(self, action):
        if not isinstance(action, dict):
            return False
        required_keys = ["aliases", "usage", "description", "handler"]
        if not all(key in action for key in required_keys):
            return False
        if not isinstance(action["aliases"], (list, tuple)):
            return False
        if not isinstance(action["usage"], str):
            return False
        if not isinstance(action["description"], str):
            return False
        if not callable(action["handler"]):
            return False
        return True

    def _validate_history_entry(self, entry):
        if not isinstance(entry, dict):
            return False
        if "input" not in entry or "output" not in entry:
            return False
        if not isinstance(entry["input"], str):
            return False
        if not isinstance(entry["output"], str):
            return False
        return True

    def _build_actions(self):
        actions = {
            "help": {
                "aliases": ["help", "h", "commands", "menu", "/help"],
                "usage": "help",
                "description": "Show all available actions and how to use them.",
                "handler": self._cmd_help
            },
            "exit": {
                "aliases": ["exit", "quit", "q", "bye", "/exit", "/quit"],
                "usage": "exit",
                "description": "Exit the assistant.",
                "handler": self._cmd_exit
            },
            "status": {
                "aliases": ["status", "ping", "health", "/status"],
                "usage": "status",
                "description": "Check if the assistant is running.",
                "handler": self._cmd_status
            },
            "echo": {
                "aliases": ["echo", "/echo"],
                "usage": "echo <message>",
                "description": "Repeat back the message.",
                "handler": self._cmd_echo
            },
            "history": {
                "aliases": ["history", "log", "logs", "show history", "show log", "/history"],
                "usage": "history OR history <number>",
                "description": "Show past commands and assistant responses (optionally last N).",
                "handler": self._cmd_history
            },
            "clear_history": {
                "aliases": ["clear history", "clear log", "clear logs", "/clear_history"],
                "usage": "clear history",
                "description": "Clear the saved history.",
                "handler": self._cmd_clear_history
            },
            "search_history": {
                "aliases": ["search history", "find", "find history", "search log", "search logs", "/search"],
                "usage": "search history <keywords>",
                "description": "Search the command logs by keywords.",
                "handler": self._cmd_search_history
            }
        }
        validated_actions = {}
        for key, action in actions.items():
            if self._validate_action(action):
                validated_actions[key] = action
        return validated_actions

    def _cmd_help(self, _args):
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
        lines.append("  history 10")
        lines.append("  search history status")
        lines.append("  search history echo hello")
        return "\n".join(lines).rstrip()

    def _cmd_exit(self, _args):
        return "Exiting. Bye!"

    def _cmd_status(self, _args):
        return "OK"

    def _cmd_echo(self, args):
        msg = (args or "").strip() if isinstance(args, str) else ""
        if not msg:
            return "Usage: echo <message>"
        return msg

    def _cmd_history(self, args):
        limit = None
        a = (args or "").strip() if isinstance(args, str) else ""
        if a:
            if self._is_int(a):
                limit = int(a)
            else:
                return "Usage: history OR history <number>"

        if not isinstance(self._history, list) or not self._history:
            return "No history yet."

        items = self._history
        if limit is not None:
            if not isinstance(limit, int) or limit <= 0:
                return "Please enter a positive number. Example: history 10"
            if limit > len(self._history):
                limit = len(self._history)
            items = self._history[-limit:]

        lines = []
        lines.append("History:")
        start_index = len(self._history) - len(items) + 1
        i = start_index
        for entry in items:
            if not self._validate_history_entry(entry):
                continue
            lines.append(str(i) + ". You: " + str(entry.get("input", "")))
            lines.append("   Assistant: " + str(entry.get("output", "")))
            i += 1
        return "\n".join(lines)

    def _cmd_clear_history(self, _args):
        if isinstance(self._history, list):
            self._history = []
        return "History cleared."

    def _cmd_search_history(self, args):
        query = self._normalize(args)
        if not query:
            return "Usage: search history <keywords>"

        if not isinstance(self._history, list) or not self._history:
            return "No history yet."

        keywords = self._split_keywords(query)
        if not keywords:
            return "Usage: search history <keywords>"

        matches = []
        for idx, entry in enumerate(self._history, 1):
            if not self._validate_history_entry(entry):
                continue
            hay = self._normalize(str(entry.get("input", "")) + " " + str(entry.get("output", "")))
            if self._all_keywords_present(hay, keywords):
                matches.append((idx, entry))

        if not matches:
            keyword_str = " ".join(str(k) for k in keywords)
            return "No matches found for: " + keyword_str

        lines = []
        lines.append("Matches (" + str(len(matches)) + "):")
        for idx, entry in matches:
            if not self._validate_history_entry(entry):
                continue
            lines.append(str(idx) + ". You: " + str(entry.get("input", "")))
            lines.append("   Assistant: " + str(entry.get("output", "")))
        return "\n".join(lines)

    def _normalize(self, text):
        if not isinstance(text, str):
            text = str(text) if text is not None else ""
        text = text.strip().lower()
        while "  " in text:
            text = text.replace("  ", " ")
        return text

    def _split_command(self, text):
        t = (text or "").strip() if isinstance(text, str) else ""
        while "  " in t:
            t = t.replace("  ", " ")
        if not t:
            return "", ""

        if t.startswith("/"):
            t = t[1:].lstrip()

        lowered = t.lower()

        if not isinstance(self._actions, dict):
            parts = t.split(" ", 1)
            cmd = parts[0].lower().strip()
            args = parts[1] if len(parts) > 1 else ""
            return cmd, args

        alias_map = {}
        for action_name, info in self._actions.items():
            if not isinstance(info, dict):
                continue
            alias_map[action_name] = action_name
            aliases = info.get("aliases", [])
            if isinstance(aliases, (list, tuple)):
                for a in aliases:
                    if isinstance(a, str):
                        alias_map[a.lower().lstrip("/")] = action_name

        aliases = list(alias_map.keys())
        aliases.sort(key=lambda x: len(str(x)), reverse=True)

        for a in aliases:
            a_str = str(a)
            if lowered == a_str:
                return a_str, ""
            if lowered.startswith(a_str + " "):
                return a_str, t[len(a_str):].lstrip()

        parts = t.split(" ", 1)
        cmd = parts[0].lower().strip()
        args = parts[1] if len(parts) > 1 else ""
        return cmd, args

    def _find_action_by_alias(self, cmd_text):
        if not isinstance(cmd_text, str):
            return None
        c = cmd_text.strip().lower().lstrip("/")
        if not c:
            return None

        if not isinstance(self._actions, dict):
            return None

        if c in self._actions:
            return c

        for name, info in self._actions.items():
            if not isinstance(info, dict):
                continue
            aliases = info.get("aliases", [])
            if not isinstance(aliases, (list, tuple)):
                continue
            for a in aliases:
                if isinstance(a, str) and c == a.lower().lstrip("/"):
                    return name
        return None

    def _is_int(self, s):
        if not isinstance(s, str):
            s = str(s) if s is not None else ""
        s = s.strip()
        if not s:
            return False
        if s[0] in "+-":
            s = s[1:]
        if not s:
            return False
        for ch in s:
            if ch < "0" or ch > "9":
                return False
        return True

    def _split_keywords(self, query):
        if not isinstance(query, str):
            query = str(query) if query is not None else ""
        parts = query.split(" ")
        out = []
        for p in parts:
            p = p.strip()
            if p:
                out.append(p)
        return out

    def _all_keywords_present(self, text, keywords):
        if not isinstance(text, str):
            text = str(text) if text is not None else ""
        if not isinstance(keywords, (list, tuple)):
            return False
        for k in keywords:
            if not isinstance(k, str):
                continue
            if k not in text:
                return False
        return True

    def _log_interaction(self, raw_input, output_text):
        if not isinstance(self._history, list):
            self._history = []
        entry = {
            "input": str(raw_input).strip() if raw_input is not None else "",
            "output": str(output_text).strip() if output_text is not None else ""
        }
        if self._validate_history_entry(entry):
            self._history.append(entry)

    def handle(self, user_text):
        raw = user_text if user_text is not None else ""
        cmd_text, args = self._split_command(raw)

        if not cmd_text:
            out = "No command entered. Type 'help' to see available actions."
            self._log_interaction(raw, out)
            return out

        action_name = self._find_action_by_alias(cmd_text)
        if action_name is None:
            out = "Unknown command: '" + cmd_text + "'. Type 'help' to see all available actions."
            self._log_interaction(raw, out)
            return out

        if not isinstance(self._actions, dict):
            out = "Error processing command."
            self._log_interaction(raw, out)
            return out

        handler_info = self._actions.get(action_name)
        if not isinstance(handler_info, dict):
            out = "Error processing command."
            self._log_interaction(raw, out)
            return out

        handler = handler_info.get("handler")
        if not callable(handler):
            out = "Error processing command."
            self._log_interaction(raw, out)
            return out

        out = handler(args)
        self._log_interaction(raw, out)
        return out

    def should_exit(self, user_text):
        cmd_text, _ = self._split_command(user_text)
        action_name = self._find_action_by_alias(cmd_text)
        return action_name == "exit"


if __name__ == "__main__":
    app = Assistant()
    print("Assistant ready. Type 'help' to see available actions.")
    while True:
        user = input("> ")
        response = app.handle(user)
        print(response)
        if app.should_exit(user):
            break

