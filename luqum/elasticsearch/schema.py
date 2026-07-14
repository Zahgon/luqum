

class SchemaAnalyzer:

    def __init__(self, schema):
        self.settings = schema.get("settings", {})
        mappings = schema.get("mappings", {})
        if mappings.get("properties"):
            self.mappings = {"_doc": mappings}
        else:
            self.mappings = mappings

    def _dot_name(self, fname, parents):
        pass

    def default_field(self):
        pass

    def _walk_properties(self, properties, parents=None, subfields=False):
        pass

    def iter_fields(self, subfields=False):
        pass

    def not_analyzed_fields(self):
        pass

    def nested_fields(self):
        pass

    def object_fields(self):
        pass

    def sub_fields(self):
        pass

    def query_builder_options(self):
        pass
