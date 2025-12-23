import json
import os
from datetime import datetime, timedelta

class ReminderAssistant:
    def __init__(self, reminders_file="reminders.json"):
        self._reminders_file = reminders_file
        self._reminders = []
        self._next_id = 1
        self._load_reminders()

    def _load_reminders(self):
        if not os.path.exists(self._reminders_file):
            return
        try:
            with open(self._reminders_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    if "reminders" in data and isinstance(data["reminders"], list):
                        self._reminders = data["reminders"]
                    if "next_id" in data and isinstance(data["next_id"], int):
                        self._next_id = data["next_id"]
        except Exception:
            pass

    def _save_reminders(self):
        try:
            data = {
                "reminders": self._reminders,
                "next_id": self._next_id
            }
            with open(self._reminders_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def _clean_spaces(self, s):
        s = (s or "").strip()
        while "  " in s:
            s = s.replace("  ", " ")
        return s

    def _lower(self, s):
        return (s or "").strip().lower()

    def _is_digits(self, s):
        s = (s or "").strip()
        if not s:
            return False
        for ch in s:
            if ch < "0" or ch > "9":
                return False
        return True

    def _minutes_left(self, due_at_str):
        try:
            due_at = datetime.fromisoformat(due_at_str)
            now = datetime.now()
            remaining = (due_at - now).total_seconds()
            if remaining < 0:
                remaining = 0
            return int((remaining + 59) // 60)
        except Exception:
            return 0

    def handle(self, user_input):
        raw = self._clean_spaces(user_input)
        lower = self._lower(raw)

        if not raw:
            return "Type 'help' to see commands."

        if lower in ("help", "h", "?"):
            return (
                "Commands:\n"
                "- add <minutes> | <message>\n"
                "- list\n"
                "Examples:\n"
                "  add 10 | drink water\n"
                "  list"
            )

        if lower.startswith("add "):
            return self._add_reminder(raw)

        if lower == "list":
            return self._list_reminders()

        return "Unknown command. Type 'help' to see commands."

    def _add_reminder(self, raw):
        rest = raw[4:].strip()
        bar = rest.find("|")
        if bar == -1:
            return "Usage: add <minutes> | <message>"

        mins_text = rest[:bar].strip()
        msg = rest[bar + 1:].strip()

        if not self._is_digits(mins_text):
            return "Invalid minutes. Example: add 5 | drink water"

        minutes = int(mins_text)
        if minutes <= 0:
            return "Minutes must be greater than 0."

        if not msg:
            return "Message cannot be empty."

        now = datetime.now()
        due_at = now + timedelta(minutes=minutes)
        rid = self._next_id
        self._next_id += 1

        reminder = {
            "id": rid,
            "message": msg,
            "due_at": due_at.isoformat()
        }
        self._reminders.append(reminder)
        self._save_reminders()

        return "Reminder added. ID=" + str(rid) + " (due in " + str(minutes) + " minute(s))"

    def _list_reminders(self):
        if not self._reminders:
            return "No reminders set."

        lines = ["Reminders:"]
        for r in self._reminders:
            mins_left = self._minutes_left(r["due_at"])
            lines.append(
                "ID=" + str(r["id"]) +
                " | in " + str(mins_left) + " min(s)" +
                " | " + r["message"]
            )
        return "\n".join(lines)


if __name__ == "__main__":
    app = ReminderAssistant(reminders_file="reminders.json")
    print("Reminder Assistant ready. Type 'help' for commands. Type 'exit' to quit.")
    while True:
        user = input("> ")
        if user.strip().lower() in ("exit", "quit"):
            print("Bye!")
            break
        print(app.handle(user))

