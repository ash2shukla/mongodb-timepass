from json.decoder import JSONDecodeError
import streamlit as st
from ..utils import Page
import streamlit as st
from ..db import MongoDBClient
import json


class CreatePage(Page):
    CREATE_NEW_DB_OPT = "CREATE NEW DATABASE"
    COLL_OPT = "collection"
    DOC_OPT = "document(s)"

    def __init__(self, state):
        self.state = state
        self.db_client: MongoDBClient = self.state.db_client

    def write(self):
        st.title("Create")
        
        obj_type = st.selectbox("Select object to create", [CreatePage.COLL_OPT, CreatePage.DOC_OPT])

        if obj_type == CreatePage.COLL_OPT:
            db_name = st.selectbox("Select Database", self.db_client.get_database_names() + [CreatePage.CREATE_NEW_DB_OPT])
            if db_name == CreatePage.CREATE_NEW_DB_OPT:
                db_name = st.text_input("Database Name ?")
            if db_name == "" and not any(char in db_name for char in {'$', '\\', '/', '.', ' ', '\"'}) and len(db_name) < 64:
                st.info("Database Names cant be empty. cant have '$', '\\', '/', '.', 'space', '\"' (quotes)' and length must be less than 64")
                st.stop()
            coll_name = st.text_input("Collection Name ?")
            if coll_name == "" and not any(char in coll_name for char in {"$", "system."}):
                st.info("Collection Names cant be empty. cant have '$' and cant have 'system.'")
                st.stop()
            
            if st.button("Create"):
                self.db_client.create_collection(db_name=db_name, coll_name=coll_name)

        elif obj_type == CreatePage.DOC_OPT:
            db_name = st.selectbox("Select Database", self.db_client.get_database_names())
            coll_name = st.selectbox("Select Collection", self.db_client.get_collection_names(db_name=db_name))
            document = st.text_area("Document(s) data ?")
            
            try:
                document = json.loads(document)
            except JSONDecodeError:
                st.warning("Must be a valid JSON.")
                st.stop()
            if st.button("Create"):
                self.db_client.insert_docs(db_name, coll_name, document)

            see_doc = st.checkbox("See Document(s) ?")
            if see_doc:
                st.write(document)
