from json.decoder import JSONDecodeError
import streamlit as st
from ..utils import Page
import streamlit as st
from ..db import MongoDBClient
import json


class DeletePage(Page):
    DROP_DB_OPT = "Drop database"
    DROP_COLL_OPT = "Drop collection"
    DELETE_DOC_OPT = "Remove document(s)"

    def __init__(self, state):
        self.state = state
        self.db_client: MongoDBClient = self.state.db_client

    def write(self):
        st.title("Remove")
        
        obj_type = st.selectbox("Select object to remove", [DeletePage.DROP_DB_OPT, DeletePage.DROP_COLL_OPT, DeletePage.DELETE_DOC_OPT])

        if obj_type == DeletePage.DROP_DB_OPT:
            db_name = st.selectbox("Select Database Name", self.db_client.get_database_names())
            

            st.write("You sure about dropping the db ? 😯")
            if st.button("DROP DATABASE"):
                self.db_client.drop_database(db_name=db_name)

        
        elif obj_type == DeletePage.DROP_COLL_OPT:
            db_name = st.selectbox("Select Database Name", self.db_client.get_database_names())
            coll_name = st.selectbox("Select Collection Name", self.db_client.get_collection_names(db_name=db_name))

            st.write("You sure about dropping the collection ? 😯")
            if st.button("DROP COLLECTION"):
                self.db_client.drop_collection(db_name=db_name, coll_name=coll_name)
        
        elif obj_type == DeletePage.DELETE_DOC_OPT:
            db_name = st.selectbox("Select Database Name", self.db_client.get_database_names())
            coll_name = st.selectbox("Select Collection Name", self.db_client.get_collection_names(db_name=db_name))

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
            
            if st.button("Delete"):
                self.db_client.remove_documents(db_name=db_name, coll_name=coll_name, _filter=_filter)
