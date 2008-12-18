from cubes.person.views import PersonPrimaryView as BasePersonPrimaryView

class PersonPrimaryView(BasePersonPrimaryView):
    
    def get_side_boxes_defs(self, entity):
        rsets = []
        limit = self.req.property_value('navigation.related-limit') + 1
        rql = 'Any E ORDERBY D DESC WHERE P use_email EA, E sender EA, E date D, P eid %s'
        rset = self.req.execute(rql % entity.eid)
        rsets.append( (_('recent email'), rset) )
        return rsets
