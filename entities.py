from cubicweb.entities import AnyEntity, fetch_config
from cubes.person.entities import Person as BasePerson
from cubes.folder.entities import Folder as BaseFolder

from cubicweb.web import uicfg

uicfg.actionbox_appearsin_addmenu.tag_object_of(('*', 'todo_by', 'Person'), True)
uicfg.actionbox_appearsin_addmenu.tag_subject_of(('Person', 'concerned_by', '*'), True)
uicfg.actionbox_appearsin_addmenu.tag_subject_of(('School', 'filed_under', 'Folder'), False)

uicfg.autoform_is_inlined.tag_subject_of(('School', 'use_email', '*'), True)
uicfg.autoform_is_inlined.tag_subject_of(('School', 'phone', '*'), True)

class School(AnyEntity):
    id = 'School'
    fetch_attrs, fetch_order = fetch_config(['name'])
