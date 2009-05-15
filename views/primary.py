from cubicweb.selectors import implements, rql_condition
from cubicweb.web.component import RelatedObjectsVComponent
from cubicweb.web import uicfg

uicfg.autoform_is_inlined.tag_subject_of(('School', 'use_email', '*'), True)
uicfg.autoform_is_inlined.tag_subject_of(('School', 'phone', '*'), True)

class SentMailVComponent(RelatedObjectsVComponent):
    """email sent by this person"""
    id = 'sentmail'
    __select__ = RelatedObjectsVComponent.__select__ & implements('Person') & rql_condition('X use_email EA, E sender EA')
    rtype = 'use_email'
    role = 'subject'
    order = 40
    # reuse generated message id
    title = _('contentnavigation_sentmail')

    def rql(self):
        """override this method if you want to use a custom rql query"""
        return 'Any E ORDERBY D DESC WHERE P use_email EA, E sender EA, E date D, P eid %(x)s'

