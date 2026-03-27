# =========================
# UI Pages
# =========================

from __future__ import annotations
import sqlite3
from datetime import date, timedelta

from configuration import HOTEL_NAME
from helpers import daterange
from db_verwaltung import get_reservations_df
from Manager_config_Page import effective_capacity_by_day

import pandas as pd
import streamlit as st


# =========================
# Availability / Occupancy
# =========================
def occupancy_by_day(df: pd.DataFrame, start: date, end: date, capacity_by_day: pd.DataFrame) -> pd.DataFrame:
    """
    capacity_by_day: DataFrame with columns ['day','capacity'] for each day in [start,end]
    Always returns columns: day, capacity, occupied, available
    """
    days = daterange(start, end)
    if not days:
        return pd.DataFrame({"day": [], "capacity": [], "occupied": [], "available": []})

    # Ensure we have capacity for all days
    cap_map = dict(zip(capacity_by_day["day"], capacity_by_day["capacity"]))
    capacities = [int(cap_map.get(d, 0)) for d in days]

    if df.empty:
        out = pd.DataFrame({"day": days, "capacity": capacities, "occupied": [0] * len(days)})
        out["available"] = (out["capacity"] - out["occupied"]).clip(lower=0)
        return out

    ci = pd.to_datetime(df["check_in"])
    co = pd.to_datetime(df["check_out"])

    occupied_counts = []
    for d in days:
        day_ts = pd.Timestamp(d)
        occ = int(((ci <= day_ts) & (day_ts < co)).sum())
        occupied_counts.append(occ)

    out = pd.DataFrame({"day": days, "capacity": capacities, "occupied": occupied_counts})
    out["available"] = (out["capacity"] - out["occupied"]).clip(lower=0)
    return out
def page_home(conn: sqlite3.Connection, source: str, capacity: int) -> None:
    st.title("Parking Reservation System")
    st.caption(f"Hotel: **{HOTEL_NAME}**")

    df = get_reservations_df(conn, source)

    st.subheader("Dashboard")
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

    st.markdown("### KPIs")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Default parking spots", int(capacity))
    k2.metric("Reservations in data source", int(len(df)))
    if not occ.empty:
        k3.metric("Peak occupied (range)", int(occ["occupied"].max()))
        k4.metric("Lowest available (range)", int(occ["available"].min()))
    else:
        k3.metric("Peak occupied (range)", 0)
        k4.metric("Lowest available (range)", int(capacity))

    st.markdown("### Availability overview")
    st.line_chart(occ.set_index("day")[["occupied", "available", "capacity"]])

    st.markdown("### Next 7 days (table)")
    st.dataframe(occ.head(7), use_container_width=True)
