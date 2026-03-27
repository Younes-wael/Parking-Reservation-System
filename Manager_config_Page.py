
from __future__ import annotations
from configuration import DEFAULT_PARKING_SPOTS
from helpers import daterange
import sqlite3
from datetime import date, datetime, timedelta
from typing import Tuple

import pandas as pd
import streamlit as st



def page_manager_config(conn: sqlite3.Connection) -> None:
    st.title("Manager Configuration")
    st.caption("Set temporary parking capacity for a specific date range (bestimmter Zeitraum).")

    st.subheader("Add capacity override")

    with st.form("override_form"):
        c1, c2 = st.columns(2)
        with c1:
            start_date = st.date_input("Start date (inclusive)", value=date.today())
        with c2:
            end_date = st.date_input("End date (inclusive)", value=date.today() + timedelta(days=7))

        new_capacity = st.number_input("Capacity for this period", min_value=0, max_value=5000, value=DEFAULT_PARKING_SPOTS, step=1)
        note = st.text_input("Note (optional)", placeholder="e.g., Construction work / reserved group / blocked area")

        submitted = st.form_submit_button("Save override")

    if submitted:
        errors = []
        if end_date < start_date:
            errors.append("End date must be on/after start date.")
        if int(new_capacity) < 0:
            errors.append("Capacity must be >= 0.")

        if errors:
            st.error("Fix these issues:")
            for e in errors:
                st.write(f"- {e}")
        else:
            ok, msg = add_capacity_override(conn, start_date, end_date, int(new_capacity), note)
            st.success(msg) if ok else st.error(msg)

    st.divider()
    st.subheader("Existing overrides")

    overrides = fetch_capacity_overrides(conn)
    if overrides.empty:
        st.info("No capacity overrides yet.")
        return

    st.dataframe(overrides, use_container_width=True)

    st.markdown("### Delete override")
    override_ids = overrides["id"].tolist()
    selected_id = st.selectbox("Select override ID to delete", override_ids)
    if st.button("Delete selected override"):
        ok, msg = delete_capacity_override(conn, int(selected_id))
        st.success(msg) if ok else st.error(msg)

def add_capacity_override(conn: sqlite3.Connection, start_date: date, end_date: date, capacity: int, note: str = "") -> Tuple[bool, str]:
    try:
        conn.execute(
            """
            INSERT INTO capacity_overrides (start_date, end_date, capacity, note, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                start_date.isoformat(),
                end_date.isoformat(),
                int(capacity),
                note.strip(),
                datetime.now().isoformat(timespec="seconds"),
            ),
        )
        conn.commit()
        return True, "Capacity override saved."
    except Exception as e:
        return False, f"Could not save override. Details: {e}"


def fetch_capacity_overrides(conn: sqlite3.Connection) -> pd.DataFrame:
    df = pd.read_sql_query(
        """
        SELECT id, start_date, end_date, capacity, note, created_at
        FROM capacity_overrides
        ORDER BY created_at DESC
        """,
        conn,
    )
    if not df.empty:
        df["start_date"] = pd.to_datetime(df["start_date"]).dt.date
        df["end_date"] = pd.to_datetime(df["end_date"]).dt.date
        df["created_at"] = pd.to_datetime(df["created_at"])
    return df


def delete_capacity_override(conn: sqlite3.Connection, override_id: int) -> Tuple[bool, str]:
    try:
        cur = conn.execute("DELETE FROM capacity_overrides WHERE id = ?", (int(override_id),))
        conn.commit()
        if cur.rowcount == 0:
            return False, "Override not found."
        return True, "Override deleted."
    except Exception as e:
        return False, f"Could not delete override. Details: {e}"


def effective_capacity_by_day(conn: sqlite3.Connection, default_capacity: int, start: date, end: date) -> pd.DataFrame:
    """
    Returns a DataFrame with columns: day, capacity
    Applies the most recently created override that covers the day (if multiple overlap).
    """
    days = daterange(start, end)
    if not days:
        return pd.DataFrame({"day": [], "capacity": []})

    cap_df = pd.DataFrame({"day": days})
    cap_df["capacity"] = int(default_capacity)

    overrides = fetch_capacity_overrides(conn)
    if overrides.empty:
        return cap_df

    # Apply overrides from oldest -> newest so newest wins on overlaps
    overrides_sorted = overrides.sort_values("created_at", ascending=True)

    for _, row in overrides_sorted.iterrows():
        s = row["start_date"]
        e = row["end_date"]
        c = int(row["capacity"])
        mask = (cap_df["day"] >= s) & (cap_df["day"] <= e)
        cap_df.loc[mask, "capacity"] = c

    return cap_df
