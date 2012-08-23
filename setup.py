from setuptools import setup, find_packages
import os

version = '4.2b1'

setup(name='genweb.core',
      version=version,
      description="Genweb core package",
      long_description=open("README.rst").read() + "\n" +
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
      extras_require={'test': ['plone.app.testing', ]},
      install_requires=[
          'setuptools',
          'requests',
          'genweb.theme',
          'genweb.controlpanel',
          'genweb.stack',
          'genweb.portlets',
          'upc.genweb.banners',
          'upc.genweb.logosfooter',
          'upc.genweb.meetings',
          'upcnet.simpleTask',
          'upc.genweb.serveis',
          'upc.genweb.descriptorTIC',
          'upc.genweb.kbpuc',
          'upc.genweb.objectiusCG',
          'upc.genweb.soa',
          'upc.genweb.recaptcha',
          'upc.cloudPrivat',
          'upcnet.cas',
          'upcnet.stats',
          'Products.LinguaPlone',
          'plone.app.ldap',
          'plone.app.caching',
          'Products.DataGridField',
          'Products.ZMySQLDA',
          'archetypes.schemaextender',
          'plone.app.dexterity [grok]',
          'plone.app.referenceablebehavior',
          'plone.app.relationfield',
          'plone.namedfile [blobs]',
          'collective.pfg.dexterity',
          'plone.app.workflowmanager',
          # Experimental GW4
          'Solgema.fullcalendar',
          'collective.panels',
          'wildcard.foldercontents',
          # To extinct
          'upc.genwebupc',
          'upc.genwebupctheme',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
