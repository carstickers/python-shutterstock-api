

class EndPointParam:
    NO_VALUE = ()  # Empty tuple for testing against

    def __init__(self, vtype=str, default=None, help_text=None, required=False):
        self.name = 'param'
        self.data_type = vtype
        self.default = default
        self.help_text = help_text
        self.required = required

    def clean(self, value):
        if value is EndPointParam.NO_VALUE or (value is None and self.required):
            value = self.default

        return value


class ChoicesParam(EndPointParam):
    def __init__(self, choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = choices


class EndpointMeta(type):
    def __new__(mcs, clsname, bases, clsdict):
        params = []
        for name, val in clsdict.items():
            if isinstance(val, EndPointParam):
                clsdict[name].name = name
                params.append(val)

        clsdict['params'] = tuple(params)
        clsobj = super().__new__(mcs, clsname, bases, clsdict)
        return clsobj


class EndPoint(metaclass=EndpointMeta):
    params = ()

    def __init__(self, uri):
        self.uri = uri

    def prepare(self, **kwargs):
        uri = self.uri.format(**kwargs)
        params = {}

        for param in self.params:
            params[param.name] = param.clean(kwargs.get(param.name, EndPointParam.NO_VALUE))

        return uri, params

    def explain(self):
        return "URI: {uri}\n\nDescription: {doc}\n\nParams:\n{params}".format(
            uri=self.uri,
            doc=self.__doc__,
            params="\n".join(
                [
                    '{name}: {help_text}'.format(
                        name=param.name,
                        help_text=param.help_text
                    )
                    for param in self.params
                ]
            )
        )
