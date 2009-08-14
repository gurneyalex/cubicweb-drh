# application are taggable
add_relation_definition('Tag','tags','Application')
# move tags from person to applications
rql('SET T tags A WHERE T tags P, P is Person, A for_person P')
rql('DELETE T tags P WHERE P is Person')
