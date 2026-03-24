
# =========================
# Database
# =========================

from __future__ import annotations
from helpers import *
from configuration import *
import json
import sqlite3
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Tuple

import pandas as pd

# =========================
# Data Model
# =========================
@dataclass
class Reservation:
    reservation_number: str
    guest_name: str
    check_in: date
    check_out: date  # exclusive (guest leaves that day)
    created_at: datetime


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reservation_number TEXT NOT NULL UNIQUE,
            guest_name TEXT NOT NULL,
            check_in TEXT NOT NULL,
            check_out TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS capacity_overrides (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            capacity INTEGER NOT NULL,
            note TEXT,
            created_at TEXT NOT NULL
        );
        """
    )
    conn.execute("CREATE INDEX IF NOT EXISTS idx_capacity_overrides_dates ON capacity_overrides(start_date, end_date);")
    conn.commit()

    conn.execute("CREATE INDEX IF NOT EXISTS idx_guest_name ON reservations(guest_name);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_reservation_number ON reservations(reservation_number);")
    conn.commit()


def insert_reservation(conn: sqlite3.Connection, r: Reservation) -> Tuple[bool, str]:
    try:
        conn.execute(
            """
            INSERT INTO reservations (reservation_number, guest_name, check_in, check_out, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                r.reservation_number,
                r.guest_name,
                r.check_in.isoformat(),
                r.check_out.isoformat(),
                r.created_at.isoformat(timespec="seconds"),
            ),
        )
        conn.commit()
        return True, "Saved."
    except sqlite3.IntegrityError as e:
        return False, f"Could not save (duplicate reservation number?). Details: {e}"


def fetch_all(conn: sqlite3.Connection) -> pd.DataFrame:
    df = pd.read_sql_query(
        """
        SELECT reservation_number, guest_name, check_in, check_out, created_at
        FROM reservations
        ORDER BY created_at DESC
        """,
        conn,
    )
    return normalize_df(df)


def search_reservations(conn: sqlite3.Connection, query: str) -> pd.DataFrame:
    q = f"%{query.strip()}%"
    df = pd.read_sql_query(
        """
        SELECT reservation_number, guest_name, check_in, check_out, created_at
        FROM reservations
        WHERE guest_name LIKE ? OR reservation_number LIKE ?
        ORDER BY created_at DESC
        """,
        conn,
        params=(q, q),
    )
    return normalize_df(df)


# =========================
# JSON mock data
# =========================
def load_json_reservations(path: str = JSON_PATH) -> pd.DataFrame:
    """
    Expected JSON format (array of objects):
    [
      {"reservation_number":"1234-ABCD","guest_name":"Anna Schmidt","check_in":"2026-01-20","check_out":"2026-01-23"}
    ]
    Optional: created_at
    """
    p = Path(path)
    if not p.exists():
        return pd.DataFrame(columns=["reservation_number", "guest_name", "check_in", "check_out", "created_at", "nights"])

    raw = json.loads(p.read_text(encoding="utf-8"))
    df = pd.DataFrame(raw)
    return normalize_df(df)


# =========================
# Dataframe normalization
# =========================

def normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame(columns=["reservation_number", "guest_name", "check_in", "check_out", "created_at", "nights"])

    # Ensure required columns exist
    for col in ["reservation_number", "guest_name", "check_in", "check_out"]:
        if col not in df.columns:
            df[col] = None

    df["reservation_number"] = df["reservation_number"].astype(str).map(normalize_spaces)
    df["guest_name"] = df["guest_name"].astype(str).map(normalize_spaces)

    df["check_in"] = pd.to_datetime(df["check_in"], errors="coerce").dt.date
    df["check_out"] = pd.to_datetime(df["check_out"], errors="coerce").dt.date

    # created_at is optional (JSON might not include it)
    if "created_at" in df.columns:
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    else:
        df["created_at"] = pd.NaT

    # nights
    df["nights"] = (pd.to_datetime(df["check_out"]) - pd.to_datetime(df["check_in"])).dt.days

    # Drop invalid rows (missing dates or bad ranges)
    df = df.dropna(subset=["check_in", "check_out"])
    df = df[df["check_out"] > df["check_in"]]

    return df


def get_reservations_df(conn: sqlite3.Connection, source: str) -> pd.DataFrame:
    if source == "JSON (mock)":
        return load_json_reservations(JSON_PATH)
    return fetch_all(conn)


def search_reservations_df(conn: sqlite3.Connection, source: str, query: str) -> pd.DataFrame:
    if source == "JSON (mock)":
        df = load_json_reservations(JSON_PATH)
        if not query.strip():
            return df
        q = query.strip().lower()
        mask = df["guest_name"].str.lower().str.contains(q, na=False) | df["reservation_number"].str.lower().str.contains(q, na=False)
        return df[mask].copy()
    return search_reservations(conn, query)
