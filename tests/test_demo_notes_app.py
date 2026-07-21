import importlib.util
import os
import tempfile
import unittest
from pathlib import Path


def load_demo_notes_module(database_url: str):
    module_path = Path(__file__).resolve().parents[1] / "demo-notes" / "app.py"
    spec = importlib.util.spec_from_file_location("demo_notes_app", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    previous = os.environ.get("DEMO_NOTES_DATABASE_URL")
    os.environ["DEMO_NOTES_DATABASE_URL"] = database_url
    try:
        spec.loader.exec_module(module)
    finally:
        if previous is None:
            os.environ.pop("DEMO_NOTES_DATABASE_URL", None)
        else:
            os.environ["DEMO_NOTES_DATABASE_URL"] = previous
    return module


class DemoNotesAppTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database_url = f"sqlite:///{Path(self.temp_dir.name) / 'demo_notes.db'}"
        self.module = load_demo_notes_module(self.database_url)
        self.module._database_initialized = False
        self.module.init_database()

    def tearDown(self) -> None:
        self.module.engine.dispose()
        self.temp_dir.cleanup()

    def test_root_returns_html_page(self) -> None:
        html = self.module.root()

        self.assertIn("Demo Notes", html)
        self.assertIn("새 메모", html)
        self.assertIn("메모 목록", html)

    def test_create_update_and_delete_note(self) -> None:
        created = self.module.create_note(
            self.module.NoteCreate(
                title="운영 메모",
                body="대시보드 버튼 점검",
                due_date="2026-07-21",
            )
        )

        note_id = created["note"]["id"]
        self.assertEqual(created["note"]["title"], "운영 메모")
        self.assertEqual(self.module.list_notes()["notes"][0]["title"], "운영 메모")

        updated = self.module.update_note(
            note_id,
            self.module.NoteUpdate(
                title="운영 메모 수정",
                body="대시보드 버튼 재점검",
                due_date="2026-07-21",
                status="in_progress",
            ),
        )
        self.assertEqual(updated["note"]["title"], "운영 메모 수정")
        self.assertEqual(updated["note"]["status"], "in_progress")

        deleted = self.module.delete_note(note_id)
        self.assertEqual(deleted["note"]["id"], note_id)
        self.assertEqual(self.module.list_notes()["notes"], [])


if __name__ == "__main__":
    unittest.main()
