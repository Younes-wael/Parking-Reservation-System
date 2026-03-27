
from __future__ import annotations
import sqlite3

from db_verwaltung import search_reservations_df

import streamlit as st


def page_reservations(conn: sqlite3.Connection, source: str) -> None:
    st.title("Reservations")
    st.caption("Search by guest name or reservation number.")

    query = st.text_input("Search", placeholder="e.g., Schmidt or 1234-ABCD")

    df = search_reservations_df(conn, source, query)

    st.write(f"Results: **{len(df)}**")

    if df.empty:
        st.info("No reservations found.")
        return

    show_cols = ["reservation_number", "guest_name", "check_in", "check_out", "nights", "created_at"]
    # created_at may be NaT for JSON mock data; still safe to show
    st.dataframe(df[show_cols], use_container_width=True)

    with st.expander("Download CSV"):
        csv_bytes = df[show_cols].to_csv(index=False).encode("utf-8")
        st.download_button("Download", csv_bytes, file_name="reservations.csv", mime="text/csv")
