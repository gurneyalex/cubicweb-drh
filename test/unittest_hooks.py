# -*- coding: utf-8 -*-

# copyright 2011-2015 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

from cubicweb import Binary
from cubicweb.devtools.testlib import MAILBOX, CubicWebTC


class HooksTC(CubicWebTC):
    
    def test_no_auto_person_for_cwuser(self):
        with self.admin_access.client_cnx() as cnx:
            self.assertFalse(cnx.find('Person'))
            user = self.create_user(cnx, 'Babar', ('users', ),
                                    email=u'babar@ratax.es')
            cnx.commit()
        with self.admin_access.client_cnx() as cnx:
            self.assertFalse(cnx.find('Person'))

    def test_auto_person_alias(self):
        with self.admin_access.client_cnx() as cnx:
            self.assertFalse(cnx.find('Person'))
            cnx.create_entity('EmailAddress',
                              address=u'first.last@some.where',
                              alias=u'First Last')
            cnx.commit()
        with self.admin_access.client_cnx() as cnx:
            self.assertTrue(cnx.find('EmailAddress', address=u'first.last@some.where'))
            p = cnx.find('Person', firstname=u'First').one()
            self.assertEqual('First', p.firstname)
            self.assertEqual('Last',  p.surname)
            self.assertTrue(cnx.find('Application', for_person=p))

    def test_auto_person_alias2(self):
        with self.admin_access.client_cnx() as cnx:
            self.assertFalse(cnx.find('Person'))
            cnx.create_entity('EmailAddress',
                              address=u'first.last@some.where',
                              alias=u'First Mid Last')
            cnx.commit()
        with self.admin_access.client_cnx() as cnx:
            self.assertTrue(cnx.find('EmailAddress', address=u'first.last@some.where'))
            p = cnx.find('Person', firstname=u'First').one()
            self.assertEqual('First', p.firstname)
            self.assertEqual('Mid Last',  p.surname)
            self.assertTrue(cnx.find('Application', for_person=p))

    def test_auto_person_alias_3(self):
        with self.admin_access.client_cnx() as cnx:
            self.assertFalse(cnx.find('Person'))
            cnx.create_entity('EmailAddress',
                              address=u'first.last@some.where',
                              alias=u'Last')
            cnx.commit()
        with self.admin_access.client_cnx() as cnx:
            self.assertTrue(cnx.find('EmailAddress', address=u'first.last@some.where'))
            p = cnx.find('Person', surname=u'Last').one()
            self.assertEqual('', p.firstname)
            self.assertEqual('Last',  p.surname)
            self.assertTrue(cnx.find('Application', for_person=p))

            
    def test_auto_person_no_alias(self):
        with self.admin_access.client_cnx() as cnx:
            self.assertFalse(cnx.find('Person'))
            cnx.create_entity('EmailAddress',
                              address=u'first.last@some.where',)
            cnx.commit()
        with self.admin_access.client_cnx() as cnx:
            self.assertTrue(cnx.find('EmailAddress', address=u'first.last@some.where'))
            p = cnx.find('Person', firstname=u'First').one()
            self.assertEqual('First', p.firstname)
            self.assertEqual('Last',  p.surname)
            self.assertTrue(cnx.find('Application', for_person=p))
            
    def test_auto_person_no_alias_2(self):
        with self.admin_access.client_cnx() as cnx:
            self.assertFalse(cnx.find('Person'))
            cnx.create_entity('EmailAddress',
                              address=u'first.mid.last@some.where',)
            cnx.commit()
        with self.admin_access.client_cnx() as cnx:
            self.assertTrue(cnx.find('EmailAddress', address=u'first.mid.last@some.where'))
            p = cnx.find('Person', firstname=u'First').one()
            self.assertEqual('First', p.firstname)
            self.assertEqual('Mid Last',  p.surname)
            self.assertTrue(cnx.find('Application', for_person=p))
           
    def test_forge_concerned_by_links(self):
        with self.admin_access.client_cnx() as cnx:
            ea = cnx.create_entity('EmailAddress',
                                   address=u'first.last@some.where',
                                   alias=u'First Last')
            cnx.commit()
            p = cnx.find('Person', firstname=u'First').one()
            
            self.assertFalse(p.concerned_by)

            e = cnx.create_entity('Email', subject=u'none', messageid=u'toto')
            f = cnx.create_entity('File', data=Binary('Some content'),
                                  data_name=u'some part',
                                  data_format=u'text/plain',
                                  data_encoding=u'ascii')
            e.cw_set(attachment=f, sender=ea)
            cnx.commit()
            
        # now check the file has been linked to the person by hooks
        with self.admin_access.client_cnx() as cnx:
            p = cnx.find('Person', firstname=u'First').one()
            self.assertTrue(p.concerned_by)
            self.assertEqual('some part', p.concerned_by[0].data_name)

            
            

if __name__ == '__main__':
    import unittest
    unittest.main()
