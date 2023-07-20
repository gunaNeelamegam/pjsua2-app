from utils.config import load_to_instance
from inspect import Parameter, Signature


class Descriptor:
    def __init__(self, *name):
        self.name = name

    def __get__(self, instance, cls):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value
        return

    def __delete__(self, instance):
        del instance.__dict__[self.name]
        return


import re


class Sized(Descriptor):
    def __init__(self, *args, maxlen, **kwargs):
        self.maxlen = maxlen
        super().__init__(*args, **kwargs)

    def __set__(self, instance, value):
        if len(value) > self.maxlen:
            raise ValueError("Length is Higher than ", self.maxlen)
        return super().__set__(instance, value)


class Regex(Descriptor):
    def __init__(self, *args, pat, **kwargs):
        self.pat = re.compile(pat)
        super().__init__(*args, **kwargs)

    def __set__(self, instance, value):
        if not self.pat.match(value):
            raise ValueError("Value Doest Match With %s Pattern .%(self.pat)")
        return super().__set__(instance, value)


class Typed(Descriptor):
    ty = object

    def __set__(self, instance, value):
        if not isinstance(value, self.ty):
            raise TypeError("Expected ", self.ty, "Got : ", type(value))
        return super().__set__(instance, value)


class Integer(Typed):
    ty = int


class String(Typed):
    ty = str


class Float(Typed):
    ty = float


class Positive(Descriptor):
    def __set__(self, instance, value):
        if not (value > 0):
            raise ValueError("Got Negative Integer ")
        return super().__set__(instance, value)


class PositiveInteger(Integer, Positive):
    pass


class PositiveFloat(Float, Positive):
    pass


class SizedString(String, Sized):
    pass


class SizedRegexString(SizedString, Regex):
    pass


def make_signature(args):
    return Signature([Parameter(i, Parameter.POSITIONAL_OR_KEYWORD) for i in args])
