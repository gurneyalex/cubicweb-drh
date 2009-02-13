
Person = import_erschema('Person')
Person.add_relation(String(maxsize=512), name='address')
Person.add_relation(Date(), name='birthday')

Person.add_relation(ObjectRelation('Comment', cardinality='1*', composite='object'), name='comments')
Person.add_relation(ObjectRelation('Tag'), name='tags')
Person.add_relation(SubjectRelation('File'), name='concerned_by')
Person.add_relation(SubjectRelation('State', cardinality='1*'), name='in_state')
Person.add_relation(ObjectRelation('TrInfo', cardinality='1*', composite='object'), name='wf_info_for')

Task = import_erschema('Task')
Task.add_relation(ObjectRelation('Comment', cardinality='1*', composite='object'), name='comments')
Task.add_relation(SubjectRelation('Person'), name='todo_by')

Event = import_erschema('Event')
Event.add_relation(ObjectRelation('Comment', cardinality='1*', composite='object'), name='comments')

class School(EntityType):
    """an (high) school"""
    name   = String(required=True, fulltextindexed=True,
                    constraints=[SizeConstraint(128)])
    address   = String(constraints=[SizeConstraint(512)])
    description = String(fulltextindexed=True)

    phone         = SubjectRelation('PhoneNumber', composite='subject')
    use_email     = SubjectRelation('EmailAddress', composite='subject')

    has_studied_in = ObjectRelation('Person')


class has_studied_in(RelationType):
    """used to indicate an estabishment where a person has been studying"""
    # XXX promotion?


class interested_in(RelationDefinition):
    subject = ('Person', 'EUser')
    object = 'Event'


