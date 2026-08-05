from copy import deepcopy
from typing import List, Dict
#from context_types import MailContext


class ContextChain():
    def __init__(self):
        self._chain:List[Dict] = []
        self._kv_cache: Dict[str, any] = {}
        self._snapshot = None

    def add_context(self, step_name:str, data: any):
        self._chain.append({'step': step_name, 'data': deepcopy(data)})
        self._kv_cache[step_name] = data

    def get_context(self, step_name:str):
        return self._kv_cache.get(step_name)

    def get_all_steps(self):
        return [entry['step'] for entry in self._chain]

    def latest(self):
        return self._chain[-1] if self._chain else None

    def snapshot(self):
        self._snapshot = deepcopy(self._chain)

    def restore(self):
        if self._snapshot:
            self._chain = deepcopy(self._snapshot)
            self._kv_cache = {item['step']: item['data'] for item in self._chain}
