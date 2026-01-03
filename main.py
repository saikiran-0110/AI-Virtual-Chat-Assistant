import json
import os


class InfoSnippetAssistant:
    def __init__(self):
        self._snippets = {
            "about": "This assistant helps with notes, reminders, calculations, and quick information.",
            "help": "Use simple commands like info <topic>, topics, or help.",
            "privacy": "All data is stored locally on your system and is not shared.",
            "notes": "Notes allow you to save, edit, search, and retrieve written information.",
            "reminders": "Reminders help you remember tasks by notifying you at the right time.",
            "calculations": "The calculator can solve small arithmetic problems quickly.",
            "definitions": "Definitions help explain unfamiliar words or technical terms.",
            "storage": "Information is saved in structured files so it is not lost across sessions.",
            "usage": "Type help to see available commands and examples.",
            "exit": "Type exit or quit to close the assistant."
        }

    def _clean(self, text):
        text = (text or "").strip()
        while "  " in text:
            text = text.replace("  ", " ")
        return text

    def _lower(self, text):
        return (text or "").strip().lower()

    def handle(self, user_input):
        raw = self._clean(user_input)
        low = self._lower(raw)

        if not raw:
            return "Type 'help' to see available commands."

        if low in ("help", "h", "?"):
            return (
                "Commands:\n"
                "- info <topic>\n"
                "- topics\n"
                "Examples:\n"
                "  info privacy\n"
                "  info reminders\n"
                "  topics"
            )

        if low == "topics":
            return self._list_topics()

        if low.startswith("info "):
            return self._get_info(raw[5:])

        return (
            "I am not sure how to answer that.\n"
            "Try: topics (to see available information)\n"
            "Or type: help"
        )

    def _list_topics(self):
        keys = list(self._snippets.keys())
        keys.sort()
        lines = ["Available topics:"]
        for k in keys:
            lines.append("- " + k)
        return "\n".join(lines)

    def _get_info(self, topic_text):
        topic = self._lower(topic_text)
        if not topic:
            return "Usage: info <topic>"

        if topic in self._snippets:
            return topic + ": " + self._snippets[topic]

        suggestions = []
        for k in self._snippets:
            if topic in k or k in topic:
                suggestions.append(k)

        if suggestions:
            return (
                "No exact information found for '" + topic + "'.\n"
                "Did you mean:\n- " + "\n- ".join(suggestions)
            )

        return (
            "No information found for '" + topic + "'.\n"
            "Type 'topics' to see available information."
        )


