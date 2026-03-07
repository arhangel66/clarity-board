"""Tests for EventService."""

import json
import tempfile
from pathlib import Path

from app.services.event_service import EventService


def test_session_start_writes_event():
    with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
        path = f.name

    svc = EventService(log_path=path)
    svc.session_start("sess-1", "user-1")

    lines = Path(path).read_text().strip().split("\n")
    assert len(lines) == 1
    event = json.loads(lines[0])
    assert event["event"] == "session_start"
    assert event["session_id"] == "sess-1"
    assert event["user_id"] == "user-1"
    assert "timestamp" in event


def test_card_created_writes_event():
    with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
        path = f.name

    svc = EventService(log_path=path)
    svc.card_created("sess-1", "user-1", "fact", "ai")

    lines = Path(path).read_text().strip().split("\n")
    event = json.loads(lines[0])
    assert event["event"] == "card_created"
    assert event["card_type"] == "fact"
    assert event["created_by"] == "ai"


def test_phase_changed_writes_event():
    with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
        path = f.name

    svc = EventService(log_path=path)
    svc.phase_changed("sess-1", "user-1", "question", "facts")

    lines = Path(path).read_text().strip().split("\n")
    event = json.loads(lines[0])
    assert event["event"] == "phase_changed"
    assert event["from_phase"] == "question"
    assert event["to_phase"] == "facts"


def test_multiple_events_append():
    with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
        path = f.name

    svc = EventService(log_path=path)
    svc.session_start("s1", "u1")
    svc.ai_call("s1", "u1", 42)
    svc.connection_created("s1", "u1", "relates")

    lines = Path(path).read_text().strip().split("\n")
    assert len(lines) == 3
    events = [json.loads(line)["event"] for line in lines]
    assert events == ["session_start", "ai_call", "connection_created"]


def test_session_end_includes_metrics():
    with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
        path = f.name

    svc = EventService(log_path=path)
    svc.session_end("s1", "u1", card_count=7, phase="connections")

    event = json.loads(Path(path).read_text().strip())
    assert event["event"] == "session_end"
    assert event["card_count"] == 7
    assert event["phase_reached"] == "connections"
