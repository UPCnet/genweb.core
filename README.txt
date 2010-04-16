Introduction
============

This is the next-gen agnostic version core Genweb UPC add-on product.

It defines all the base modifications to Plone by UPCnet. This modifications includes:
- Custom translations to Catalan, Spanish and English
- Default parameterization of sites
- Genweb UPC default workflows (genweb_simple, genweb_review, genweb_intranet)
- Installlation of Genweb UPC default stack add-on products
- Customization and parameterize this add-on products

TODO
====
- How to handle the properties via new plone.registry
- Custom Workflows modifications of PloneBoard and Poi. It's needed to create a custom package for it.
- Choose the custom structure/viewlets/CSS modifications made to all flavors may apply here (e.g DocumentActions)
- Constraints to use in folders.

New Packages
------------
- genweb.resources
- genweb.workflows
- upc.genweb.config
- upc.genweb.customfck
- upc.genweb.initialcontent
- upc.genweb.content