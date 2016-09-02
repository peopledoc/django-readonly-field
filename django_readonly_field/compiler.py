from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.compiler import SQLInsertCompiler as BaseSQLInsertCompiler
from django.db.models.sql.compiler import SQLDeleteCompiler
from django.db.models.sql.compiler import SQLUpdateCompiler as BaseSQLUpdateCompiler
from django.db.models.sql.compiler import SQLAggregateCompiler


class ReadOnlySQLCompilerMixin(object):
    def as_sql(self):
        try:
            read_only_meta = getattr(self.query.model, "ReadOnlyMeta")
        except AttributeError:
            pass
        else:
            read_only_field_names = set(getattr(
                read_only_meta, "read_only", set()))
            self.remove_read_only_fields(read_only_field_names)
        return super(ReadOnlySQLCompilerMixin, self).as_sql()


class SQLUpdateCompiler(ReadOnlySQLCompilerMixin, BaseSQLUpdateCompiler):

    def remove_read_only_fields(self, read_only_field_names):
        for i, (field, __, __) in list(enumerate(self.query.values))[::-1]:
            if field.name in read_only_field_names:
                del self.query.values[i]


class SQLInsertCompiler(ReadOnlySQLCompilerMixin, BaseSQLInsertCompiler):

    def remove_read_only_fields(self, read_only_field_names):
        for field in self.query.fields:
            if field.name in read_only_field_names:
                self.query.fields.remove(field)


