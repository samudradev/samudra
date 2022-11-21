from collections import defaultdict
from pathlib import Path
from typing import List, Dict, Optional

import pytomlpp as toml

HOME: Path = Path("~")

dotconfig = Path(HOME, ".samudra").expanduser()
db_dotconfig = Path(dotconfig, "databases.toml")

if not dotconfig.exists():
    dotconfig.mkdir()


def save_database(db_name: str, path: Path):
    databases: Dict[Dict] = defaultdict(dict)
    databases[db_name] = path.resolve().__str__()
    with open(db_dotconfig, mode="a") as f:
        f.write(toml.dumps({"databases": databases}))


def get_databases_config() -> dict:
    with open(db_dotconfig, mode="r") as f:
        return toml.load(f)


def get_database_info(name: str) -> Optional[dict]:
    return get_databases_config().get("databases").get(name, None)
