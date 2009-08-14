from logilab.mtconverter import html_escape

from cubicweb.web.views import startup

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
        if rset:
            self.w(u'<p><a href="%s">%s %s</a></p>'
                   % (html_escape(self.build_url(rql=rql, vtitle=title)),
                      len(rset), title))
        # candidatures en attente
        rset = self.req.execute('Any A,P,group_concat(TN),E,B '
                                'GROUPBY A,P,E,B,CD ORDERBY CD '
                                'WHERE A is Application, A in_state X, '
                                'X name "received", '
                                'A for_person P, P has_studied_in E?, '
                                'P birthday B?, T? tags A, T name TN, '
                                'A creation_date CD')
        if rset:
            self.w(u'<h2>%s</h2>' % _('Juger candidatures'))
            self.wview('table',rset,'null')
        else:
            self.w(u'<p>%s</p>' % _('aucune candidature en attente'))




def registration_callback(vreg):
    vreg.register(IndexView, clear=True)
