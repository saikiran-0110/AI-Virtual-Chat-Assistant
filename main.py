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


if __name__ == "__main__":
    app = InfoSnippetAssistant()
    print("Info Assistant ready. Type 'help' for commands. Type 'exit' to quit.")
    while True:
        user = input("> ")
        if user.strip().lower() in ("exit", "quit"):
            print("Bye!")
            break
        print(app.handle(user))

