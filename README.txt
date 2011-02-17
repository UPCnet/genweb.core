-*- rst -*-
Introduction
============

This is the next-gen agnostic version core Genweb UPC add-on product.

It defines all the base modifications to Plone by UPCnet. This modifications includes:
- Custom translations to Catalan, Spanish and English
- Default parameterization of sites
- Genweb UPC default workflows (genweb_simple, genweb_review, genweb_intranet)
- Installlation of Genweb UPC default stack add-on products
- Customization and configuration of these add-on products

TODO
====
- How to handle the properties via new plone.registry
- Custom Workflows modifications of PloneBoard and Poi. It's needed to create a custom package for it.
- Choose the custom structure/viewlets/CSS modifications made to all flavors may apply here (e.g DocumentActions)
- Constraints to use in folders.
- Check if the patches in gemweb.patches are longer necessary for new versions of products.
- Trim and make more sostenible utils.py.
- Move language selector into a independent language selector.

New Packages
------------
- genweb.resources
- genweb.workflows
- genweb.controlpanel
- genweb.setup
- genweb.patches
- genweb.content

Tests
-----
- setup_view (genweb.setup)
