"""drh web ui"""

from cubicweb.web import uicfg

uicfg.actionbox_appearsin_addmenu.tag_subject_of(('Person', 'concerned_by', '*'), True)
uicfg.actionbox_appearsin_addmenu.tag_object_of(('*', 'todo_by', 'Person'), True)
uicfg.actionbox_appearsin_addmenu.tag_subject_of(('School', 'filed_under', 'Folder'), False)
uicfg.autoform_is_inlined.tag_subject_of(('School', 'use_email', '*'), True)
uicfg.autoform_is_inlined.tag_subject_of(('School', 'phone', '*'), True)
uicfg.primaryview_section.tag_subject_of(('Person', 'concerned_by', '*'), 'hidden')
uicfg.autoform_section.tag_subject_of(('Application', 'for_person', '*'), 'primary')
