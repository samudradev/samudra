import peewee as pw

from samudra.models import create_tables

mock_db = pw.SqliteDatabase(":memory:")


def bind_test_database(function: callable, *args, **kwargs) -> callable:
    """Decorator to open and close a test database connection"""

    def wrapper():
        try:
            create_tables(mock_db, auth=True, experimental=True)
            function(*args, **kwargs)
        finally:
            mock_db.close()  # All data in `:memory:` database are deleted automatically once closed

    return wrapper
