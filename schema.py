from yams.buildobjs import (EntityType, RelationType, RelationDefinition,
                            SubjectRelation, ObjectRelation,
                            String, Date)

try:
    from cubes.person.schema import Person
    from cubes.task.schema import Task
    from cubes.event.schema import Event
except (ImportError, NameError):
    # old-style yams schema will raise NameError on EntityType, RelationType, etc.
    Person = import_erschema('Person')
    Task = import_erschema('Task')
    Event = import_erschema('Event')

Person.add_relation(String(maxsize=512), name='address')
Person.add_relation(Date(), name='birthday')

Person.add_relation(ObjectRelation('Comment', cardinality='1*', composite='object'), name='comments')
Person.add_relation(ObjectRelation('Tag'), name='tags')
Person.add_relation(SubjectRelation('File'), name='concerned_by')
Person.add_relation(SubjectRelation('State', cardinality='1*'), name='in_state')
Person.add_relation(ObjectRelation('TrInfo', cardinality='1*', composite='object'), name='wf_info_for')

Task.add_relation(ObjectRelation('Comment', cardinality='1*', composite='object'), name='comments')
Task.add_relation(SubjectRelation('Person'), name='todo_by')

Event.add_relation(ObjectRelation('Comment', cardinality='1*', composite='object'), name='comments')

class School(EntityType):
    """an (high) school"""
    name   = String(required=True, fulltextindexed=True, maxsize=128)
    address   = String(maxsize=512)
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


