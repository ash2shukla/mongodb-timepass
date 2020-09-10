import streamlit as st

from src.utils import Page, provide_state, get_base_64_img, _skip_hash
from src.pages import ExplorePage, CreatePage
from pathlib import Path
from src.db import MongoDBClient

import pymongo

from typing import Dict, Type

PAGE_MAP: Dict[str, Type[Page]] = {
    "Explore": ExplorePage,
    "Create": CreatePage
}


@provide_state(hash_funcs={MongoDBClient: _skip_hash})
def main(state=None):
    st.beta_set_page_config(
        page_title="MongoDB TimePass",
        layout="centered",
        initial_sidebar_state="auto",
    )

    logo_uri = get_base_64_img(Path(__file__).parent / "assets" / "timepass-logo.png")

    st.sidebar.markdown(logo_uri, unsafe_allow_html=True)

    CONN_URI = st.sidebar.text_input("Connection URI")

    if CONN_URI == "":
        st.sidebar.info("Input a connection URI")
        st.stop()

    current_page = st.sidebar.radio("Go To", list(PAGE_MAP))

    if state.db_client is None or state.CONN_URI != CONN_URI:
        # different sessions can have differnet DB Connections
        state.db_client = MongoDBClient(CONN_URI)
        state.CONN_URI = CONN_URI

    PAGE_MAP[current_page](state=state).write()


if __name__ == "__main__":
    main()
