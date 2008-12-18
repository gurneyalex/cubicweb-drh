from cubicweb.entities import AnyEntity, fetch_config
from eperson.entities import Person as BasePerson
from eclassfolders.entities import Folder as BaseFolder

class Person(BasePerson):
    id = 'Person'
    __rtags__ = {'concerned_by' : 'create',
                 'todo_by'      : 'create',
                }

class Folder(BaseFolder):
    id = 'Folder'
    __rtags__ = {('filed_under', 'School', 'object') : 'link',
                }

class School(AnyEntity):
    id = 'School'
    __rtags__ = {'use_email' : 'inlineview',
                 'phone'     : 'inlineview',
                }
    fetch_attrs, fetch_order = fetch_config(['name'])
