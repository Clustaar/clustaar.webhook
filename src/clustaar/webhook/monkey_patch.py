def patch_jmespath(key_not_found_sentinel):
    """Patch JMESPath in order to know when a key does not exists
    in JSON.
    Default behavior is to return None but this does not mean
    that key was not found in JSON

    Args:
        key_not_found_sentinel (object): sentinel returned when key is not found
    """
    from jmespath.visitor import TreeInterpreter

    def visit_field(self, node, value):
        # https://github.com/jmespath/jmespath.py/blob/develop/jmespath/visitor.py#L134
        try:
            return value[node["value"]]
        except (AttributeError, TypeError):
            return key_not_found_sentinel

    TreeInterpreter.visit_field = visit_field
