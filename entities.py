from cubicweb.entities import AnyEntity, fetch_config

class School(AnyEntity):
    id = 'School'
    fetch_attrs, fetch_order = fetch_config(['name'])
