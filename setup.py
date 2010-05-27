from setuptools import setup, find_packages
import os

version = '3.5'

setup(name='genweb.core',
      version=version,
      description="Genweb core package",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='genweb',
      author='UPCnet Plone Team',
      author_email='plone.team@upcnet.es',
      url='https://dev.genweb.upc.edu/svn/core/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['genweb'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
#          'upc.genweb.banners',
#          'upc.genweb.logosfooter',
#          'upc.genweb.meetings',
#          'upc.genweb.descriptorTIC',
#          'upc.genweb.kbpuc',
#          'upc.genweb.objectiusCG',
#          'upc.genweb.patches',
#          'upc.permalink',
#          'upc.genweb.serveis',
#          'upc.remotecontrol',
#          'upcnet.simpleTask',
#          'plone.app.blob',
#          'upcnet.cas',
#          'Products.AJAXAddRemoveWidget',
#          'Products.PloneLDAP',
#          'Products.FCKeditor',
#          'Products.Ploneboard',
#          'Products.PloneFormGen',
#          'Products.LinguaPlone',
#          'Products.Collage',
#          'Products.Poi',
#          'Products.AddRemoveWidget',
#          'Products.DataGridField',
#          'Products.PythonField',
#          'Products.TemplateFields',
#          'Products.TALESField',
#          'Products.PloneSurvey',
#          'Products.ZMySQLDA',
#          'Products.windowZ',
#          'Products.PlonePopoll',
#          'archetypes.schemaextender',
#          'BeautifulSoup',
#          'zope.i18nmessageid',      
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
