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

    def _to_lower(self, text):
        return (text or "").strip().lower()

    def _split_tags(self, tags_text):
        raw = (tags_text or "").strip()
        if not raw:
            return []
        parts = raw.split(",")
        out = []
        for p in parts:
            t = self._to_lower(p)
            t = self._clean(t)
            if t:
                out.append(t)
        unique = []
        for t in out:
            if t not in unique:
                unique.append(t)
        return unique

    def _validate_note(self, title, content):
        if not title or not title.strip():
            return False, "Title cannot be empty."
        if not content or not content.strip():
            return False, "Content cannot be empty."
        return True, None

    def _matches_keywords(self, note, keywords):
        hay = self._to_lower(note["title"] + " " + note["content"])
        for k in keywords:
            if k not in hay:
                return False
        return True

    def handle(self, user_input):
        raw = self._clean(user_input)
        low = raw.lower()

        if not raw:
            return "Type 'help' to see commands."

        if low in ("help", "h", "?"):
            return (
                "Commands:\n"
                "- new <title> | <content> | <tag1,tag2,...>\n"
                "- list\n"
                "- get <id>\n"
                "- delete <id>\n"
                "- search keyword <words>\n"
                "- search tag <tagname>\n"
                "Examples:\n"
                "  new shopping | buy milk and bread\n"
                "  new groceries | buy eggs | personal,shopping\n"
                "  search keyword milk eggs\n"
                "  search tag shopping"
            )

        if low.startswith("new "):
            return self._new_note(raw[4:])

        if low == "list":
            return self._list_notes()

        if low.startswith("get "):
            return self._get_note(raw[4:])

        if low.startswith("delete "):
            return self._delete_note(raw[7:])

        if low.startswith("search keyword "):
            return self._search_keyword(raw[len("search keyword "):])

        if low.startswith("search tag "):
            return self._search_tag(raw[len("search tag "):])

        return "Unknown command. Type 'help' to see commands."

    def _new_note(self, rest):
        rest = rest.strip()
        parts = rest.split("|")
        if len(parts) < 2:
            return "Usage: new <title> | <content> | <tag1,tag2,...>"

        title = parts[0].strip()
        content = parts[1].strip()
        tags_text = ""
        if len(parts) >= 3:
            tags_text = parts[2].strip()

        valid, error = self._validate_note(title, content)
        if not valid:
            return error

        tags = self._split_tags(tags_text)

        note = {
            "id": self._next_id,
            "title": title,
            "content": content,
            "tags": tags
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
            tags = n.get("tags", [])
            tag_part = "tags: " + (", ".join(tags) if tags else "none")
            lines.append("ID=" + str(n["id"]) + " | " + n["title"] + " | " + tag_part)
        return "\n".join(lines)

    def _get_note(self, id_text):
        id_text = id_text.strip()
        if not self._is_number(id_text):
            return "Usage: get <id>"

        note_id = int(id_text)
        for n in self._notes:
            if n["id"] == note_id:
                tags = n.get("tags", [])
                tags_str = ", ".join(tags) if tags else "none"
                return (
                    "ID=" + str(n["id"]) + "\n"
                    "Title: " + n["title"] + "\n"
                    "Tags: " + tags_str + "\n"
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

    def _search_keyword(self, words):
        text = self._clean(words)
        if not text:
            return "Usage: search keyword <words>"

        keywords = self._clean(self._to_lower(text)).split(" ")
        filtered = []
        for k in keywords:
            k = k.strip()
            if k:
                filtered.append(k)

        if not filtered:
            return "Usage: search keyword <words>"

        matches = []
        for n in self._notes:
            if self._matches_keywords(n, filtered):
                matches.append(n)

        if not matches:
            return "No notes found for keywords: " + " ".join(filtered)

        lines = ["Matches (" + str(len(matches)) + "):"]
        for n in matches:
            lines.append("ID=" + str(n["id"]) + " | " + n["title"])
        return "\n".join(lines)

    def _search_tag(self, tag_text):
        tag = self._clean(self._to_lower(tag_text))
        if not tag:
            return "Usage: search tag <tagname>"

        matches = []
        for n in self._notes:
            tags = n.get("tags", [])
            if tag in tags:
                matches.append(n)

        if not matches:
            return "No notes found for tag: " + tag

        lines = ["Matches (" + str(len(matches)) + ") for tag '" + tag + "':"]
        for n in matches:
            lines.append("ID=" + str(n["id"]) + " | " + n["title"])
        return "\n".join(lines)


if __name__ == "__main__":
    app = NoteAssistant()
    print("Note Assistant ready. Type 'help' for commands. Type 'exit' to quit.")
    while True:
        user = input("> ")
        if user.strip().lower() in ("exit", "quit"):
            print("Bye!")
            break
        print(app.handle(user))

