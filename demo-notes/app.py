import os
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlalchemy import Integer, String, Text, create_engine, select
from sqlalchemy.engine import make_url
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

app = FastAPI(title="Demo Notes Service")


class Base(DeclarativeBase):
    pass


class Note(Base):
    __tablename__ = "demo_notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200))
    body: Mapped[str] = mapped_column(Text)
    due_date: Mapped[str | None] = mapped_column(String(20), nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="open")


class NoteCreate(BaseModel):
    title: str
    body: str
    due_date: str | None = None


class NoteUpdate(NoteCreate):
    status: str | None = None


_database_initialized = False


def is_running_in_container() -> bool:
    return Path("/.dockerenv").exists()


def normalize_database_url(database_url: str) -> str:
    if is_running_in_container():
        return database_url

    try:
        parsed = make_url(database_url)
    except Exception:
        return database_url

    if parsed.host != "db":
        return database_url

    return str(parsed.set(host="localhost"))


def get_database_url() -> str:
    database_url = (
        os.getenv("DEMO_NOTES_DATABASE_URL")
        or os.getenv("DATABASE_URL")
        or "sqlite:///./demo_notes.db"
    )
    return normalize_database_url(database_url)


def build_engine():
    database_url = get_database_url()
    connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
    return create_engine(database_url, future=True, pool_pre_ping=True, connect_args=connect_args)


engine = build_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def serialize_note(note: Note) -> dict:
    return {
        "id": note.id,
        "title": note.title,
        "body": note.body,
        "due_date": note.due_date,
        "status": note.status,
    }


@contextmanager
def get_session() -> Iterator[Session]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def init_database() -> None:
    global _database_initialized

    if _database_initialized:
        return

    Base.metadata.create_all(engine)
    _database_initialized = True


def list_note_rows() -> list[Note]:
    init_database()
    with get_session() as session:
        notes = session.scalars(select(Note).order_by(Note.id.desc())).all()
        return list(notes)


