from pathlib import Path

from src.ContentModerator import ContentModerator

if __name__ == "__main__":
    content_moderator = ContentModerator(Path("database.db"))
    content_moderator.run()