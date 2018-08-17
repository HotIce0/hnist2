from django.conf.global_settings import SECRET_KEY
import base64
from itsdangerous import URLSafeTimedSerializer


class Token:
    def __init__(self):
        self.security_key = SECRET_KEY
        self.salt = base64.encodebytes(self.security_key.encode(encoding='utf-8'))

    def generate_email_active_token(self, username):
        serializer = URLSafeTimedSerializer(self.security_key)
        return serializer.dumps(username, self.salt)

    def confirm_email_active_token(self, token, expiration=3600):
        serializer = URLSafeTimedSerializer(self.security_key)
        return serializer.loads(token, salt=self.salt, max_age=expiration)
