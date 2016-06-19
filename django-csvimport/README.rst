Django CSV Import
=================

Ed Crewe - October 2014

Overview
--------

django-csvimport is a generic importer tool to allow the upload of CSV files for
populating data. The egg installs an admin cvsimport model that has a file upload field.
Add a new csvimport and upload a comma separated values file or MS Excel file.

The upload triggers the import mechanism which matches the header line of the files 
field names to the fields in the selected model. Importing any rows that include all required fields.
Optionally required fields can be specified as part of the upload.
By default duplicate value rows are not inserted.

The import can also be run as a custom command, ie manage.py importcsv filename
for possible use via cronjob etc.

For CSV files import where their schema is unknown, and there is no existing model to import to, there
is another command, inspectcsv, to generate the model code from the CSV file, guessing data types from the data
using https://messytables.readthedocs.org - to use this command please pip install messytables.

The core import code was based on http://djangosnippets.org/snippets/633/ by Jonathan Holst.
It adds character encoding handling, model field and column autodetection, admin interface,
custom command etc.

Version 2 - Sept 2014
---------------------

#. New management command csvinspect to generate models from CSV files
#. General code refactor 
#. Management command renamed from csvimport to importcsv
#. More features to cope with bad encoding and date types

Version Compatibility
---------------------

Version 2.3 tested with Django 1.7, Python 2.7 and Python 3.4

Please use version 2.1, eg. pip install django-csvimport==2.1 
for Django versions prior to 1.7

This Django 1.7 requirement is because django-csvimport uses the newly added AppConfig for versions > 2.1
(NB: To fix this issue you could install django-appconf to django 1.6 or earlier 
and tweak csvimport to use it in csvimport.app)

For really old Django versions < 1.4 you may have to dial back the versions until it works!

Note that only versions > 2.2 are compatible with Python 3.4


Installation instructions
-------------------------

Add the following to the INSTALLED_APPS in the settings.py of your project:

>>>  pip install django-csvimport
...
...  INSTALLED_APPS = (
...  ...
...  'csvimport.app.CSVImportConf',  # use AppConfig for django >=1.7 csvimport >=2.2
...  )
...
...  python manage.py syncdb


Custom commands
---------------

INSPECTCSV

(pip install messytables to use this command)

manage.py inspectcsv importfile.csv > models.py

This returns the code for a new models file with a guesstimated model for the CSV file.
Add it to your project then run syncdb.

You can then run the import to that model for importfile.csv

NB: As it says its a guesstimate, you may have to manually tweak the generated models.py to get 
the import to work better.

If there are no headings in the CSV file, then it just uses automated ones col_1, col_2 ... etc.

IMPORTCSV

(Please note this command used to be csvimport but that caused name clash issues with the module)

manage.py importcsv --mappings='' --model='app_label.model_name' importfile.csv

For mappings enter a list of fields in order only if you dont have a header row 
with matching field names - or you want to override it, eg.

--mappings = 'column1=shared_code,column2=org(Organisation|name)'

where (model|foreign key field) is used to specify relations if again, you want to
override what would be looked up from your models.

If you have no real field names in your csv file, then you can use 
--mappings='none' and it will assume the fields are named col_1, col_2 ... etc.

Admin interface import
----------------------

Just add a csvimport item, fill in the form and submit. 
Failed import rows are added to the log field.

Demonstration installation instructions
---------------------------------------

To see how it works, you can install a demo easily enough eg. via virtual environment, 
then use the tests settings to have some sample models for importing data, and the fixtures are sample csv files.

- Run the following in your shell:

>>> virtualenv mysite
... cd mysite
... pip install django
... pip install django-csvimport
...
... cat > bin/django-admin.py << EOF
... #!/usr/bin/env python
... from django.core import management
... import os
... os.environ["DJANGO_SETTINGS_MODULE"] = "csvimport.tests.settings"
... if __name__ == "__main__":
...     management.execute_from_command_line()
... EOF
...
... django-admin.py syncdb
... django-admin.py runserver

- Go to http://127.0.0.1:8000/admin/ in your browser - pay attention to the trailing / !
- Click on add Csvimport
- Pick the django-csvimport/csvimport/tests/fixtures/countries.csv [1] and upload it
- Check to see if the Country model is now populated.

[1] also available from https://raw.github.com/edcrewe/django-importcsv/master/importcsv/tests/fixtures/countries.csv

Alternatively you can use the command line to upload

django-admin.py importcsv --model='csvimport.Country' django-csvimport/csvimport/tests/fixtures/countries.csv --settings=csvimport.tests.settings 

tzinfo monkeypatch
------------------

In order for dates to be imported outside of the timezone range of 1970-2037 
for certain database backends such as sqlite there is a patch of django.utils.timezone 

Acknowledgements
----------------

This egg was created as part of a django dash at the House of Omni, Bristol UK, organised
by Dan Fairs and my local django users group, #DBBUG. It was a core component for an application
for aid agency supply chain sharing, prompted by Fraser Stephens of the HELIOS foundation
and developed by Ed Crewe and Tom Dunham.

 

