from fastapi import HTTPException
from datetime import datetime

from .router import Router
import models
from secrets import token_hex


class SessionsRouter(Router):

    def __init__(self, config, database):
        super().__init__('/sessions', config, database)

    def methods(self):

        @self.router.get('/all')
        async def get_sessions(key: models.ApiKey):

            api_key_check = self.check_api_key(key.key, 'super')
            if api_key_check is not True: raise api_key_check

            with self.database as cursor:
                cursor.execute("SELECT id, time, user, token FROM sessions")

                sessions = [{'id': id, 'time': time, 'user': user, 'token': token} for id, time, user, token in cursor.fetchall()]

            return sessions

        @self.router.get('/')
        async def get_session(key: models.ApiKey, session: models.Session):

            api_key_check = self.check_api_key(key.key, 'super')
            if api_key_check is not True: raise api_key_check

            with self.database as cursor:

                cursor.execute("SELECT id, user FROM sessions WHERE token=?", (session.token,))
                session = cursor.fetchone()
                if not session:
                    raise HTTPException(404, 'Session does not exist')
                id, user_id = session

                cursor.execute("SELECT permission FROM users WHERE id=?", (user_id,))
                user = cursor.fetchone()
                if not user:
                    raise HTTPException(404, 'User does not exist')
                permission, = user

                session = {'id': id, 'user': user_id, 'permission': permission}

            return session

        @self.router.put('/')
        async def put_session(key: models.ApiKey, session: models.NewSession):

            api_key_check = self.check_api_key(key.key, 'super')
            if api_key_check is not True: raise api_key_check

            with self.database as cursor:

                cursor.execute("SELECT permission FROM users WHERE id=?", (session.user,))
                user = cursor.fetchone()
                if not user:
                    raise HTTPException(404, "User does not exist")
                permission = user[0]

                cursor.execute("DELETE FROM sessions WHERE user=?", (session.user,))

                time = round(datetime.now().timestamp())
                token = token_hex(self.config['TOKEN_SECURITY'][permission])
                cursor.execute("INSERT INTO sessions (time, user, token) VALUES (?, ?, ?)", (time, session.user, token))

                cursor.execute("SELECT id, time, user, token FROM sessions WHERE user=?", (session.user,))
                session = cursor.fetchone()

            return {'id': session[0], 'time': session[1], 'user': session[2], 'token': session[3]}
