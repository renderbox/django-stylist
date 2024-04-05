![Stylist CI](https://github.com/renderbox/django-stylist/workflows/Stylist%20CI/badge.svg)

![Stylist Develop](https://github.com/renderbox/django-stylist/workflows/Stylist%20Develop/badge.svg)

# Stylist

App for updating and manipulating SASS/SCSS compiling on the fly

## Installation Options
Full install if you need to compile sass on the fly: `pip install django-stylist[sass]`
If you just need the model to store style values: `pip install django-stylist`

## Upgrading from from 0.1.x

Legacy users should add the setting STYLIST_USE_SASS = True should they choose to continue compiling sass files.