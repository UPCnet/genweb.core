from setuptools import setup, find_packages
import os

version = '4.4.0'

README = open("README.rst").read()
HISTORY = open(os.path.join("docs", "HISTORY.rst")).read()

setup(name='genweb.core',
      version=version,
      description="Genweb core package",
      long_description=README + "\n" + HISTORY,
      classifiers=[
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='genweb',
      author='UPCnet Plone Team',
      author_email='plone.team@upcnet.es',
      url='https://github.com/upcnet/genweb.core',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['genweb'],
      include_package_data=True,
      zip_safe=False,
      extras_require={'test': ['plone.app.testing']},
      install_requires=[
          'setuptools',
          'requests',
          'five.grok',
          'five.pt',
          'plone.api',
          'genweb.theme',
          'genweb.alternatheme',
          'genweb.portlets',
          'genweb.controlpanel',
          'plone.app.caching',
          'archetypes.schemaextender',
          'plone.app.dexterity [grok,relations]',
          'plone.app.contenttypes',
          'plone.app.event[dexterity]',
          'plone.app.multilingual[archetypes]',
          'plone.app.referenceablebehavior',
          'plone.namedfile [blobs]',
          'plone.app.workflowmanager',
          'collective.tinymcetemplates',
          'wildcard.foldercontents',
          'jarn.jsi18n',
          'Products.PloneLDAP'
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
