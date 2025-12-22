import json
import os

class PreferenceAssistant:
    def __init__(self, prefs_file="user_profile.json"):
        self._prefs_file = prefs_file
        self._prefs = {
            "name": "",
            "age": "",
            "city": "",
            "language": "",
            "tone": ""
        }
        self._load_prefs()

    def _load_prefs(self):
        if not os.path.exists(self._prefs_file):
            return
        try:
            with open(self._prefs_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    for key in self._prefs:
                        if key in data:
                            self._prefs[key] = str(data[key]) if data[key] is not None else ""
        except Exception:
            pass

    def _save_prefs(self):
        try:
            with open(self._prefs_file, "w", encoding="utf-8") as f:
                json.dump(self._prefs, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def _clean_spaces(self, s):
        s = (s or "").strip()
        while "  " in s:
            s = s.replace("  ", " ")
        return s

    def _normalize_key(self, key):
        k = (key or "").strip().lower()
        while "  " in k:
            k = k.replace("  ", " ")
        out = []
        for ch in k:
            ok = ("a" <= ch <= "z") or ("0" <= ch <= "9") or ch in ["_", "-", " "]
            if ok:
                out.append(ch)
        k = "".join(out).strip()
        while "  " in k:
            k = k.replace("  ", " ")
        return k

    def _parse_set(self, text):
        if not text.lower().startswith("set "):
            return "", ""
        rest = text[4:].strip()
        eq = rest.find("=")
        if eq == -1:
            return "", ""
        left = rest[:eq].strip()
        right = rest[eq + 1:].strip()
        key = self._normalize_key(left)
        value = right
        if not key or not value:
            return "", ""
        return key, value

    def _is_digits(self, s):
        s = (s or "").strip()
        if not s:
            return False
        for ch in s:
            if ch < "0" or ch > "9":
                return False
        return True

    def handle(self, user_input):
        raw = self._clean_spaces(user_input)
        if not raw:
            return "Type: set <key> = <value> OR say <message> OR prefs"

        lower = raw.lower()

        if lower.startswith("set "):
            key, value = self._parse_set(raw)
            if not key:
                return "Usage: set <key> = <value>"
            if key not in self._prefs:
                return "Unknown preference field: " + key + ". Type 'help' to see allowed fields."
            if key == "age":
                if not self._is_digits(value):
                    return "Invalid age. Please enter digits only. Example: set age = 23"
            self._prefs[key] = value
            self._save_prefs()
            return "Saved: " + key + " = " + value

        if lower.startswith("get "):
            key = self._normalize_key(raw[4:])
            if not key:
                return "Usage: get <key>"
            if key not in self._prefs:
                return "No preference found for: " + key
            return key + " = " + self._prefs[key]

        if lower == "prefs":
            if not any(self._prefs.values()):
                return "No preferences saved."
            keys = list(self._prefs.keys())
            keys.sort()
            lines = ["Preferences:"]
            for k in keys:
                if self._prefs[k]:
                    lines.append("- " + k + " = " + self._prefs[k])
            return "\n".join(lines) if len(lines) > 1 else "No preferences saved."

        if lower == "clear all":
            for key in self._prefs:
                self._prefs[key] = ""
            self._save_prefs()
            return "All preferences cleared."

        if lower.startswith("clear "):
            key = self._normalize_key(raw[6:])
            if not key:
                return "Usage: clear <key> OR clear all"
            if key not in self._prefs:
                return "No preference found for: " + key
            self._prefs[key] = ""
            self._save_prefs()
            return "Removed preference: " + key

        if lower.startswith("say "):
            msg = raw[4:].strip()
            if not msg:
                return "Usage: say <message>"

            name = (self._prefs.get("name", "") or "").strip()
            tone = (self._prefs.get("tone", "") or "").strip().lower()
            language = (self._prefs.get("language", "") or "").strip()

            prefix = ""
            if name:
                prefix = name + ": "

            if tone == "formal":
                base = "Received. " + prefix + msg
            else:
                base = "Got it. " + prefix + msg

            if language:
                base = base + " (Preferred language: " + language + ")"

            return base

        if lower in ("help", "h", "?"):
            return (
                "Commands:\n"
                "- set <key> = <value>\n"
                "- get <key>\n"
                "- prefs\n"
                "- clear <key>\n"
                "- clear all\n"
                "- say <message>\n"
                "Examples:\n"
                "  set name = Ahmed\n"
                "  set tone = formal\n"
                "  say remind me tomorrow"
            )

        return "Unknown command. Type 'help' to see commands."


if __name__ == "__main__":
    app = PreferenceAssistant(prefs_file="user_profile.json")
    print("Preference Assistant ready. Type 'help' for commands.")
    while True:
        user = input("> ")
        if user.strip().lower() in ("exit", "quit"):
            print("Bye!")
            break
        print(app.handle(user))

