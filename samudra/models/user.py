from peewee import TextField

from samudra.models.base import BaseTable


class User(BaseTable):
    username = TextField(null=False)
    password_hash = TextField(null=False)

    def __repr__(self) -> str:
        return f'<model.{self.__class__.__name__}: id={self.id} username={self.username} password_hash={self.password_hash}>'
