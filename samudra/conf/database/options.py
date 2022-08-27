import enum


class DatabaseEngine(str, enum.Enum):
    SQLite = "sqlite"
    MySQL = "mysql"
    CockroachDB = "cockroachdb"
