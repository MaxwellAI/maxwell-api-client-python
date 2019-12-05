class Model:
    _exclude_fields = [
        "id",
    ]

    def __repr__(self):
        values = [
            "%s=%s" % (k, repr(v))
            for k, v in self.__dict__.items()
            if not k.startswith("_")
        ]
        return "%s(%s)" % (self.__class__.__name__, ", ".join(values))

    @property
    def _data(self):
        def _serialize(value):
            if isinstance(value, list):
                return [_serialize(item) for item in value]
            return value._data if hasattr(value, "_data") else value

        rv = {}
        for key, value in self.__dict__.items():
            if key.startswith("_") or (
                key in self._exclude_fields
                and key not in getattr(self, "_include_fields", [])
            ):
                continue
            rv[key] = _serialize(value)
        return rv
