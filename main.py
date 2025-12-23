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
                "usage": "history",
                "description": "Show past commands and assistant responses.",
                "handler": self._cmd_history
            },
            "clear_history": {
                "aliases": ["clear history", "clear log", "clear logs", "/clear_history"],
                "usage": "clear history",
                "description": "Clear the saved history.",
                "handler": self._cmd_clear_history
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

        lines.append("Tip: If a command is unknown, type 'help' to see valid commands.")
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

    def _normalize(self, text):
        if not isinstance(text, str):
            text = str(text) if text is not None else ""
        text = text.strip()
        while "  " in text:
            text = text.replace("  ", " ")
        return text

    def _split_command(self, text):
        t = self._normalize(text)
        if not t:
            return "", ""

        if t.startswith("/"):
            t = t[1:].lstrip()

        parts = t.split(" ", 1)
        cmd = parts[0].lower().strip()
        args = parts[1] if len(parts) > 1 else ""
        return cmd, args

    def _find_action(self, cmd):
        if not isinstance(cmd, str):
            return None
        cmd = cmd.lower().strip()
        if not cmd:
            return None

        if not isinstance(self._actions, dict):
            return None

        if cmd in self._actions:
            return cmd

        for name, info in self._actions.items():
            if not isinstance(info, dict):
                continue
            aliases = info.get("aliases", [])
            if not isinstance(aliases, (list, tuple)):
                continue
            for a in aliases:
                if isinstance(a, str) and cmd == a.lower().lstrip("/"):
                    return name
        return None

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
        cmd, args = self._split_command(raw)

        if not cmd:
            out = "No command entered. Type 'help' to see available actions."
            self._log_interaction(raw, out)
            return out

        action_name = self._find_action(cmd)
        if action_name is None:
            out = self._unknown_command_message(cmd)
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
        cmd, _ = self._split_command(user_text)
        action_name = self._find_action(cmd)
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