class KeywordSnippetAssistant:
    def __init__(self):
        self._info = InfoSnippetAssistant()
        self._snippets = self._build_snippets()
        self._last_results = []

    def _build_snippets(self):
        data = [
            ("privacy", "Data is stored locally on the computer and is not shared with anyone."),
            ("notes", "Notes help store information. Notes can be created, edited, searched, and deleted."),
            ("reminders", "Reminders help remember tasks by alerting at a set time."),
            ("calculator", "Calculations support basic arithmetic to solve small problems quickly."),
            ("definitions", "Definitions explain new words with simple meaning."),
            ("storage", "Structured files keep saved information across sessions."),
            ("help", "Use commands like ask <keywords>, show <id>, and all to explore snippets."),
            ("exit", "Type exit or quit to close the assistant.")
        ]

        out = []
        i = 1
        for title, text in data:
            out.append({"id": i, "title": title, "text": text})
            i += 1
        return out

    def _clean(self, s):
        s = (s or "").strip()
        while "  " in s:
            s = s.replace("  ", " ")
        return s

    def _lower(self, s):
        return (s or "").strip().lower()

    def _split_keywords(self, text):
        text = self._lower(self._clean(text))
        if not text:
            return []
        parts = text.split(" ")
        out = []
        for p in parts:
            p = p.strip()
            if p:
                out.append(p)
        return out

    def _score(self, snippet, keywords):
        title = self._lower(snippet["title"])
        body = self._lower(snippet["text"])

        score = 0
        for k in keywords:
            if k in title:
                score += 3
            if k in body:
                score += 1
        return score

    def _sort_by_score(self, scored_list):
        items = scored_list[:]
        out = []
        while items:
            best_i = 0
            i = 1
            while i < len(items):
                if items[i][0] > items[best_i][0]:
                    best_i = i
                elif items[i][0] == items[best_i][0]:
                    if items[i][1]["id"] < items[best_i][1]["id"]:
                        best_i = i
                i += 1
            out.append(items.pop(best_i))
        return out

    def handle(self, user_input):
        raw = self._clean(user_input)
        low = self._lower(raw)

        if not raw:
            return "Type 'help' to see commands."

        if low in ("help", "h", "?"):
            return (
                "Commands:\n"
                "- info <topic>\n"
                "- topics\n"
                "- ask <keywords>\n"
                "- show <id>\n"
                "- all\n"
                "Examples:\n"
                "  info privacy\n"
                "  ask save data storage\n"
                "  show 2"
            )

        if low == "topics":
            return self._info.handle(user_input)

        if low.startswith("info "):
            return self._info.handle(user_input)

        if low == "all":
            return self._all_titles()

        if low.startswith("ask "):
            return self._ask(raw[4:])

        if low.startswith("show "):
            return self._show(raw[5:])

        return "Unknown command. Type 'help' to see commands."

    def _all_titles(self):
        lines = ["All snippets:"]
        for s in self._snippets:
            lines.append("ID=" + str(s["id"]) + " | " + s["title"])
        return "\n".join(lines)

    def _ask(self, keywords_text):
        keywords = self._split_keywords(keywords_text)
        if not keywords:
            return "Usage: ask <keywords>"

        scored = []
        for snip in self._snippets:
            sc = self._score(snip, keywords)
            if sc > 0:
                scored.append((sc, snip))

        if not scored:
            self._last_results = []
            return (
                "No matching information found.\n"
                "Try different keywords or type 'all' to see available topics."
            )

        ordered = self._sort_by_score(scored)
        self._last_results = []
        for sc, snip in ordered:
            self._last_results.append(snip)

        lines = ["Matches:"]
        i = 0
        while i < len(ordered) and i < 5:
            sc, snip = ordered[i]
            preview = snip["text"]
            if len(preview) > 70:
                preview = preview[:70] + "..."
            lines.append(
                "ID=" + str(snip["id"]) +
                " | score=" + str(sc) +
                " | " + snip["title"] +
                " | " + preview
            )
            i += 1

        lines.append("Use: show <id> to view the full snippet.")
        return "\n".join(lines)

    def _show(self, id_text):
        id_text = id_text.strip()
        if not id_text:
            return "Usage: show <id>"

        for ch in id_text:
            if ch < "0" or ch > "9":
                return "Usage: show <id>"

        sid = int(id_text)
        for snip in self._snippets:
            if snip["id"] == sid:
                return (
                    "ID: " + str(snip["id"]) + "\n"
                    "Title: " + snip["title"] + "\n"
                    "Text: " + snip["text"]
                )

        return "Snippet not found: " + str(sid)


