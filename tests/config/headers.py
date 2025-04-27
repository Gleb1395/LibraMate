import os

from dotenv import load_dotenv


from tests.utils.auth import login

load_dotenv()

ADMIN_EMAIL = os.getenv("API_EMAIL_ADMIN")
ADMIN_PASSWORD = os.getenv("API_LOGIN_PASSWORD_ADMIN")

USER_EMAIL = os.getenv("API_EMAIL_USER")
USER_PASSWORD = os.getenv("API_LOGIN_PASSWORD_USER")


class Headers:

    @classmethod
    def admin(cls):
        token = login(email=ADMIN_EMAIL, password=ADMIN_PASSWORD)
        return {"Authorization": f"Bearer {token['access']}"}

    @classmethod
    def user(cls):
        token = login(email=USER_EMAIL, password=USER_PASSWORD)
        return {"Authorization": f"Bearer {token['access']}"}
