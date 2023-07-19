import re

SipUriRegex = re.compile("(sip|sips):([^:;>\@]*)@?([^:;>]*):?([^:;>]*)")


def ParseSipUri(sip_uri_str):
    m = SipUriRegex.search(sip_uri_str)
    if not m:
        assert 0
        return None

    scheme = m.group(1)
    user = m.group(2)
    host = m.group(3)
    port = m.group(4)
    if host == "":
        host = user
        user = ""

    return SipUri(scheme.lower(), user, host.lower(), port)


class SipUri:
    def __init__(self, scheme, user, host, port):
        self.scheme = scheme
        self.user = user
        self.host = host
        self.port = port

    def __cmp__(self, sip_uri):
        if (
            self.scheme == sip_uri.scheme
            and self.user == sip_uri.user
            and self.host == sip_uri.host
        ):
            # don't check port, at least for now
            return 0
        return -1

    def __str__(self):
        s = self.scheme + ":"
        if self.user:
            s += self.user + "@"
        s += self.host
        if self.port:
            s += ":" + self.port
        return s
