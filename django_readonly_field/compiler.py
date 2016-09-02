from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.compiler import SQLInsertCompiler as BaseSQLInsertCompiler
from django.db.models.sql.compiler import SQLDeleteCompiler
from django.db.models.sql.compiler import SQLUpdateCompiler as BaseSQLUpdateCompiler
from django.db.models.sql.compiler import SQLAggregateCompiler
from django.utils.functional import cached_property


class ReadOnlySQLCompilerMixin(object):
    
    @cached_property
    def read_only_field_names(self):
        try:
            read_only_meta = getattr(self.query.model, "ReadOnlyMeta")
        except AttributeError:
            return ()
        else:
            return frozenset(getattr(read_only_meta, "read_only", ()))

    def as_sql(self):
        read_only_field_names = self.read_only_field_names
        if read_only_field_names:
            self.remove_read_only_fields(read_only_field_names)
        return super(ReadOnlySQLCompilerMixin, self).as_sql()


class SQLUpdateCompiler(ReadOnlySQLCompilerMixin, BaseSQLUpdateCompiler):

    def remove_read_only_fields(self, read_only_field_names):
        """
        Remove the values from the query which correspond to a
        readonly field
        """
        values = self.query.values
        # is there some values to remove ?
        has_readonly_value = any(
            field.name in read_only_field_names
            for (field, _, __) in values
        )
        if has_readonly_value:
            values[:] = (
                (field, _, __) for (field, _, __) in values
                if field.name not in read_only_field_names
            )


class SQLInsertCompiler(ReadOnlySQLCompilerMixin, BaseSQLInsertCompiler):

    def remove_read_only_fields(self, read_only_field_names):
        for field in self.query.fields:
            if field.name in read_only_field_names:
                self.query.fields.remove(field)


