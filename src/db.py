import streamlit as st

import pymongo
from bson.json_util import dumps
from json import loads
from functools import lru_cache


class MongoDBClient:
    def __init__(self, CONN_URI):
        self.conn = pymongo.MongoClient(CONN_URI)

    def get_database_names(self):
        return self.conn.list_database_names()

    def get_collection_names(self, db_name):
        db = self.conn[db_name]
        return db.list_collection_names()

    @lru_cache(maxsize=1024)
    def get_collection_count(self, db_name, coll_name):
        doc_count = self.conn[db_name][coll_name].count_documents({})
        return doc_count

    def __del__(self):
        self.conn.close()

    @lru_cache(maxsize=1024)
    def collect_documents(self, db_name, coll_name, page, query, projection, page_size, page_number):
        query = loads(query)
        projection = loads(projection)
        st.write("Cache missing:")
        result = []
        if projection != "":
            data = list(self.conn[db_name][coll_name].find(query, projection).skip((page-1)*page_size).limit(page_size))
        else:
            data = list(self.conn[db_name][coll_name].find(query).skip((page-1)*page_size).limit(page_size))
        for record in data:
            json_str = dumps(record)
            result.append(loads(json_str))
        return result