def get_notes_page() -> str:
    return """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Demo Notes</title>
        <style>
            :root {
                color-scheme: light;
                --bg: #f3f8fd;
                --panel: #ffffff;
                --border: #d8e4f1;
                --text: #203047;
                --muted: #6d8098;
                --accent: #2382d3;
                --accent-soft: #edf6ff;
                --mint: #7dc35f;
                --shadow: 0 18px 40px rgba(40, 86, 145, 0.08);
            }

            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                font-family: "Segoe UI", Arial, sans-serif;
                background: linear-gradient(180deg, #fbfdff 0%, var(--bg) 100%);
                color: var(--text);
            }

            .page {
                max-width: 1120px;
                margin: 0 auto;
                padding: 28px 20px 40px;
            }

            .hero {
                margin-bottom: 20px;
            }

            .hero h1 {
                margin: 0;
                font-size: 34px;
                letter-spacing: -0.03em;
            }

            .hero p {
                margin: 8px 0 0;
                color: var(--muted);
                font-size: 14px;
            }

            .layout {
                display: grid;
                grid-template-columns: 360px minmax(0, 1fr);
                gap: 18px;
            }

            .panel {
                background: var(--panel);
                border: 1px solid var(--border);
                border-radius: 18px;
                box-shadow: var(--shadow);
                padding: 20px;
            }

            .panel h2 {
                margin: 0 0 16px;
                font-size: 18px;
            }

            .field {
                margin-bottom: 14px;
            }

            .field label {
                display: block;
                margin-bottom: 7px;
                font-size: 13px;
                font-weight: 700;
                color: #556e8d;
            }

            .field input,
            .field textarea {
                width: 100%;
                border: 1px solid var(--border);
                border-radius: 12px;
                padding: 12px 14px;
                font: inherit;
                background: #fbfdff;
                color: var(--text);
            }

            .field textarea {
                min-height: 130px;
                resize: vertical;
            }

            .actions {
                display: flex;
                align-items: center;
                flex-wrap: wrap;
                gap: 10px;
            }

            button {
                border: 0;
                border-radius: 12px;
                padding: 12px 16px;
                font: inherit;
                font-weight: 700;
                cursor: pointer;
            }

            .primary {
                background: linear-gradient(135deg, var(--accent), #3aa9d8);
                color: white;
            }

            .secondary {
                background: #f4f8fc;
                color: #56708f;
                border: 1px solid var(--border);
            }

            .feedback {
                margin-top: 12px;
                min-height: 20px;
                color: var(--muted);
                font-size: 13px;
            }

            .list-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 12px;
                margin-bottom: 14px;
            }

            .count {
                display: inline-flex;
                align-items: center;
                padding: 7px 11px;
                border-radius: 999px;
                background: var(--accent-soft);
                color: var(--accent);
                font-size: 12px;
                font-weight: 700;
            }

            .notes {
                display: grid;
                gap: 12px;
            }

            .note {
                border: 1px solid #e2ebf6;
                border-radius: 14px;
                padding: 16px;
                background: #fcfeff;
            }

            .note-top {
                display: flex;
                justify-content: space-between;
                gap: 12px;
                margin-bottom: 8px;
            }

            .note-title {
                font-size: 16px;
                font-weight: 800;
            }

            .note-status {
                display: inline-flex;
                align-items: center;
                padding: 6px 10px;
                border-radius: 999px;
                background: #eef7e9;
                color: #5f9931;
                font-size: 11px;
                font-weight: 800;
                text-transform: uppercase;
            }

            .note-body {
                color: #526983;
                font-size: 14px;
                line-height: 1.6;
                white-space: pre-wrap;
            }

            .note-meta {
                margin-top: 10px;
                color: var(--muted);
                font-size: 12px;
            }

            .note-actions {
                margin-top: 14px;
                display: flex;
                gap: 8px;
            }

            .note-actions button {
                padding: 9px 12px;
                font-size: 12px;
            }

            .danger {
                background: #fff2ef;
                color: #c85648;
                border: 1px solid #f0d4cf;
            }

            .empty {
                padding: 28px 16px;
                border: 1px dashed #d5e3f2;
                border-radius: 14px;
                text-align: center;
                color: var(--muted);
                background: #fbfdff;
            }

            @media (max-width: 900px) {
                .layout {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        <div class="page">
            <div class="hero">
                <h1>Demo Notes</h1>
                <p>운영자가 바로 입력하고 저장할 수 있는 작은 내부 메모 서비스입니다.</p>
            </div>

            <div class="layout">
                <section class="panel">
                    <h2>새 메모</h2>
                    <form id="note-form">
                        <input id="editing-id" type="hidden" />
                        <div class="field">
                            <label for="title">제목</label>
                            <input id="title" name="title" required />
                        </div>
                        <div class="field">
                            <label for="body">내용</label>
                            <textarea id="body" name="body" required></textarea>
                        </div>
                        <div class="field">
                            <label for="due_date">기한</label>
                            <input id="due_date" name="due_date" type="date" />
                        </div>
                        <div class="actions">
                            <button class="primary" type="submit" id="submit-button">저장</button>
                            <button class="secondary" type="button" id="cancel-edit-button">수정 취소</button>
                            <button class="secondary" type="button" id="refresh-button">새로 고침</button>
                        </div>
                        <div id="feedback" class="feedback"></div>
                    </form>
                </section>

                <section class="panel">
                    <div class="list-header">
                        <h2>메모 목록</h2>
                        <div id="note-count" class="count">0개</div>
                    </div>
                    <div id="notes" class="notes"></div>
                </section>
            </div>
        </div>

        <script>
            function resetForm() {
                document.getElementById("note-form").reset();
                document.getElementById("editing-id").value = "";
                document.getElementById("submit-button").textContent = "저장";
                document.getElementById("cancel-edit-button").style.display = "none";
            }

            function startEdit(note) {
                document.getElementById("editing-id").value = String(note.id);
                document.getElementById("title").value = note.title || "";
                document.getElementById("body").value = note.body || "";
                document.getElementById("due_date").value = note.due_date || "";
                document.getElementById("submit-button").textContent = "수정 저장";
                document.getElementById("cancel-edit-button").style.display = "inline-flex";
                document.getElementById("feedback").textContent = "수정 모드입니다.";
                window.scrollTo({ top: 0, behavior: "smooth" });
            }

            async function loadNotes() {
                const notesRoot = document.getElementById("notes");
                const count = document.getElementById("note-count");
                notesRoot.innerHTML = "";

                try {
                    const response = await fetch("/api/notes");
                    if (!response.ok) {
                        throw new Error("notes_api_failed");
                    }

                    const payload = await response.json();
                    const notes = payload.notes || [];

                    count.textContent = notes.length + "개";

                    if (notes.length === 0) {
                        notesRoot.innerHTML = '<div class="empty">저장된 메모가 없습니다.</div>';
                        return;
                    }

                    notes.forEach(note => {
                        const item = document.createElement("article");
                        item.className = "note";
                        const top = document.createElement("div");
                        const title = document.createElement("div");
                        const status = document.createElement("div");
                        const body = document.createElement("div");
                        const meta = document.createElement("div");
                        const actions = document.createElement("div");
                        const editButton = document.createElement("button");
                        const deleteButton = document.createElement("button");

                        top.className = "note-top";
                        title.className = "note-title";
                        status.className = "note-status";
                        body.className = "note-body";
                        meta.className = "note-meta";
                        actions.className = "note-actions";
                        editButton.className = "secondary";
                        deleteButton.className = "danger";

                        title.textContent = note.title;
                        status.textContent = note.status;
                        body.textContent = note.body;
                        meta.textContent = "기한: " + (note.due_date || "-");
                        editButton.textContent = "수정";
                        deleteButton.textContent = "삭제";

                        editButton.addEventListener("click", () => startEdit(note));
                        deleteButton.addEventListener("click", async () => {
                            const confirmed = window.confirm("이 메모를 삭제할까요?");
                            if (!confirmed) {
                                return;
                            }

                            const deleteResponse = await fetch("/api/notes/" + note.id, {
                                method: "DELETE",
                            });

                            if (!deleteResponse.ok) {
                                document.getElementById("feedback").textContent = "메모 삭제에 실패했습니다.";
                                return;
                            }

                            document.getElementById("feedback").textContent = "메모를 삭제했습니다.";
                            if (document.getElementById("editing-id").value === String(note.id)) {
                                resetForm();
                            }
                            await loadNotes();
                        });

                        top.appendChild(title);
                        top.appendChild(status);
                        actions.appendChild(editButton);
                        actions.appendChild(deleteButton);
                        item.appendChild(top);
                        item.appendChild(body);
                        item.appendChild(meta);
                        item.appendChild(actions);
                        notesRoot.appendChild(item);
                    });
                } catch (error) {
                    count.textContent = "-";
                    notesRoot.innerHTML = '<div class="empty">메모 서비스를 불러오지 못했습니다. DB 연결 상태를 확인해주세요.</div>';
                }
            }

            async function saveNote(event) {
                event.preventDefault();

                const feedback = document.getElementById("feedback");
                const editingId = document.getElementById("editing-id").value;
                const payload = {
                    title: document.getElementById("title").value.trim(),
                    body: document.getElementById("body").value.trim(),
                    due_date: document.getElementById("due_date").value || null,
                };

                feedback.textContent = editingId ? "수정 중..." : "저장 중...";

                const response = await fetch(editingId ? "/api/notes/" + editingId : "/api/notes", {
                    method: editingId ? "PUT" : "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(payload),
                });

                if (!response.ok) {
                    feedback.textContent = editingId ? "메모 수정에 실패했습니다." : "메모 저장에 실패했습니다.";
                    return;
                }

                resetForm();
                feedback.textContent = editingId ? "메모를 수정했습니다." : "메모를 저장했습니다.";
                await loadNotes();
            }

            document.getElementById("note-form").addEventListener("submit", saveNote);
            document.getElementById("refresh-button").addEventListener("click", loadNotes);
            document.getElementById("cancel-edit-button").addEventListener("click", resetForm);
            resetForm();
            loadNotes();
        </script>
    </body>
    </html>
    """


