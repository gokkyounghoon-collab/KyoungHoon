import os
import sys
from alembic.config import Config
from alembic import command


def get_alembic_config() -> Config:
    config_path = os.path.join(os.path.dirname(__file__), "alembic.ini")
    config = Config(config_path)
    database_url = os.getenv("GAEUN_DATABASE_URL")
    if database_url:
        config.set_main_option("sqlalchemy.url", database_url)
    return config


def main() -> int:
    if len(sys.argv) < 2:
        print("사용법: python migrate_db.py <upgrade|downgrade|current|history> [revision]")
        return 1

    action = sys.argv[1]
    revision = sys.argv[2] if len(sys.argv) > 2 else "head"
    config = get_alembic_config()

    if action == "upgrade":
        command.upgrade(config, revision)
    elif action == "downgrade":
        command.downgrade(config, revision)
    elif action == "current":
        command.current(config)
    elif action == "history":
        command.history(config)
    else:
        print("지원하지 않는 명령입니다:", action)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
