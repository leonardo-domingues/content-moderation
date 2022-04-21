from contextlib import closing
from pathlib import Path
from typing import Dict, List, Optional, Type

import sqlite3

from src.FoulLanguageStatus import FoulLanguageStatus

class DatabaseManager:
    def __init__(self, location: Path):
        self.location = location
        if not location.exists():
            location.parent.mkdir(parents=True, exist_ok=True)
            self.__initialize_database()


    def __initialize_database(self) -> None:
        with closing(sqlite3.connect(self.location)) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute('''
                               CREATE TABLE IF NOT EXISTS posts
                               ([id] INTEGER PRIMARY KEY, [title] TEXT, [hasFoulLanguage] INTEGER)
                               ''')
                cursor.execute('''
                               CREATE TABLE IF NOT EXISTS paragraphs
                               ([id] INTEGER PRIMARY KEY, [content] TEXT, [hasFoulLanguage] INTEGER, [postId] INTEGER, FOREIGN KEY(postId) REFERENCES posts(id))
                               ''')
                connection.commit()


    def insert_post(self, title: str, paragraphs: List[str]) -> int:
        with closing(sqlite3.connect(self.location)) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute(f"INSERT INTO posts (title, hasFoulLanguage) VALUES ('{title}', {int(FoulLanguageStatus.UNVERIFIED)});")
                post_id = cursor.lastrowid
                for paragraph in paragraphs:
                    cursor.execute(f"""INSERT INTO paragraphs (content, hasFoulLanguage, postId)
                                       VALUES ('{paragraph}', {int(FoulLanguageStatus.UNVERIFIED)}, {post_id});""")
                connection.commit()
        return post_id


    def get_post_ids(self, only_unverified: bool = False, limit: Optional[int] = None) -> List[int]:
        query_language_suffix = f" WHERE hasFoulLanguage={int(FoulLanguageStatus.UNVERIFIED)}" if only_unverified else ""
        query_limit_suffix = f" limit {limit}" if limit else ""
        query = f"SELECT id FROM posts{query_language_suffix}{query_limit_suffix};"
        with closing(sqlite3.connect(self.location)) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute(query)
                records = cursor.fetchall()
        return [r[0] for r in records]


    def get_post_paragraphs(self, post_id: int, only_unverified: bool = False) -> Dict[int, str]:
        query_language_suffix = f" AND hasFoulLanguage={int(FoulLanguageStatus.UNVERIFIED)}" if only_unverified else ""
        query = f"SELECT id, content FROM paragraphs WHERE postId={post_id}{query_language_suffix};"
        with closing(sqlite3.connect(self.location)) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute(query)
                records = cursor.fetchall()
        return {r[0]:r[1] for r in records}


    def update_paragraphs_status(self, new_status: Dict[int, Type[FoulLanguageStatus]]) -> None:
        with closing(sqlite3.connect(self.location)) as connection:
            with closing(connection.cursor()) as cursor:
                for id, status in new_status.items():
                    query = f"UPDATE paragraphs SET hasFoulLanguage={int(status)} WHERE id={id};"
                    cursor.execute(query)
                connection.commit()


    def update_post_status(self, post_id: int, new_status: Type[FoulLanguageStatus]) -> None:
        with closing(sqlite3.connect(self.location)) as connection:
            with closing(connection.cursor()) as cursor:
                query = f"UPDATE posts SET hasFoulLanguage={int(new_status)} WHERE id={post_id};"
                cursor.execute(query)
                connection.commit()
