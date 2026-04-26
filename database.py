import sqlite3
from datetime import datetime

DATABASE_NAME = "insurance_copilot.db"


def create_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    return connection


def initialize_database():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workflow_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            request_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            module_name TEXT NOT NULL,
            risk_level TEXT,
            route TEXT,
            confidence REAL,
            escalation_flag TEXT,
            human_review_required TEXT,
            latency_seconds REAL,
            status TEXT NOT NULL,
            notes TEXT
        )
    """)

    connection.commit()
    connection.close()


def save_workflow_event(
    event_type,
    request_id,
    module_name,
    risk_level=None,
    route=None,
    confidence=None,
    escalation_flag=None,
    human_review_required=None,
    latency_seconds=None,
    status="Completed",
    notes=None
):
    connection = create_connection()
    cursor = connection.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO workflow_events (
            event_type,
            request_id,
            timestamp,
            module_name,
            risk_level,
            route,
            confidence,
            escalation_flag,
            human_review_required,
            latency_seconds,
            status,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        event_type,
        request_id,
        timestamp,
        module_name,
        risk_level,
        route,
        confidence,
        escalation_flag,
        human_review_required,
        latency_seconds,
        status,
        notes
    ))

    connection.commit()
    connection.close()


def get_all_workflow_events():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            event_type,
            request_id,
            timestamp,
            module_name,
            risk_level,
            route,
            confidence,
            escalation_flag,
            human_review_required,
            latency_seconds,
            status,
            notes
        FROM workflow_events
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    connection.close()

    return rows