import enum

from peewee import TextField, BooleanField, ForeignKeyField

from samudra.models.base import BaseDataTable, BaseStrictDataTable


class RoleEnum(enum.Enum):
    """List of Roles

    ## Values
    - `DEFAULT` = 'BIASA'
    - `ADMIN` = 'ADMIN'
    """

    DEFAULT = "BIASA"
    ADMIN = "ADMIN"


class Keizinan(BaseStrictDataTable):
    """Role model for controlling access types

    ## Fields
    - `peranan` (TextField): name of role
        * null: False
        * unique: True
    - `tambah` (BooleanField): can create
        * null: False
    - `baca` (BooleanField): can read
        * null: False
    - `ubah` (BooleanField): can update
        * null: False
    - `buang` (BooleanField): can delete
        * null: False
    """

    peranan = TextField(null=False, unique=True)
    tambah = BooleanField(null=False)
    baca = BooleanField(null=False)
    ubah = BooleanField(null=False)
    buang = BooleanField(null=False)


class Pengguna(BaseDataTable):
    """User model to store users.

    ## Fields
    - `nama` (TextField): username
        * null: False
    - `kunci` (TextField): hashed password
        * null: False
    - `peranan` (ForeignKeyField): foreign key to [`Keizinan`][samudra.models.auth.pengguna.Keizinan]
        * field: Keizinan.peranan
        * backref: Keizinan.pengguna
        * on delete: set default
        * default: [`RoleEnum.DEFAULT`][samudra.model.auth.pengguna.RoleEnum]
    """

    nama = TextField(null=False)
    kunci = TextField(null=False)
    peranan = ForeignKeyField(
        model=Keizinan,
        field=Keizinan.peranan,
        backref="pengguna",
        on_delete="set default",
        default=RoleEnum.DEFAULT.value,
    )

    def __repr__(self) -> str:
        return f"<model.{self.__class__.__name__}: id={self.id} nama={self.nama} kunci={self.kunci}>"
