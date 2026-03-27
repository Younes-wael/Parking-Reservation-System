
from __future__ import annotations
from Home_Page import *
import sqlite3
from datetime import date, datetime, timedelta


import streamlit as st

def can_add_reservation(conn: sqlite3.Connection, source: str, capacity: int, df: "pd.DataFrame", check_in: date, check_out: date) -> tuple[bool, str]:
    """
    Returns (ok, message). Blocks if adding 1 reservation would exceed capacity on any day.
    We check occupancy day-by-day in the stay window.
    """
    # Reservation occupies nights: check_in <= day < check_out
    start = check_in
    end = check_out - timedelta(days=1)  # last occupied day (inclusive)

    if end < start:
        return False, "Invalid stay dates."

    cap_by_day = effective_capacity_by_day(conn, capacity, start, end)
    occ = occupancy_by_day(df, start, end, cap_by_day)

    # after adding this new reservation, occupied would be +1
    occ["available_after"] = occ["available"] - 1


    bad = occ[occ["available_after"] < 0]
    if not bad.empty:
        # Pick the first date that fails
        first_bad_day = bad.iloc[0]["day"]
        return (
            False,
            f"No parking spots left available for this stay. First fully booked day: {first_bad_day}.",
        )

    return True, "OK"


def page_new_reservation(conn: sqlite3.Connection, source: str, capacity: int) -> None:
    st.title("New Reservation")
    st.caption(f"Create a parking reservation for **{HOTEL_NAME}**")

    if source == "JSON (mock)":
        st.warning(
            "You are using **JSON (mock)** as the data source. "
            "Creating reservations will save to **SQLite**, not to the JSON file."
        )

    with st.form("new_reservation_form"):
        reservation_number = st.text_input("Reservation number", placeholder="e.g., 1234-ABCD")
        guest_name = st.text_input("Guest full name", placeholder="e.g., Anna Schmidt")

        col1, col2 = st.columns(2)
        with col1:
            check_in = st.date_input("Check-in date", value=date.today())
        with col2:
            check_out = st.date_input("Check-out date", value=date.today() + timedelta(days=1))

        submitted = st.form_submit_button("Save")

    if not submitted:
        return

    reservation_number_clean = normalize_spaces(reservation_number)
    guest_name_clean = normalize_spaces(guest_name)

    errors = []
    if not is_valid_reservation_number(reservation_number_clean):
        errors.append("Reservation number must be 4–32 chars and contain only letters/numbers/dashes.")
    if len(guest_name_clean) < 2:
        errors.append("Guest name looks too short.")
    if check_out <= check_in:
        errors.append("Check-out must be after check-in.")
    if nights_between(check_in, check_out) > 60:
        errors.append("Stay seems unusually long (> 60 nights). If valid, remove/adjust this rule.")

    if errors:
        st.error("Fix these issues:")
        for e in errors:
            st.write(f"- {e}")
        return

    r = Reservation(
        reservation_number=reservation_number_clean,
        guest_name=guest_name_clean,
        check_in=check_in,
        check_out=check_out,
        created_at=datetime.now(),
    )
    df = get_reservations_df(conn, source)
    cap_ok, cap_msg = can_add_reservation(conn, source, capacity, df, check_in, check_out)
    if cap_ok:
        ok, msg = insert_reservation(conn, r)
    else:
        ok, msg = False, cap_msg


    if ok:
        st.success(msg)
    else:
        st.error(msg)


def page_availability(conn: sqlite3.Connection, source: str, capacity: int) -> None:
    st.title("Availability")
    st.caption("Check parking availability by date range.")

    df = get_reservations_df(conn, source)

    c1, c2 = st.columns(2)
    with c1:
        start = st.date_input("From", value=date.today())
    with c2:
        end = st.date_input("To", value=date.today() + timedelta(days=14))

    if end < start:
        st.error("End date must be on/after start date.")
        return

    cap_by_day = effective_capacity_by_day(conn, capacity, start, end)
    occ = occupancy_by_day(df, start, end, cap_by_day)

    st.markdown("### Availability chart")
    # This will NOT crash now, because 'available' always exists.
    st.bar_chart(occ.set_index("day")[["available"]])

    st.markdown("### Daily detail")
    st.dataframe(occ, use_container_width=True)

    if not occ.empty:
        min_avail_day = occ.loc[occ["available"].idxmin(), "day"]
        min_avail_val = int(occ["available"].min())
        st.info(f"Lowest availability in range: **{min_avail_val}** spots on **{min_avail_day}**.")
