from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.compiler import SQLInsertCompiler as BaseSQLInsertCompiler  # noqa
from django.db.models.sql.compiler import SQLDeleteCompiler
from django.db.models.sql.compiler import SQLUpdateCompiler as BaseSQLUpdateCompiler  # noqa
from django.db.models.sql.compiler import SQLAggregateCompiler

SQLCompiler = SQLCompiler
SQLDeleteCompiler = SQLDeleteCompiler
SQLAggregateCompiler = SQLAggregateCompiler


class ReadOnlySQLCompilerMixin(object):

    @property
    def read_only_field_names(self):
        try:
            read_only_meta = getattr(self.query.model, "ReadOnlyMeta")
        except AttributeError:
            return ()
        else:
            fields = getattr(read_only_meta, "_cached_read_only", None)
            if not fields:
                read_only_meta._cached_read_only = fields = frozenset(
                    getattr(read_only_meta, "read_only", ()))
            return fields

    def as_sql(self):
        read_only_field_names = self.read_only_field_names
        if read_only_field_names:
            self.remove_read_only_fields(read_only_field_names)
        return super(ReadOnlySQLCompilerMixin, self).as_sql()


class SQLUpdateCompiler(ReadOnlySQLCompilerMixin, BaseSQLUpdateCompiler):

    def remove_read_only_fields(self, read_only_field_names):
        """
        Remove the values from the query which correspond to a
        read_only field
        """
        values = self.query.values

        # The tuple is (field, model, value) where model if used for FKs.
        values[:] = (
            (field, _, __) for (field, _, __) in values
            if field.name not in read_only_field_names
        )


class SQLInsertCompiler(ReadOnlySQLCompilerMixin, BaseSQLInsertCompiler):

    def _exclude_readonly_fields(self, fields, read_only_field_names):
        for field in fields:
            if field.name not in read_only_field_names:
                yield field

    def remove_read_only_fields(self, read_only_field_names):
        """
        Remove the fields from the query which correspond to a
        read_only field
        """
        fields = self.query.fields

        try:
            fields[:] = self._exclude_readonly_fields(
                fields, read_only_field_names)
        except AttributeError:
            # When deserializing, we might get an attribute error because this
            # list shoud be copied first :

            # "AttributeError: The return type of 'local_concrete_fields'
            # should never be mutated. If you want to manipulate this list for
            # your own use, make a copy first."

            self.query.fields = list(self._exclude_readonly_fields(
                fields, read_only_field_names))
