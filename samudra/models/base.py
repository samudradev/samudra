"""File that contains Base Models that is to be inherited by all models.

The four bases currently available:

- [BaseDataTable][samudra.models.base.BaseDataTable]
- [BaseRelationshipTable][samudra.models.base.BaseRelationshipTable]
- [BaseAttachmentDataTable][samudra.models.base.BaseAttachmentDataTable]
- [BaseStrictDataTable][samudra.models.base.BaseStrictDataTable]
"""
from collections import defaultdict
from typing import List, Dict, Tuple, Type

import peewee
import peewee as pw


class BaseDataTable(pw.Model):
    """The simplest type of data model.
    All other models derive from this model including other base models.

    ## Fields
    - `id` (AutoField): the unique id of the data
        * primary_key: True
    - `tarikh_masuk` (TimestampField): the time it enters the database

    ## Meta
    Meta is subclass of [`BaseDataTable`][samudra.models.base.BaseDataTable] to hold metadata

    ### Attr(Meta)
    - `legacy_table_names` (bool): The naming scheme of models in SQL Tables.
        Set to `False`, so that `CamelCase` model classnames are converted into `camel_case` table names in the database.
        (If set to `True`,`CamelCase` ➡ `camelcase`)
    """

    id = pw.AutoField(primary_key=True)
    tarikh_masuk = pw.TimestampField()

    class Meta:
        legacy_table_names = False


class BaseRelationshipTable(BaseDataTable):
    """Model to hold many-to-many relationships.
    Model classes are named `ModelAXModelB` where
        `ModelA` is any [`BaseAttachmentDataTable`][samudra.models.base.BaseAttachmentDataTable] and
        `ModelB` is any [`BaseDataTable`][samudra.models.base.BaseDataTable].
    """


class BaseAttachmentDataTable(BaseDataTable):
    """Model to hold attachment data that has a many-to-many relationship with the primary data."""

    "The [`BaseRelationshipTable`] that holds the relationship with the primary data."

    @classmethod
    def connects_to(cls, other: BaseDataTable, through: BaseRelationshipTable) -> None:
        """Create a dict that defines connection with [data][samudra.models.base.BaseDataTable] and its [relationship table][samudra.models.base.BaseAttachmentDataTable]

        Args:
            other (BaseDataTable): The data to attach the connection
            through (BaseRelationshipTable): The bridge that holds the many-to-many connections
        """
        cls.connection_table: Dict[str, BaseRelationshipTable] = defaultdict(
            BaseRelationshipTable
        )
        cls.connection_table[other._meta.table_name] = through

    @classmethod
    def __attach__(
        cls, other: BaseDataTable, values: List[Dict[str, str]]
    ) -> pw.ModelSelect:
        """A custom dunder method to attach a single row of attachment data to the primary data.
        Is expected to use when a `other.attach(cls, *args, *kwargs)` method is called.

        Args:
            other (BaseDataTable): An instance of the primary data.
            values (List[Dict[field, value]]): A field:value pair related to this class.

        Raises:
            AttributeError: Raised when the connection table is not set.

        Returns:
            pw.ModelSelect: A list of rows of this table associated with `other`.
        """
        rows = [cls.get_or_create(**value)[0] for value in values]
        for row in rows:
            try:
                cls.connection_table[other._meta.table_name].get_or_create(
                    **{cls._meta.table_name: row.id, other._meta.table_name: other.id}
                )
            except AttributeError:
                raise AttributeError(f"{cls} has no associated connection table")
            except KeyError:
                raise KeyError(f"{cls} has not defined a connection with {other}")
        return getattr(other, cls._meta.table_name)

    @classmethod
    def with_dependencies(cls) -> Tuple[Type[BaseDataTable], ...]:
        """List itself and dependencies tables."""
        # TODO Add ways to programmatically define dependencies
        return cls, *cls.connection_table.values()


class BaseStrictDataTable(BaseDataTable):
    """Model to hold finitely defined data."""

    @classmethod
    def get_or_create(cls, *args, **kwargs) -> None:
        """Overrides the default `cls.get_or_create()` method to render it unusable.
        A finitely defined data must be explicitly defined.

        Raises:
            AttributeError: This method should not be used.
        """
        raise AttributeError(
            f"{cls} is a strict table. Rows can only be created explicitly by the `Model.create` method."
        )
