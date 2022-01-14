config = \
    {
        "HOST": "localhost",
        "PORT": 8000,
        "DATABASE": "database.db",

        "KEY_PERMISSIONS": {
            "super": 0
        },

        "USER_PERMISSIONS": {
            "owner": 0,
            "admin": 1,
            "default": 2,
            "banned": 3
        },

        "TOKEN_SECURITY": {
            "superkey": 64,
            "owner": 64,
            "admin": 32,
            "default": 16
        }

    }
