"""Source type manager"""
from enum import Enum
from logging import getLogger

from passbook.oauth_client.views.core import OAuthCallback, OAuthRedirect

LOGGER = getLogger(__name__)

class RequestKind(Enum):
    """Enum of OAuth Request types"""

    callback = 'callback'
    redirect = 'redirect'


class SourceTypeManager:
    """Manager to hold all Source types."""

    __source_types = {}
    __names = []

    def source(self, kind, name):
        """Class decorator to register classes inline."""
        def inner_wrapper(cls):
            if kind not in self.__source_types:
                self.__source_types[kind] = {}
            self.__source_types[kind][name.lower()] = cls
            self.__names.append(name)
            LOGGER.debug("Registered source '%s' for '%s'", cls.__name__, kind)
            return cls
        return inner_wrapper

    def get_name_tuple(self):
        """Get list of tuples of all registered names"""
        return [(x.lower(), x) for x in set(self.__names)]

    def find(self, source, kind):
        """Find fitting Source Type"""
        if kind in self.__source_types:
            if source.provider_type in self.__source_types[kind]:
                return self.__source_types[kind][source.provider_type]
            # Return defaults
            if kind == RequestKind.callback:
                return OAuthCallback
            if kind == RequestKind.redirect:
                return OAuthRedirect
        raise KeyError


MANAGER = SourceTypeManager()
