import streamlit as st

import pymongo
from bson import json_util
import json
from functools import lru_cache


class MongoDBClient:
    def __init__(self, CONN_URI):
        self.conn = pymongo.MongoClient(CONN_URI)

    def get_database_names(self):
        return self.conn.list_database_names()

    def get_collection_names(self, db_name):
        db = self.conn[db_name]
        return db.list_collection_names()

    def get_collection_count(self, db_name, coll_name, _filter=None):
        if _filter is None:
            _filter = {}
        doc_count = self.conn[db_name][coll_name].count_documents(_filter)
        return doc_count

    def collect_documents(
        self, db_name, coll_name, page, query, projection, page_size, page_number
    ):
        query = json.loads(query)
        projection = json.loads(projection)
        result = []
        if projection != "":
            data = list(
                self.conn[db_name][coll_name]
                .find(query, projection)
                .skip((page - 1) * page_size)
                .limit(page_size)
            )
        else:
            data = list(
                self.conn[db_name][coll_name]
                .find(query)
                .skip((page - 1) * page_size)
                .limit(page_size)
            )
        for record in data:
            json_str = json_util.dumps(record)
            result.append(json.loads(json_str))
        return result

    def create_collection(self, db_name, coll_name):
        return self.conn[db_name].create_collection(coll_name)

    def insert_docs(self, db_name, coll_name, document):
        if isinstance(document, dict):
            return self.conn[db_name][coll_name].insert_one(document)
        elif isinstance(document, list):
            return self.conn[db_name][coll_name].insert_many(document)

    def rename_collection(self, db_name, coll_from, coll_to):
        return self.conn[db_name][coll_from].rename(coll_to)

    def update_documents(self, db_name, coll_name, _filter, update, upsert):
        return self.conn[db_name][coll_name].update_many(_filter, update, upsert=upsert)
    
    def drop_database(self, db_name):
        return self.conn.drop_database(db_name)

    def drop_collection(self, db_name, coll_name):
        return self.conn[db_name].drop_collection(coll_name)
    
    def remove_documents(self, db_name, coll_name, _filter):
        return self.conn[db_name][coll_name].delete_many(_filter)

    def __del__(self):
        self.conn.close()
