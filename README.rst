.. flake8: noqa

======
README
======

LICENSE
=======

See TOPMATTER_.

.. _TOPMATTER: https://github.com/cldershem/homelessgaffer/blob/master/TOPMATTER.rst

INSTALLATION
============

- prereqs on `git`, `python-pip`

.. code:: sh

  git clone /var/www/homelessgaffer.com
  cd /home/$USER
  git init --bare homelessgaffer.git
  mv homelessgaffer.git/hooks homelessgaffer.git/hooks.bak
  ln -s /var/www/homelessgaffer.com/.githooks ./homelessgaffer.git/hooks

- `/var/www/homelessgaffer.com` must be owned by user, add write to group?
- if needed set `baseDir` in `homelessgaffer.git/hooks/post-receive`
- edit `/etc/sudoers` to add

.. code::

  cldershem ALL= NOPASSWD: /usr/sbin/service nginx \*
  cldershem ALL= NOPASSWD: /usr/sbin/service uwsgi \*

- fill out secrets.py

.. code:: sh

  cp secrets.py.example secrets.py

- setup virtualenv

.. code:: sh

  sudo apt-get install virtualenv
  sudo pip install virtualenvwrapper
  mkvirtualenv hg
  workon hg
  pip install -r requirements.txt

- run dev server

.. code:: sh

  workon hg
  python manage run

TODO
====

User issue_tracker_.

.. _issue_tracker: https://github.com/cldershem/homelessgaffer/issues

ISSUES
======

Tracked at issue_tracker_.

.. _issue_tracker: https://github.com/cldershem/homelessgaffer/issues

CHANGELOG
=========

- moved all issues/requests/etc to github issue tracker
- manage backup_db backs up and zips locally (not remotely)
- create_admin works with recaptcha properly
- create_admin works with recaptcha in `app.forms` commented out.
- moved `get_activation_link` and the like to staticmethods under User
- added google analytics
- updated githooks to work with virtualenvwrapper
- using virtualenvwrapper
- replace `run.py` with `python manage.py run`
- begin work on manage.py
- change `app.models.Unity.get_unique()` to `app.models.Unity.get()`
- bug fix: title 'page' when reloading page from submission error
- remove <strong> from page numbers
- abstracted db calls out

  - instead of `User.objects.get(tag='taco')` use `User.find()`

- add secrets.py.example
- add docstrings for a lot of things
- draft mode for new pages and posts working

  - viewable only by author or admin
  - hg.com/page/newpagetitle/draft (uses new/edit template)

- begin work on new navbar
- disqus implemented..
- add DEBUG back to config
- add testing disqus db
- hashed password reset link oldpwd has inside of payload
- remove google and facebook login that was never finished
- password reset link cannot be reused

  - added oldpwdhash to payload

- fix bug where login wouldn't work with extra whitespace (common on phones)
- update flask-pagedown
- commented out blog and page
- add unity.summary
- begin work on updated resume
- githook fixed
- fix bug where unity.tags and unity.sources show up when empty
- fix admin pages not having authentication

  - only admin can login

- fix static html file page
- renamed "page" to "pageTitle"
- add pageTitle to title bar
- fix Sources as TagListField
- fixed unity/edit tags is populated with "[]"
- fix edit post error where slug would be duplicate
- add custom TagListField
- removed ckeditor
- Unity working.
- fixed "if server: debug=False"

  - DEBUG flag now set in app/__init__.py

- sidebar block added to base template
- add markdown support

  - add pagedown editor with preview
  - remove ckeditor from templates
  - add [[wikilink]] support

- made forms into a macro
- disabled user registration until needed
- fixed BASE-DIR in pre hook
- finished user blueprint
- finished blog blueprint
- finished Page Blueprint
- fixed listpages
- Page Blueprint add
- currentPage navButton works again
- added anon-required decorator
- added forgot password
- user confirm email uses token
- user can only login after confirmation
- added confirmation email
- flask-mail is async
- flask-mail setup
- added constants.py
- dateTimeNow deprecated, DATE-TIME-NOW replaces (underscores not hyphens)
- git hook downloads js libraries
- git hook restarts nginx, uwsgi PROPERLY!!!!!!
- rewrote git hooks in python, added flake8
- added githooks to repo and created working symlinks
- githook only runs pip when changes
- added post-receive githook for pip install -r requirements.txt
- added pre-commit githook for pip freeze
- added secrets.py
- added recaptcha
- set up bcrypt
- fixed vim on hg.com
- changed all times to utc
- no page number if only one page
- added pagination on posts
- add https
- flask admin working
