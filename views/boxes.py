# -*- coding: utf-8 -*-

from cubicweb.web.box import BoxTemplate
from cubicweb.web.htmlwidgets import BoxWidget, BoxLink

class StartupViewsBox(BoxTemplate):
    """display a box containing links to all startup views"""
    id = 'drh_workflow_box'
    visible = True # disabled by default
    title = _('State')
    order = 70

    def call(self, **kwargs):
        box = BoxWidget(self.req._(self.title), self.id)
        rset = self.req.execute('Any S,SN,count(P) GROUPBY S,SN '
                                'WHERE P is Person, P in_state S, S name SN')
        rows = list(rset)
        keyorder = [u'jugement candidature', u'envoi réponse négative', u'envoi proposition entretien',
                    u'négociation horaire entretien', u'entretien convenu',  u'jugement entretien',
                    u'envoi réponse positive',]
        
        for key in keyorder:
            for eid, state, count in rows:
                if state != key: continue
                url = self.build_url(rql='Any P WHERE P in_state S, S eid %s' % eid,
                                     vtitle=state)
                label = u'%s: %s' % (state, count)
                box.append(BoxLink(url, label))
        
        if not box.is_empty():
            box.render(self.w)
