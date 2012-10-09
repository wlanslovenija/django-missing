from urllib2 import *

class LessStrictHTTPErrorProcessor(HTTPErrorProcessor):
    """
    A urllib2 HTTP error processor which does not raise an error
    on HTTP 201 (created) or 202 (accepted) response.
    Used by HTTP push server when replying to a publisher.
    """

    def http_error_201(self, request, fp, code, msg, hdrs):
        """
        Does not raise an error on HTTP 201 (created) response.
        """
        return fp

    def http_error_202(self, request, fp, code, msg, hdrs):
        """
        Does not raise an error on HTTP 202 (accepted) response.
        """
        return fp

opener = build_opener(LessStrictHTTPErrorProcessor)
install_opener(opener)
