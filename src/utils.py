from streamlit.report_thread import get_report_ctx
from streamlit.hashing import _CodeHasher
from streamlit.server.server import Server

from functools import wraps
import pymongo
import base64

from abc import ABC, abstractmethod
from copy import deepcopy

from typing import Dict, Any
import _thread
import io

def _skip_hash(arg):
    pass

# no_hash = {
#     pymongo.auth._Cache: _skip_hash,
#     pymongo.pool.PoolOptions: _skip_hash,
#     pymongo.write_concern.WriteConcern: _skip_hash,
#     _thread.LockType: _skip_hash,
#     pymongo.server_description.ServerDescription: _skip_hash,
#     io.TextIOWrapper: _skip_hash,
# }

class Page(ABC):
    @abstractmethod
    def write(self):
        pass


class _SessionState:
    def __init__(self, session, hash_funcs):
        """Initialize SessionState instance."""
        self.__dict__["_state"] = {
            "data": {},
            "hash": None,
            "hasher": _CodeHasher(hash_funcs),
            "is_rerun": False,
            "session": session,
        }

    def __call__(self, **kwargs):
        """Initialize state data once."""
        for item, value in kwargs.items():
            if item not in self._state["data"]:
                self._state["data"][item] = value

    def __getitem__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)

    def __getattr__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)

    def __setitem__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value

    def __setattr__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value

    def clear(self):
        """Clear session state and request a rerun."""
        self._state["data"].clear()
        self._state["session"].request_rerun()

    def sync(self):
        """Rerun the app with all state values up to date from the beginning to fix rollbacks."""

        # Ensure to rerun only once to avoid infinite loops
        # caused by a constantly changing state value at each run.
        #
        # Example: state.value += 1
        if self._state["is_rerun"]:
            self._state["is_rerun"] = False

        elif self._state["hash"] is not None:
            if self._state["hash"] != self._state["hasher"].to_bytes(
                self._state["data"], None
            ):
                self._state["is_rerun"] = True
                self._state["session"].request_rerun()

        self._state["hash"] = self._state["hasher"].to_bytes(self._state["data"], None)


def _get_session():
    session_id = get_report_ctx().session_id
    session_info = Server.get_current()._get_session_info(session_id)

    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")

    return session_info.session

def get_state(hash_funcs=None):
    session = _get_session()

    if not hasattr(session, "_custom_session_state"):
        session._custom_session_state = _SessionState(session, hash_funcs)

    return session._custom_session_state

# Only used for separating namespace, everything can be saved at state variable as well.
CONFIG_DEFAULTS: Dict[str, Any] = {"slider_value": 0}

def provide_state(hash_funcs=None):
    def inner(func):
        def wrapper(*args, **kwargs):
            state = get_state(hash_funcs=hash_funcs)
            if state.client_config is None:
                state.client_config = deepcopy(CONFIG_DEFAULTS)

            return_value = func(state=state, *args, **kwargs)
            state.sync()
            return return_value

        return wrapper
    return inner


def get_base_64_img(path, format="png", width="", height=""):
    img_bytes = open(path, "rb").read()
    b64_bytes = base64.b64encode(img_bytes).decode()
    return f'<img src=data:image/{format};base64,{b64_bytes} width="{width}" height="{height}">'
