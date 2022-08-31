import streamlit as st
import pandas as pd
from datetime import date
from typing import List
import plotly.figure_factory as ff

import sqlalchemy
from sqlalchemy import create_engine

from sqlmodel import Session, col, select
from config import TESLAQUAKE_DATABASE_URL, DEBUG

from models import Event
from config import TESLAQUAKE_COLUMNS
from config import TESLAQUAKE_EVENTS
from config import START_DATE_ISO_STR

STREAMLIT_MIN_DATE = date.fromisoformat(START_DATE_ISO_STR)
STREAMLIT_MAX_DATE = date(2017,12,31)

# APP CONFIG #####################################################

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

# HELPERS #####################################################

@st.experimental_singleton
def init_connection():
    engine = create_engine(TESLAQUAKE_DATABASE_URL, echo=DEBUG)
    return engine

engine = init_connection()


@st.cache(hash_funcs={sqlalchemy.engine.Engine: id, sqlalchemy.orm.attributes.InstrumentedAttribute: lambda _: None})
def get_filtered_events(
    min_mag: float, 
    max_mag: float, 
    start_date: date, 
    end_date: date, 
    types_of_interest: List[str], 
    engine) -> pd.DataFrame:
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

# APP #####################################################


st.title('⚡ Teslaquake ⚡')
st.caption('by Maximum Gainz Bernkopf')


with st.sidebar:
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start date", date(2017, 1, 1), min_value = STREAMLIT_MIN_DATE, max_value=STREAMLIT_MAX_DATE)
    with col2:
        end_date = st.date_input("End date", date(2017, 31, 12), min_value = STREAMLIT_MIN_DATE, max_value=STREAMLIT_MAX_DATE)
        

    min_mag, max_mag = st.slider(
        "Select a range of magnitudes", 
        min_value=0.0,
        max_value=10.0, 
        value=(0.0, 10.0),
        step=0.1
    )

    types_of_interest = st.multiselect(
        "What type of events?",
        TESLAQUAKE_EVENTS,
        ['earthquake', 'sonic boom', 'nuclear explosion'],
        format_func = lambda x: x.capitalize())


filtered_events_df = get_filtered_events(
    min_mag=min_mag, 
    max_mag=max_mag, 
    start_date=start_date, 
    end_date=end_date,
    types_of_interest=types_of_interest,
    engine=engine
    )

if len(filtered_events_df.index) == 0:
    st.warning('There is no data available for your current selection....', icon="⚠️")

else:

    st.subheader(f"The biggest events for your current selection is:")
    biggest_event = filtered_events_df[filtered_events_df['mag'] == filtered_events_df['mag'].max()]
    st.dataframe(biggest_event.reset_index())
    filtered_events_df = filtered_events_df[TESLAQUAKE_COLUMNS]


    st.subheader('Histogram by Magnitude')
    fig = ff.create_distplot([filtered_events_df['mag']], ['Magnitude'], bin_size=.2, show_rug=False)
    fig.update_xaxes(title_text='Magnitude')
    st.plotly_chart(fig, use_container_width=True)


    st.subheader('Most probable hour')
    st.markdown("""Below we consider a density plot
     of the hour for each of the buckets. 
     Interpredation is open for discussion :)
     """)
    bins = [0, 1, 2, 3, 4, 5, 6, 10]
    labels = ["0-1", "1-2", "2-3", "3-4", "4-5", "5-6", "6-10"]
    filtered_events_df['bin'] = pd.cut(filtered_events_df['mag'], bins=bins, labels=labels)
    filtered_events_df['hour'] = filtered_events_df['time'].dt.hour

    tmp = []
    for label in labels:
        tmp.append(filtered_events_df[filtered_events_df['bin']==label]['hour'])

    fig = ff.create_distplot(tmp, labels, show_hist=False, show_rug=False)
    fig.update_xaxes(title_text='Hour')

    st.plotly_chart(fig, use_container_width=True)


    st.subheader('Map of all events')
    st.map(filtered_events_df)
    

    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.dataframe(filtered_events_df)
