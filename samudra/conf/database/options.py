import enum


class DatabaseEngine(enum.Enum):
    SQLite = 'sqlite'
    MySQL = 'mysql'
    CockroachDB = 'cockroachdb'
