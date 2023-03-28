from collections import defaultdict
from pathlib import Path
from typing import Dict, Optional, Union, Any

import pytomlpp as toml

HOME: Path = Path("~")

dotconfig = Path(HOME, ".samudra").expanduser()
database_list_file = Path(dotconfig, "databases.toml")
config_file = Path(dotconfig, "config.toml")

database_list_file.touch()
config_file.touch()

if not dotconfig.exists():
    dotconfig.mkdir()


def append_database_list(name: str, path: Union[Path, str], engine: str):
    databases: Dict[Dict] = defaultdict(dict)
    databases[name] = {"path": path.resolve().__str__(), "engine": engine}
    with open(database_list_file, mode="a") as f:
        f.write(toml.dumps({"databases": databases}))


def read_databases_list() -> dict:
    return toml.load(database_list_file)


def read_database_info(name: str) -> Optional[dict]:
    return read_databases_list().get("databases").get(name, None)


def read_config(key: Optional[str] = None) -> Any:
    configs = toml.load(config_file, mode="r")
    if key:
        return configs.get(key)
    return configs


def write_config(content: Dict) -> None:
    configs = read_config(key=None)
    for key, val in zip(content.keys(), content.values()):
        configs[key] = val
    toml.dump(configs, config_file, mode="w")
