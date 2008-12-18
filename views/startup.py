from logilab.mtconverter import html_escape
from cubicweb.web.views import dynimages, startup

class IndexView(startup.ManageView):
    id = 'index'
    title = _('Index')
    
    def call(self):
        _ = self.req._
        user = self.req.user
        self.w(u'<h1>%s</h1>' % self.req.property_value('ui.site-title'))
        
        # email addresses not linked
        rql = 'Any X WHERE NOT P use_email X'
        title = u'email addresses not linked to a person'
        rset = self.req.execute(rql)
        if rset and len(rset):
            self.w(u'<p><a href="%s">%s %s</a></p>'
                   % (html_escape(self.build_url(rql=rql, vtitle=title)),
                      len(rset), title))

        # candidatures en attente
        rset = self.req.execute('Any CD,P,CONCAT_STRINGS(TN),E,B '
                                'GROUPBY P,E,B,CD ORDERBY CD '
                                'WHERE P in_state X, P is Person, '
                                'X name "jugement candidature", '
                                'T? tags P, T name TN, P has_studied_in E?, '
                                'P birthday B?, P creation_date CD')
        if rset and len(rset):
            self.w(u'<h2>%s</h2>' % _('Juger candidatures'))
            self.wview('table',rset,'null')
        else:
            self.w(u'<p>%s</p>' % _('aucune candidature en attente'))




