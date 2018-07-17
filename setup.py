from setuptools import setup, find_packages
import os

version = '4.8.53'

README = open('README.rst').read()
HISTORY = open(os.path.join('docs', 'HISTORY.rst')).read()

setup(name='genweb.core',
      version=version,
      description='Genweb core package',
      long_description=README + '\n' + HISTORY,
      classifiers=[
          'Environment :: Web Environment',
          'Framework :: Plone',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Libraries :: Python Modules',
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
      extras_require={'test': ['plone.app.robotframework',
                               'plone.app.testing[robot] >= 4.2.4']},
      install_requires=[
          'setuptools',
          'requests',
          'five.grok',
          'plone.api',
          'genweb.theme',
          'genweb.cdn',
          'genweb.js',
          'genweb.portlets',
          'genweb.controlpanel',
          'plone.app.caching',
          'archetypes.schemaextender',
          'plone.app.dexterity [grok,relations]',
          'plone.app.contenttypes',
          'plone.app.event[dexterity]',
          'plone.app.referenceablebehavior',
          'plone.app.lockingbehavior',
          'plone.namedfile [blobs]',
          'plone.app.workflowmanager',
          'collective.tinymcetemplates',
          'wildcard.foldercontents',
          'jarn.jsi18n',
          'Products.PloneLDAP',
          'quintagroup.seoptimizer',
          'pyquery',
          'souper.plone',
          'elasticsearch',
          'simplejson',
          'pyyaml',
          'ipdb',
          'plone.restapi'
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      [console_scripts]
      do_install_pre_commit_hook = genweb.core:install_pre_commit_hook
      uninstall_pre_commit_hook = genweb.core:uninstall_pre_commit_hook
      """,
      )
