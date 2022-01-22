from fastapi import HTTPException
from .router import Router
import models


class UsersRouter(Router):

    def __init__(self, config, database):
        super().__init__('/users', config, database)

    def methods(self):

        @self.router.get('/all')
        async def get_users(key: models.ApiKey):

            api_key_check = self.check_api_key(key.key, 'super')
            if api_key_check is not True: raise api_key_check

            with self.database as cursor:
                cursor.execute("SELECT id, nick FROM users")

                users = [{'id': id, 'nick': nick} for id, nick in cursor.fetchall()]

            return users

        @self.router.put('/')
        async def put_user(key: models.ApiKey, user: models.NewUser):

            api_key_check = self.check_api_key(key.key, 'super')
            if api_key_check is not True: raise api_key_check

            with self.database as cursor:

                cursor.execute("SELECT nick FROM users")

                if user.nick.upper() in [user[0].upper() for user in cursor.fetchall()]:
                    raise HTTPException(409, "Nickname already taken")

                cursor.execute("INSERT INTO users (name, nick, password, permission) VALUES (?, ?, ?, ?)",
                               (user.name, user.nick, user.password, user.permission))

                cursor.execute("SELECT id, name, nick, permission FROM users WHERE nick=?", (user.nick,))

                user = cursor.fetchone()

            return {'id': user[0], 'name': user[1], 'nick': user[2], 'permission': user[3]}

        @self.router.delete('/', response_model=models.OldUser)
        async def delete_user(key: models.ApiKey, user: models.OldUser):

            api_key_check = self.check_api_key(key.key, 'super')
            if api_key_check is not True: raise api_key_check

            with self.database as cursor:

                cursor.execute("SELECT id FROM users WHERE id=?", (user.id,))

                if not [user for user in cursor.fetchall()]:
                    raise HTTPException(404, "User does not exist")

                cursor.execute("DELETE FROM users WHERE id=?", (user.id,))

            return user

        @self.router.post('/', response_model=models.User)
        async def post_user(key: models.ApiKey, user: models.EditedUser):

            api_key_check = self.check_api_key(key.key, 'super')
            if api_key_check is not True: raise api_key_check

            with self.database as cursor:

                cursor.execute("SELECT id FROM users WHERE id=?", (user.id,))

                if not [user for user in cursor.fetchall()]:
                    raise HTTPException(404, "User does not exist")

                if user.new_name:
                    cursor.execute("UPDATE users SET name=? WHERE id=?", (user.new_name, user.id))
                if user.new_nick:
                    cursor.execute("UPDATE users SET nick=? WHERE id=?", (user.new_nick, user.id))
                if user.new_password:
                    cursor.execute("UPDATE users SET password=? WHERE id=?", (user.new_password, user.id))
                if user.new_permission:
                    cursor.execute("UPDATE users SET permission=? WHERE id=?", (user.new_permission, user.id))

                cursor.execute("SELECT id, name, nick, permission FROM users WHERE id=?", (user.id,))

                user = cursor.fetchone()

            return {'id': user[0], 'name': user[1], 'nick': user[2], 'permission': user[3]}
