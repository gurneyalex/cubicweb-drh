from cubes.person.views import PersonPrimaryView as BasePersonPrimaryView

class PersonPrimaryView(BasePersonPrimaryView):
    
    def get_side_boxes_defs(self, entity):
        boxes = []
        limit = self.req.property_value('navigation.related-limit') + 1
        rql = 'Any E ORDERBY D DESC WHERE P use_email EA, E sender EA, E date D, P eid %(x)s'
        rset = self.req.execute(rql, {'x': entity.eid})
        boxes.append( (_('recent email'), rset) )
        return boxes
