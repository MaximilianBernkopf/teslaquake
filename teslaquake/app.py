import streamlit as st
import pandas as pd
import numpy as np
from datetime import date
from typing import List

from sqlmodel import Session, col, select

from database import engine
from models import Event
from config import TESLAQUAKE_COLUMNS
from config import TESLAQUAKE_EVENTS
from config import START_DATE_ISO_STR

STREAMLIT_MIN_DATE = date.fromisoformat(START_DATE_ISO_STR)
STREAMLIT_MAX_DATE = date(2017,12,31)

st.set_page_config(
    page_title="Teslaquake", 
    page_icon="⚡", 
    layout="wide", 
    initial_sidebar_state="expanded",
    menu_items={
        'About': """
            # Yes Daddy Elon!
            
            You can find my homepage [here](https://maximilianbernkopf.github.io/data/).
        """
    }
)
st.title('⚡ Teslaquake ⚡')
st.subheader('by Maximum Gainz Bernkopf')


with st.sidebar:
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start date", date(2017, 1, 1), min_value = STREAMLIT_MIN_DATE, max_value=STREAMLIT_MAX_DATE)
    with col2:
        end_date = st.date_input("End date", date(2017, 3, 1), min_value = STREAMLIT_MIN_DATE, max_value=STREAMLIT_MAX_DATE)
        

    min_mag, max_mag = st.slider(
        "Select a range of magnitudes", 
        min_value=0.0,
        max_value=10.0, 
        value=(5.0, 10.0),
        step=0.1
    )

    types_of_interest = st.multiselect(
        "What type of events?",
        TESLAQUAKE_EVENTS,
        ['earthquake', 'sonic boom', 'nuclear explosion'],
        format_func = lambda x: x.capitalize())


def get_filtered_events(min_mag: float, max_mag: float, start_date: date, end_date: date, types_of_interest: List[str]) -> pd.DataFrame:
    with Session(engine) as session:
        statement = (
            select(Event)
            .where(col(Event.mag) >= min_mag, col(Event.mag) <= max_mag)
            .where(col(Event.time) >= start_date, col(Event.time) <= end_date)
            .where(col(Event.type).in_(types_of_interest))
            )
        events = session.exec(statement)
        records = [e.dict() for e in events]
        df = pd.DataFrame.from_records(records)

    return df


filtered_events_df = get_filtered_events(
    min_mag=min_mag, 
    max_mag=max_mag, 
    start_date=start_date, 
    end_date=end_date,
    types_of_interest=types_of_interest
    )

if len(filtered_events_df.index) == 0:
    st.warning('There is no data available for your current selection....', icon="⚠️")

else:
    filtered_events_df = filtered_events_df[TESLAQUAKE_COLUMNS]

    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.dataframe(filtered_events_df)

    st.subheader('Histogram by Magnitude')
    hist_values = np.histogram(filtered_events_df['mag'], bins=50, range=(0,10))[0]
    st.bar_chart(hist_values)

    st.subheader('Map of all events')
    st.map(filtered_events_df)