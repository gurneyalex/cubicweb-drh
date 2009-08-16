from cubicweb.interfaces import ITree
from cubicweb.common.mixins import TreeMixIn

from cubicweb.entities import AnyEntity, fetch_config

from cubes.email.entities import EmailThread as EmailEmailThread

class School(AnyEntity):
    id = 'School'
    fetch_attrs, fetch_order = fetch_config(['name'])


class EmailThread(TreeMixIn, EmailEmailThread):

    __implements__ = EmailEmailThread.__implements__ + (ITree,)

    tree_attribute = 'topic'

    def parent(self):
        """for breadcrumbs"""
        return self.topic and self.topic[0] or None


class Application(TreeMixIn, AnyEntity):

    __implements__ = AnyEntity.__implements__ + (ITree,)

    tree_attribute = 'for_person'

    def parent(self):
        """for breadcrumbs"""
        return self.for_person and self.for_person[0] or None

