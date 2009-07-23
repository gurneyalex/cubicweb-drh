# -*- coding: utf-8 -*-

from cubicweb.web.box import BoxTemplate
from cubicweb.web.htmlwidgets import BoxWidget, BoxLink

from logilab.mtconverter import html_escape
from cubicweb.web.box import EntityBoxTemplate

from cubicweb.selectors import implements, rql_condition
from cubicweb.web.htmlwidgets import SideBoxWidget, BoxLink

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
        keyorder = [u'application', u'send interview proposition', u'interview time negociation',
                    u'interview planned', u'interview judgment', u'send positive answer',
                    u'send negative answer', u'refused', u'recruited', u'canceled']

        for key in keyorder:
            for eid, state, count in rows:
                if state != key: continue
                rql_syn = 'Any CD,P,group_concat(TN),E,B '\
                          'GROUPBY P,E,B,CD ORDERBY CD '\
                          'WHERE P in_state X, P is Person, '\
                          'X eid %s, '\
                          'T? tags P, T name TN, P has_studied_in E?, '\
                          'P birthday B?, P creation_date CD'
                url = self.build_url(rql=rql_syn % eid,
                                     vtitle=self.req._(state))
                label = u'%s: %s' % (state, count)
                box.append(BoxLink(url, label))
        
        if not box.is_empty():
            box.render(self.w)


class AttachmentsDownloadBox(EntityBoxTemplate):
    """
    A box containing all downloadable attachments concerned by Person.
    """
    id = 'concerned_by_box'
    __select__ = EntityBoxTemplate.__select__ & implements('Person')
    rtype = 'concerned_by'
    target = 'subject'
    order = 0
    
    def cell_call(self, row, col, **kwargs):
        entity = self.entity(row, col)
        req = self.req
        self.w(u'<div class="sideBox">')
        title = req._('concerned_by')
        self.w(u'<div class="sideBoxTitle downloadBoxTitle"><span>%s</span></div>'
            % html_escape(title))
        self.w(u'<div class="sideBox downloadBox"><div class="sideBoxBody">')
        for attachment in entity.concerned_by:
            self.w(u'<div><a href="%s"><img src="%s" alt="%s"/> %s</a>'
                   % (html_escape(attachment.download_url()),
                      req.external_resource('DOWNLOAD_ICON'),
                      _('download icon'), html_escape(attachment.dc_title())))
            self.w(u'</div>')
        self.w(u'</div>\n</div>\n</div>\n')
        

class PeopleBox(EntityBoxTemplate):
    id = '123people_box'
    __select__ = EntityBoxTemplate.__select__ & implements('Person')
    order = 25

    def cell_call(self, row, col, **kwargs):
        entity = self.entity(row, col)
        firstname = entity.firstname
        surname = entity.surname
        box = SideBoxWidget(self.req._('The url\'s Person on 123people '), 
                            'person_on_123people')
        box.append(BoxLink('http://www.123people.com/s/%s+%s/world' % (firstname, surname), '%s %s' % (firstname, surname)))
        self.w(box.render())
