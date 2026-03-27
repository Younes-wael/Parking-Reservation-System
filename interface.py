# app.py
# Mercure Hotel Frankfurt Airport Langen — Parking Reservation System
# Streamlit multi-page UI + SQLite persistence + optional JSON mock data source

from __future__ import annotations
import streamlit as st

from configuration import HOTEL_NAME, DEFAULT_PARKING_SPOTS
import sqlite3

from db_verwaltung import get_conn, init_db
from Home_Page import page_home
from reservation_Page import page_reservations
from new_reservation import page_new_reservation, page_availability
from Manager_config_Page import page_manager_config










# =========================
# UI Pages
# =========================








# =========================
# App Bootstrap
# =========================
@st.cache_resource
def _get_db() -> sqlite3.Connection:
    """Create and initialise the DB connection once; reused across all reruns."""
    conn = get_conn()
    init_db(conn)
    return conn


def main() -> None:
    st.set_page_config(page_title=f"{HOTEL_NAME} — Parking", layout="wide")

    conn = _get_db()

    with st.sidebar:
        st.header("Navigation")


        page = st.radio(
            "Go to",
            ["Home", "Reservations", "New Reservation", "Availability", "Manager Config"],
            index=0,
        )

        st.divider()
        st.subheader("Settings")
        source = st.selectbox("Data source", ["SQLite (real)", "JSON (mock)"], index=0)
        capacity = st.number_input(
            "Total parking spots",
            min_value=1,
            max_value=5000,
            value=DEFAULT_PARKING_SPOTS,
            step=1,
            help="Used for availability calculations (occupied vs available).",
        )

        st.caption("SQLite data file: parking_reservations.db")
        st.caption("Mock JSON file: data.json (optional)")

    if page == "Home":
        page_home(conn, source, int(capacity))
    elif page == "Reservations":
        page_reservations(conn, source)
    elif page == "New Reservation":
        page_new_reservation(conn, source, int(capacity))
    elif page == "Availability":
        page_availability(conn, source, int(capacity))
    elif page == "Manager Config":
        page_manager_config(conn)



if __name__ == "__main__":
    main()
