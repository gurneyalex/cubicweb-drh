Person = import_erschema('Person')
Person.add_relation(Date(), name='birthday')
Person.add_relation(ObjectRelation('Comment', cardinality='1*', composite='object'), name='comments')
Person.add_relation(ObjectRelation('Tag'), name='tags')
Person.add_relation(SubjectRelation('File'), name='concerned_by')


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
    subject = ('Person', 'CWUser')
    object = 'Event'


class Application(WorkflowableEntityType):
    for_person = SubjectRelation('Person', cardinality='*1')
    date = Datetime(default='TODAY', required=True)




