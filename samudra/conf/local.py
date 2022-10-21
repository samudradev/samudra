from pathlib import Path
from typing import List, Dict

import pytomlpp as toml

HOME: Path = Path("~")

dotconfig = Path(HOME, ".samudra").expanduser()

if not dotconfig.exists():
    dotconfig.mkdir()


def save_db(db_name: str, path: Path):
    databases: List[Dict] = list()
    databases.append({"name": db_name, "path": f"{path.resolve()}"})
    with open(Path(dotconfig, "databases.toml"), mode="a") as f:
        f.write(toml.dumps({"databases": databases}))


def list_db():
    with open(Path(dotconfig, "databases.toml"), mode="r") as f:
        return toml.load(f)
