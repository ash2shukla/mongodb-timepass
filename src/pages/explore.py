import streamlit as st
from ..utils import Page
import streamlit as st
from math import ceil
from json import loads, JSONDecodeError
import json


class ExplorePage(Page):
    def __init__(self, state):
        self.state = state
        self.db_client = self.state.db_client

    def write(self):
        st.title("Explore Data")
        db_name = st.sidebar.selectbox(
            "Select database: ", self.db_client.get_database_names()
        )
        coll_name = st.sidebar.selectbox(
            "Select collection: ", self.db_client.get_collection_names(db_name=db_name)
        )
        total_documents = st.sidebar.empty()

        document_count = self.db_client.get_collection_count(
            db_name=db_name, coll_name=coll_name
        )

        find_query = st.sidebar.empty()
        find_warning = st.sidebar.empty()
        projection = st.sidebar.empty()
        projection_warning = st.sidebar.empty()

        st.sidebar.markdown("---")

        page_size = st.sidebar.number_input(
            "Page Size", min_value=1, max_value=1000, value=10
        )

        page_number = st.number_input(
            label="Page Number",
            min_value=1,
            max_value=ceil(document_count / page_size),
            step=1,
        )

        total_documents.markdown(f"Total Documents: {document_count}")

        find_str = find_query.text_input(
            "Find Query to Run on selected Collection", value="{}"
        )

        try:
            find_str = loads(find_str)
        except JSONDecodeError as e:
            find_warning.warning("Find string should be a valid JSON")
            st.stop()

        project_str = projection.text_input(
            "Projection to Filter on selected Collection", value=""
        )

        try:
            if project_str != "":
                project_str = loads(project_str)
        except JSONDecodeError as e:
            projection_warning.warning("Projection String should be a valid JSON")
            st.stop()

        # dump back to string to avoid unhashable type dict in LRU cache
        st.write(
            self.db_client.collect_documents(
                db_name=db_name,
                coll_name=coll_name,
                page=page_number,
                query=json.dumps(find_str),
                projection=json.dumps(project_str),
                page_size=page_size,
                page_number=page_number,
            )
        )

