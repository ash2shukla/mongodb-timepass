from json.decoder import JSONDecodeError
import streamlit as st
from ..utils import Page
import streamlit as st
from ..db import MongoDBClient
import json


class UpdatePage(Page):
    RENAME_COLL_OPT = "Update Collection Name"
    UPDATE_DOCS_OPT = "Update Documents"

    def __init__(self, state):
        self.state = state
        self.db_client: MongoDBClient = self.state.db_client

    def write(self):
        st.title("Update")

        opt = st.selectbox(
            "Select Update Type",
            [UpdatePage.RENAME_COLL_OPT, UpdatePage.UPDATE_DOCS_OPT],
        )
        if opt == UpdatePage.RENAME_COLL_OPT:
            db_name = st.selectbox(
                "Select Database", self.db_client.get_database_names()
            )
            coll_from = st.selectbox(
                "Select Collection Name To Update",
                self.db_client.get_collection_names(db_name=db_name),
            )
            coll_to = st.text_input("Enter New Collection Name")
            if coll_to == "" and not any(char in coll_to for char in {"$", "system."}):
                st.info(
                    "Collection Names cant be empty. cant have '$' and cant have 'system.'"
                )
                st.stop()
            if st.button("Update"):
                self.db_client.rename_collection(
                    db_name=db_name, coll_from=coll_from, coll_to=coll_to
                )
        elif opt == UpdatePage.UPDATE_DOCS_OPT:
            db_name = st.selectbox(
                "Select Database", self.db_client.get_database_names()
            )
            coll_name = st.selectbox(
                "Select Collection",
                self.db_client.get_collection_names(db_name=db_name),
            )
            _filter = st.text_area("Filter")

            try:
                _filter = json.loads(_filter)
            except JSONDecodeError:
                st.warning("Must be a valid JSON.")
                st.stop()

            see_filter = st.checkbox("See Filter ?")
            if see_filter:
                st.write(_filter)
            
            see_how_many = st.checkbox("See How Many Match ?")
            if see_how_many:
                count = self.db_client.get_collection_count(db_name=db_name, coll_name=coll_name, _filter=_filter)
                st.write(count)
            update = st.text_input("Update")

            try:
                update = json.loads(update)
            except JSONDecodeError:
                st.warning("Must be a valid JSON.")
                st.stop()

            see_update = st.checkbox("See update ?")
            if see_update:
                st.write(update)

            do_upsert = st.checkbox("Upsert? (Update if found else insert)")

            if st.button("Update"):
                self.db_client.update_documents(
                    db_name=db_name,
                    coll_name=coll_name,
                    _filter=_filter,
                    update=update,
                    upsert=do_upsert,
                )

