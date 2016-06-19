""" Base test case for command line manage.py csvimport """
import os

from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist

from csvimport.management.commands.importcsv import Command as ImportCommand
from csvimport.management.commands.inspectcsv import Command as InspectCommand
from csvimport.tests.models import Item

DEFAULT_ERRS = ["Columns = CODE_SHARE, CODE_ORG, ORGANISATION, DESCRIPTION, UOM, QUANTITY, STATUS",
                'Using mapping from first row of CSV file', 
                'Imported 4 rows to Item',
                'Imported 6 rows to Item',
                'Imported 7 rows to Item',
                'Imported 8 rows to Item',
                'Outputting setup message',
                'Using manually entered (or default) mapping list'
                ]

class DummyFileObj():
    """ Use to replace html upload / or command arg
        with test fixtures files
    """
    path = ''

    def set_path(self, filename):
        self.path = os.path.join(os.path.dirname(__file__),
                                 'fixtures',
                                 filename)

class CommandTestCase(TestCase):
    """ Run test of use of optional command line args - mappings, default and charset """


    def inspectcsv(self, csvfile, model='', charset='', defaults=''):
        """ Run inspectcsv command to parse file """
        cmd = InspectCommand()
        uploaded = DummyFileObj()
        uploaded.set_path(csvfile)
        cmd.csvfile = cmd.open_csvfile(uploaded.path)
        cmd.handle_label(csvfile, **{'model':model, 'charset':charset, 'defaults':defaults})
        return cmd.makemodel

    def command(self, 
                csvfile=None, 
                mappings='',
                modelname='csvimport.Item',
                charset='',
                expected_errs=[],
                defaults='country=KE(Country|code)',
                uploaded=None,
                nameindexes=False,
                deduplicate=True
                ):
        """ Run core csvimport command to parse file """
        cmd = ImportCommand()
        uploaded = DummyFileObj()
        uploaded.set_path(csvfile)
        cmd.setup(mappings=mappings,
                  modelname=modelname,
                  charset=charset,
                  defaults=defaults,
                  uploaded=uploaded,
                  nameindexes=nameindexes,
                  deduplicate=deduplicate
                  )

        # Report back any unnexpected parse errors
        # and confirm those that are expected.
        # Fail test if they are not matching
        errors = cmd.run(logid='commandtest')
        expected = [err for err in DEFAULT_ERRS]
        if expected_errs:
            expected.extend(expected_errs)
        for err in expected:
            try:
                errors.remove(err)
            except:
                pass
        if errors:
            for err in errors:
                print (err)
        self.assertEqual(errors, [])

    def get_item(self, code_share='sheeting'):
        """ Get item for confirming import is OK """
        try:
            item = Item.objects.get(code_share__exact=code_share)
        except ObjectDoesNotExist:
            item = None
            self.assertTrue(item, 'Failed to get row from imported test.csv Items')
        return item
