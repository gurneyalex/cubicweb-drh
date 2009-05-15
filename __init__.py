from cubicweb.web import uicfg

uicfg.actionbox_appearsin_addmenu.tag_object_of(('Person', 'concerned_by', '*'), True)
uicfg.actionbox_appearsin_addmenu.tag_object_of(('Person', 'todo_by', '*'), True)