@app.on_event("startup")
def startup() -> None:
    init_database()


@app.get("/", response_class=HTMLResponse)
def root() -> str:
    return get_notes_page()


@app.get("/healthz")
def healthz() -> dict:
    init_database()
    return {
        "status": "ok",
        "service": "demo-notes",
    }


@app.get("/api/notes")
def list_notes() -> dict:
    try:
        notes = [serialize_note(note) for note in list_note_rows()]
        return {
            "notes": notes,
        }
    except SQLAlchemyError as error:
        raise HTTPException(status_code=503, detail="메모 저장소에 연결할 수 없습니다.") from error


@app.post("/api/notes")
def create_note(payload: NoteCreate) -> dict:
    init_database()

    with get_session() as session:
        note = Note(
            title=payload.title.strip(),
            body=payload.body.strip(),
            due_date=payload.due_date,
            status="open",
        )
        session.add(note)
        session.commit()
        session.refresh(note)
        return {
            "note": serialize_note(note),
        }


@app.put("/api/notes/{note_id}")
def update_note(note_id: int, payload: NoteUpdate) -> dict:
    init_database()

    with get_session() as session:
        note = session.get(Note, note_id)
        if note is None:
            raise HTTPException(status_code=404, detail="Note not found")

        note.title = payload.title.strip()
        note.body = payload.body.strip()
        note.due_date = payload.due_date
        if payload.status:
            note.status = payload.status

        session.commit()
        session.refresh(note)
        return {
            "note": serialize_note(note),
        }


@app.delete("/api/notes/{note_id}")
def delete_note(note_id: int) -> dict:
    init_database()

    with get_session() as session:
        note = session.get(Note, note_id)
        if note is None:
            raise HTTPException(status_code=404, detail="Note not found")

        payload = serialize_note(note)
        session.delete(note)
        session.commit()
        return {
            "note": payload,
        }