class PersistentSnippets:
    def __init__(self, file_path="snippets.json"):
        self._file_path = file_path
        self._info = InfoSnippetAssistant()
        self._keyword = KeywordSnippetAssistant()
        self._snippets = []
        self._next_id = 1
        loaded = self._load_file()

        if not loaded:
            self._seed_defaults()
            self._save_file()

    def _clean(self, s):
        s = (s or "").strip()
        while "  " in s:
            s = s.replace("  ", " ")
        return s

    def _is_number(self, s):
        s = (s or "").strip()
        if not s:
            return False
        for ch in s:
            if ch < "0" or ch > "9":
                return False
        return True

    def _split_pipe(self, text):
        parts = text.split("|")
        out = []
        for p in parts:
            out.append(p.strip())
        return out

    def _lower(self, s):
        return (s or "").strip().lower()

    def _find_snip(self, sid):
        for sn in self._snippets:
            if sn["id"] == sid:
                return sn
        return None

    def _load_file(self):
        if not os.path.exists(self._file_path):
            return False

        try:
            with open(self._file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict) and "snippets" in data:
                    snippets_list = data["snippets"]
                    if isinstance(snippets_list, list):
                        self._snippets = []
                        self._next_id = 1
                        for item in snippets_list:
                            if isinstance(item, dict) and "id" in item and "title" in item and "text" in item:
                                sid = item["id"]
                                if isinstance(sid, int) and sid > 0:
                                    self._snippets.append({
                                        "id": sid,
                                        "title": str(item["title"]),
                                        "text": str(item["text"])
                                    })
                                    if sid >= self._next_id:
                                        self._next_id = sid + 1
                        return len(self._snippets) > 0
        except Exception:
            pass
        return False

    def _save_file(self):
        try:
            data = {
                "snippets": self._snippets
            }
            with open(self._file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def _seed_defaults(self):
        defaults = [
            ("privacy", "Data is stored locally and is not shared."),
            ("usage", "Type help to see commands. Use list, get, add, delete, search."),
            ("notes", "Notes store text information for later review."),
            ("reminders", "Reminders help remember tasks at the right time."),
            ("calculator", "Calculator solves small arithmetic problems quickly."),
        ]
        for title, text in defaults:
            self._snippets.append({"id": self._next_id, "title": title, "text": text})
            self._next_id += 1

    def handle(self, user_input):
        raw = self._clean(user_input)
        low = self._lower(raw)

        if not raw:
            return "Type 'help' to see commands."

        if low in ("help", "h", "?"):
            return (
                "Commands:\n"
                "- info <topic>\n"
                "- topics\n"
                "- ask <keywords>\n"
                "- show <id>\n"
                "- all\n"
                "- add <title> | <text>\n"
                "- list\n"
                "- get <id>\n"
                "- delete <id>\n"
                "- search <keyword>\n"
                "Notes:\n"
                "- Snippets auto-load on startup.\n"
                "- Snippets auto-save after add/delete."
            )

        if low == "topics":
            return self._info.handle(user_input)

        if low.startswith("info "):
            return self._info.handle(user_input)

        if low == "all":
            return self._keyword.handle(user_input)

        if low.startswith("ask "):
            return self._keyword.handle(user_input)

        if low.startswith("show "):
            return self._keyword.handle(user_input)

        if low.startswith("add "):
            return self._add(raw[4:])

        if low == "list":
            return self._list()

        if low.startswith("get "):
            return self._get(raw[4:])

        if low.startswith("delete "):
            return self._delete(raw[7:])

        if low.startswith("search "):
            return self._search(raw[7:])

        return "Unknown command. Type 'help' to see commands."

    def _add(self, rest):
        parts = self._split_pipe(rest)
        if len(parts) < 2:
            return "Usage: add <title> | <text>"

        title = parts[0]
        text = parts[1]

        if not title:
            return "Title cannot be empty."
        if not text:
            return "Text cannot be empty."

        sn = {"id": self._next_id, "title": title, "text": text}
        self._next_id += 1
        self._snippets.append(sn)
        self._save_file()

        return "Snippet saved. ID=" + str(sn["id"])

    def _list(self):
        if not self._snippets:
            return "No snippets available."
        lines = ["Snippets:"]
        for sn in self._snippets:
            lines.append("ID=" + str(sn["id"]) + " | " + sn["title"])
        return "\n".join(lines)

    def _get(self, id_text):
        id_text = id_text.strip()
        if not self._is_number(id_text):
            return "Usage: get <id>"

        sid = int(id_text)
        sn = self._find_snip(sid)
        if not sn:
            return "Snippet not found: " + str(sid)

        return (
            "ID: " + str(sn["id"]) + "\n"
            "Title: " + sn["title"] + "\n"
            "Text: " + sn["text"]
        )

    def _delete(self, id_text):
        id_text = id_text.strip()
        if not self._is_number(id_text):
            return "Usage: delete <id>"

        sid = int(id_text)
        for i in range(len(self._snippets)):
            if self._snippets[i]["id"] == sid:
                del self._snippets[i]
                self._save_file()
                return "Snippet deleted. ID=" + str(sid)

        return "Snippet not found: " + str(sid)

    def _search(self, keyword_text):
        key = self._lower(keyword_text)
        if not key:
            return "Usage: search <keyword>"

        matches = []
        for sn in self._snippets:
            if key in self._lower(sn["title"]) or key in self._lower(sn["text"]):
                matches.append(sn)

        if not matches:
            return "No snippets found for keyword: " + key

        lines = ["Matches:"]
        for sn in matches:
            lines.append("ID=" + str(sn["id"]) + " | " + sn["title"])
        return "\n".join(lines)


if __name__ == "__main__":
    app = PersistentSnippets(file_path="snippets.json")
    print("Persistent Snippets Assistant ready. Type 'help' for commands. Type 'exit' to quit.")
    while True:
        user = input("> ")
        if user.strip().lower() in ("exit", "quit"):
            print("Bye!")
            break
        print(app.handle(user))

