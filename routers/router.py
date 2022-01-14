from fastapi import APIRouter, HTTPException


class Router:

    def __init__(self, prefix, config, database):
        self.config = config
        self.database = database
        self.router = APIRouter(prefix=prefix)
        self.methods()

    def check_api_key(self, key: str, permission: str = None):

        with self.database as cursor:

            cursor.execute("SELECT permission FROM api_keys WHERE key=?", (key,))

            api_key = cursor.fetchone()

            if not api_key:
                return HTTPException(422, "Invalid API Key")

            if permission and not self.config['KEY_PERMISSIONS'][api_key[0]] <= self.config['KEY_PERMISSIONS'][permission]:
                return HTTPException(403, "API Key does not have enough permissions")

            return True

    def methods(self):
        pass
