from pathlib import Path
from typing import Dict, List, Type

from FoulLanguageStatus import FoulLanguageStatus

class DatabaseManager:
    def __init__(self, location: Path = None):
        if location is None:
            self.location = ":memory:"
        else:
            self.location = location
            if not location.exists():
                location.parent.mkdir(parents=True, exist_ok=True)
                self.initialize_database()

    def initialize_database(self) -> None:
        pass

    def insert_post(self, title: str, paragraphs: List[str]) -> int:
        pass

    def get_post_ids(self, only_unverified: bool = False, limit: int = 1) -> List[int]:
        pass

    def get_post_statements(self, post_id: int, only_unverified: bool = False) -> Dict[int, str]:
        pass

    def update_statements_status(self, new_status: Dict[int, Type[FoulLanguageStatus]]) -> None:
        pass

    def update_post_status(self, post_id: int, new_status: Type[FoulLanguageStatus]) -> None:
        pass
