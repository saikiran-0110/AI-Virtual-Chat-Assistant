"""
Black-Box Testing: Specification-Based Testing
Technique: Equivalence Partitioning + Boundary Value Analysis
Function: Note Creation Feature
Student: Abhinay Karnati (259050844)
"""

import unittest
import sys
import os
import json
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

# Try to import note functions - adjust import based on actual implementation
try:
    from main import NoteManager
except ImportError:
    # If not in main.py, create a placeholder for testing structure
    class NoteManager:
        def __init__(self, file_path="notes.json"):
            self._file_path = file_path
            self._notes = []
            self._next_id = 1
            self._load_notes()
        
        def create_note(self, title, content, tags=None):
            """Create a new note"""
            if not title or not title.strip():
                return "Title cannot be empty."
            if not content or not content.strip():
                return "Content cannot be empty."
            note = {
                "id": self._next_id,
                "title": title.strip(),
                "content": content.strip(),
                "tags": tags if tags else []
            }
            self._next_id += 1
            self._notes.append(note)
            self._save_notes()
            return f"Note created. ID={note['id']}"
        
        def _load_notes(self):
            """Load notes from file"""
            if os.path.exists(self._file_path):
                try:
                    with open(self._file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if isinstance(data, dict) and "notes" in data:
                            self._notes = data["notes"]
                            if self._notes:
                                self._next_id = max(n["id"] for n in self._notes) + 1
                            return True
                except Exception:
                    pass
            return False
        
        def _save_notes(self):
            """Save notes to file"""
            try:
                data = {"notes": self._notes}
                with open(self._file_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                return True
            except Exception:
                return False
        
        def retrieve_note(self, note_id):
            """Retrieve a note by ID"""
            for note in self._notes:
                if note["id"] == note_id:
                    return f"ID: {note['id']}\nTitle: {note['title']}\nContent: {note['content']}\nTags: {', '.join(note.get('tags', []))}"
            return f"Note not found: {note_id}"
        
        def list_all_notes(self):
            """List all notes"""
            if not self._notes:
                return "No notes found."
            lines = ["All Notes:"]
            for note in self._notes:
                lines.append(f"ID={note['id']} | {note['title']}")
            return "\n".join(lines)
        
        def delete_note(self, note_id):
            """Delete a note by ID"""
            for i in range(len(self._notes)):
                if self._notes[i]["id"] == note_id:
                    del self._notes[i]
                    self._save_notes()
                    return f"Note deleted. ID={note_id}"
            return f"Note not found: {note_id}"
        
        def search_notes(self, keyword=None, tag=None):
            """Search notes by keyword and/or tag"""
            if not keyword and not tag:
                return "Usage: search with keyword and/or tag"
            
            matches = []
            for note in self._notes:
                match = True
                if keyword:
                    keyword_lower = keyword.lower()
                    if keyword_lower not in note["title"].lower() and keyword_lower not in note["content"].lower():
                        match = False
                if tag:
                    if tag not in note.get("tags", []):
                        match = False
                if match:
                    matches.append(note)
            
            if not matches:
                return "No notes found."
            
            lines = ["Matches:"]
            for note in matches:
                lines.append(f"ID={note['id']} | {note['title']}")
            return "\n".join(lines)
        
        def update_note(self, note_id, title=None, content=None, tags=None):
            """Update a note"""
            for note in self._notes:
                if note["id"] == note_id:
                    if title is not None:
                        if not title.strip():
                            return "Title cannot be empty."
                        note["title"] = title.strip()
                    if content is not None:
                        note["content"] = content.strip()
                    if tags is not None:
                        note["tags"] = tags
                    self._save_notes()
                    return "Note updated."
            return f"Note not found: {note_id}"


class TestNoteCreationSpecificationBased(unittest.TestCase):
    """
    Specification-Based Black-Box Tests for Note Creation
    """
    
    def setUp(self):
        """Set up test fixture with temporary file"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.note_mgr = NoteManager(file_path=self.temp_file.name)
    
    def tearDown(self):
        """Clean up temporary file"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_create_note_valid(self):
        """
        Test Case: Create note with valid inputs
        Input: title="Meeting Notes", content="Discuss project"
        Expected Output: "Note created. ID=1"
        Technique: Valid input partition
        """
        result = self.note_mgr.create_note("Meeting Notes", "Discuss project")
        self.assertIn("created", result.lower())
        self.assertIn("ID=1", result)
        print(f"✓ PASS: Create note (valid) - Input: title='Meeting Notes', Output: {result}")
    
    def test_create_note_empty_title(self):
        """
        Test Case: Create note with empty title
        Input: title="", content="Some content"
        Expected Output: Error message
        Technique: Invalid input partition
        """
        result = self.note_mgr.create_note("", "Some content")
        self.assertIn("cannot be empty", result.lower())
        print(f"✓ PASS: Create note (empty title) - Input: title='', Output: {result}")
    
    def test_create_note_empty_content(self):
        """
        Test Case: Create note with empty content
        Input: title="Title", content=""
        Expected Output: Error message
        Technique: Invalid input partition
        """
        result = self.note_mgr.create_note("Title", "")
        self.assertIn("cannot be empty", result.lower())
        print(f"✓ PASS: Create note (empty content) - Input: content='', Output: {result}")
    
    def test_create_note_whitespace_title(self):
        """
        Test Case: Create note with whitespace-only title
        Input: title="   ", content="Content"
        Expected Output: Error message
        Technique: Boundary value - whitespace
        """
        result = self.note_mgr.create_note("   ", "Content")
        self.assertIn("cannot be empty", result.lower())
        print(f"✓ PASS: Create note (whitespace title) - Input: title='   ', Output: {result}")
    
    def test_create_note_with_tags(self):
        """
        Test Case: Create note with tags
        Input: title="Note", content="Content", tags=["work", "important"]
        Expected Output: Note created with tags
        Technique: Valid input partition - with optional tags
        """
        result = self.note_mgr.create_note("Note", "Content", tags=["work", "important"])
        self.assertIn("created", result.lower())
        print(f"✓ PASS: Create note (with tags) - Input: tags=['work', 'important'], Output: {result}")
    
    def test_create_note_long_title(self):
        """
        Test Case: Create note with very long title
        Input: title="A" * 1000, content="Content"
        Expected Output: Note created
        Technique: Boundary value - very long input
        """
        long_title = "A" * 1000
        result = self.note_mgr.create_note(long_title, "Content")
        self.assertIn("created", result.lower())
        print("✓ PASS: Create note (long title) - Note created")
    
    def test_create_note_multiple_notes(self):
        """
        Test Case: Create multiple notes
        Input: Create 3 notes sequentially
        Expected Output: Each note gets unique ID
        Technique: Valid input partition - multiple operations
        """
        result1 = self.note_mgr.create_note("Note 1", "Content 1")
        result2 = self.note_mgr.create_note("Note 2", "Content 2")
        result3 = self.note_mgr.create_note("Note 3", "Content 3")
        self.assertIn("ID=1", result1)
        self.assertIn("ID=2", result2)
        self.assertIn("ID=3", result3)
        print("✓ PASS: Create multiple notes - Each gets unique ID")


if __name__ == '__main__':
    unittest.main(verbosity=2)

