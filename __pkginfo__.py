# pylint: disable-msg=W0622
"""cubicweb-drh packaging information"""

distname = "cubicweb-drh"

numversion = (0, 11, 1)
version = '.'.join(str(num) for num in numversion)

license = 'LCL'
copyright = '''Copyright (c) 2003-2008 LOGILAB S.A. (Paris, FRANCE).
http://www.logilab.fr/ -- mailto:contact@logilab.fr'''

author = "Logilab"
author_email = "contact@logilab.fr"

short_desc = "CubicWeb application tempalte for Human resource management"
long_desc = """CubicWeb is a entities / relations bases knowledge management system
developped at Logilab.
.
This package provides the "DRH" application built on top of CubicWeb.
It manages users, documents, tasks, comments, states
"""

from os import listdir
from os.path import join

web, ftp = '', ''

pyversions = ['2.4']

orig_dir = 'schemas'
TEMPLATES_DIR = join('share', 'cubicweb', 'cubes')
try:
    data_files = [
        [join(TEMPLATES_DIR, 'drh'),
         [fname for fname in listdir('.')
          if fname.endswith('.py') and fname != 'setup.py']],
        [join(TEMPLATES_DIR, 'drh', 'views'),
         [join('i18n', fname) for fname in listdir('views')]],
        [join(TEMPLATES_DIR, 'drh', 'i18n'),
         [join('i18n', fname) for fname in listdir('i18n')]],
        [join(TEMPLATES_DIR, 'drh', 'migration'),
         [join('migration', fname) for fname in listdir('migration')]],
        ]
except OSError:
    # we are in an installed directory
    pass

__use__ = ('file', 'email', 'person', 'addressbook',
           'folder', 'tag', 'comment',
           # could be moved out
           'basket', 'event', 'task')

cube_eid = 9653
