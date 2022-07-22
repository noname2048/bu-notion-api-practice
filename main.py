"""
A CLI tools for requests make multiple fakeruser in notion db
"""
from pprint import pprint
from datetime import timezone, timedelta, datetime

import requests
from pydantic import BaseSettings
from IPython import embed

from faker import Faker

KST = timezone(timedelta(hours=9))


class Setting(BaseSettings):
    """
    Settings exchange .env file to python data class
    """

    notion_api_key: str
    db_id: str

    class Config:
        """
        Metadatas
        """

        env_file = ".env"
        env_file_encoding = "utf-8"


setting: Setting = Setting()
url: str = "https://api.notion.com/v1/pages"
headers: dict = {
    "Authorization": f"Bearer {setting.notion_api_key}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}
fake = Faker("ko_KR")


def post_notion():
    """
    Post notion to create page (user)
    """
    data: dict = {
        "parent": {"database_id": setting.db_id},
        "properties": {
            "이름": {"title": [{"text": {"content": fake.name()}}]},
            "email": {"email": fake.email()},
            "created_at": {"date": {"start": str(datetime.now(tz=KST).date())}},
        },
    }
    response = requests.post(
        url=url,
        json=data,
        headers=headers,
    )
    print(status_code := response.status_code)
    if status_code != 200:
        pprint(response.json())
        embed()


if __name__ == "__main__":
    for _ in range(10):
        post_notion()
