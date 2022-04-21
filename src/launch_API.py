from pathlib import Path

from src.APIController import APIController

if __name__ == "__main__":
    controller = APIController("127.0.0.1", 5000, Path("database.db"))
    controller.start()