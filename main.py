import json
import os

class NoteAssistant:
    def __init__(self):
        self._notes = []
        self._next_id = 1
        self._json_file = "notes.json"
        self._load_notes()

    def _load_notes(self):
        if os.path.exists(self._json_file):
            try:
                with open(self._json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self._notes = data
                        if self._notes:
                            self._next_id = max(n.get("id", 0) for n in self._notes) + 1
            except (json.JSONDecodeError, IOError):
                self._notes = []

    def _save_notes(self):
        try:
            with open(self._json_file, "w", encoding="utf-8") as f:
                json.dump(self._notes, f, indent=2, ensure_ascii=False)
        except IOError:
            pass

    def _clean(self, text):
        text = (text or "").strip()
        while "  " in text:
            text = text.replace("  ", " ")
        return text

    def _is_number(self, text):
        text = (text or "").strip()
        if not text:
            return False
        for ch in text:
            if ch < "0" or ch > "9":
                return False
        return True

    def _validate_note(self, title, content):
        if not title or not title.strip():
            return False, "Title cannot be empty."
        if not content or not content.strip():
            return False, "Content cannot be empty."
        return True, None

    def handle(self, user_input):
        raw = self._clean(user_input)
        low = raw.lower()

        if not raw:
            return "Type 'help' to see commands."

        if low in ("help", "h", "?"):
            return (
                "Commands:\n"
                "- new <title> | <content>\n"
                "- list\n"
                "- get <id>\n"
                "- delete <id>\n"
                "Examples:\n"
                "  new shopping | buy milk and bread\n"
                "  list\n"
                "  get 1\n"
                "  delete 1"
            )

        if low.startswith("new "):
            return self._new_note(raw[4:])

        if low == "list":
            return self._list_notes()

        if low.startswith("get "):
            return self._get_note(raw[4:])

        if low.startswith("delete "):
            return self._delete_note(raw[7:])

        return "Unknown command. Type 'help' to see commands."

    def _new_note(self, rest):
        rest = rest.strip()
        sep = rest.find("|")
        if sep == -1:
            return "Usage: new <title> | <content>"

        title = rest[:sep].strip()
        content = rest[sep + 1:].strip()

        valid, error = self._validate_note(title, content)
        if not valid:
            return error

        note = {
            "id": self._next_id,
            "title": title,
            "content": content
        }
        self._notes.append(note)
        self._next_id += 1
        self._save_notes()

        return "Note created. ID=" + str(note["id"])

    def _list_notes(self):
        if not self._notes:
            return "No notes found."
        lines = ["Notes:"]
        for n in self._notes:
            lines.append("ID=" + str(n["id"]) + " | " + n["title"])
        return "\n".join(lines)

    def _get_note(self, id_text):
        id_text = id_text.strip()
        if not self._is_number(id_text):
            return "Usage: get <id>"

        note_id = int(id_text)
        for n in self._notes:
            if n["id"] == note_id:
                return (
                    "ID=" + str(n["id"]) + "\n"
                    "Title: " + n["title"] + "\n"
                    "Content: " + n["content"]
                )
        return "Note not found: " + str(note_id)

    def _delete_note(self, id_text):
        id_text = id_text.strip()
        if not self._is_number(id_text):
            return "Usage: delete <id>"

        note_id = int(id_text)
        for i in range(len(self._notes)):
            if self._notes[i]["id"] == note_id:
                removed_title = self._notes[i]["title"]
                del self._notes[i]
                self._save_notes()
                return "Deleted note ID=" + str(note_id) + " (" + removed_title + ")"
        return "No note found with ID=" + str(note_id)


if __name__ == "__main__":
    app = NoteAssistant()
    print("Note Assistant ready. Type 'help' for commands. Type 'exit' to quit.")
    while True:
        user = input("> ")
        if user.strip().lower() in ("exit", "quit"):
            print("Bye!")
            break
        print(app.handle(user))
