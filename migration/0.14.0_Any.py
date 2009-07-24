#delete after the person's cube migration
add_relation_definition('Person', 'postal_address', 'PostalAddress')

##migrate address
add_entity_type('PostalAddress')
rset = rql('Any X , Y WHERE X is Person, NOT X address NULL, X address Y ')

for person_eid, address_value in rset:
    ## move address to description if it's longer than 256 character
    if len(address_value) < 256:
        rql("INSERT PostalAddress P: P street %(S)s , P city %(C)s, P postalcode %(PC)s, \
        D postal_address P WHERE D is Person, D eid %(eid)s", \
            {'S':address_value, 'C':u'???', 'PC':u'???', 'eid': person_eid},\
            ask_confirm=False)
    else:
        desc_base = rql("Any D WHERE X is Person, X description D, X eid %(eid)s", {'eid': person_eid}).rows[0][0]
        if desc_base and desc_base[0][0]:
            desc_new = desc_base[0][0] + ' ' + address_value
        else:
            desc_new = address_value 
        rql("SET X description %(D)s WHERE X is Person, X eid %(eid)s", {'D': desc_new, 'eid':person_eid})

drop_attribute('Person', 'address')


##state label was changed
rset = rql('Any P WHERE P is Person')

state_changed ={u'jugement candidature': u'application',  u'envoi réponse négative': u'send negative answer',
                u'envoi proposition entretien': u'send interview proposition',
                u'négociation horaire entretien': u'interview time negociation',
                u'jugement entretien': u'interview judgment',  u'entretien convenu': u'send interview proposition',
                u'envoi réponse positive': u'send positive answer',
                u'refusé': u'refused', u'recruté': u'recruited', u'annulé': u'canceled'}

for old_state, new_state in state_changed.items():
    rql(u'SET S name %(NS)s WHERE S state_of P , P name "Person", S name %(OS)s',
        {'NS': new_state, 'OS': old_state})

##migrate state form person to application
add_entity_type('Application')

for person_eid in rset:
    person_state = rql(u'Any S, P Where P is Person, P eid %(eid)s , P in_state S',  {'eid': person_eid[0]})[0][0]
    app_eid = rql(u'INSERT Application X : X for_person P WHERE P eid %(eid)s', {'eid': person_eid[0]})[0][0]
    rql(u'SET A in_state S WHERE A is Application, A eid %(AP)s, S eid %(s)s',
        {'eid': person_eid[0], 's': person_state, 'AP': app_eid})

##add state and transition on Apllication and remove it from Person
appl  = add_state(_('application'),                'Application', initial=True)
prop  = add_state(_('send interview proposition'), 'Application')
itne  = add_state(_('interview time negociation'), 'Application')
itpl  = add_state(_('interview planned'),          'Application')
itju  = add_state(_('interview judgment'),         'Application')
spoa  = add_state(_('send positive answer'),       'Application')  
snea  = add_state(_('send negative answer'),       'Application')
refu  = add_state(_('refused'),                    'Application')
recr  = add_state(_('recruited'),                  'Application')
canc  = add_state(_('canceled'),                   'Application')

add_transition(_('cancel application'), 'Application', (appl, prop, itne, itpl, itju, spoa, snea, refu, recr),  canc)
add_transition(_('discard application'), 'Application', (appl, itju),  snea)
add_transition(_('negative answer sent'), 'Application', (snea,),  refu)
add_transition(_('propose interview'), 'Application', (appl,),  prop)
add_transition(_('schedule interview'), 'Application', (appl,),  itne)
add_transition(_('interview scheduled'), 'Application', (itne,),  itpl)
add_transition(_('interview done'), 'Application', (itpl,),  itju)
add_transition(_('propose new interview'), 'Application', (itju,),  prop)
add_transition(_('accept application'), 'Application', (itju, ),  spoa)
add_transition(_('propositiion accepted'), 'Application', (spoa,),  recr)

sync_schema_props_perms('Application')

#delete state for Person
rql('DELETE State S WHERE S state_of X, X name "Person"')
drop_relation_definition('Person', 'in_state', 'State')
drop_relation_definition('Person', 'wf_info_for', 'TrInfo')
checkpoint()

