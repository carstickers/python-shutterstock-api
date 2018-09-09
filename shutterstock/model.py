
class Field:
    def __init__(self, default=None, help_text=None):
        self.name = None
        self.help_text = help_text
        self.default = default

    def __get__(self, instance, cls):
        return instance.__dict__[self.name] or self.default

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        raise AttributeError("Can't delete model fields.")


class ModelMeta(type):
    def __new__(mcs, clsname, bases, clsdict):
        fields = [key for key, val in clsdict.items()
                  if isinstance(val, Field)]
        for name in fields:
            clsdict[name].name = name

        return super().__new__(mcs, clsname, bases, clsdict)


class Model(metaclass=ModelMeta):
    def __init__(self, *args, **kwargs):
        pass
