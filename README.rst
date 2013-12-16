.. flake8: noqa

======
README
======

INSTALLATION
============
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


TODO
====

LOOK
----

- make it not look like crap
- fix resume

  - embed pdf?
  - resume push to release updates website

    - git module?

- add sidebar to blog

  - sidebar has categories, related posts, etc.

- fix alignment on pages with forms
- fix spacing between header and first line
- shorten homelessgaffer.com when smaller view port
- fix blog list markdown stripping looking dumb
- fix pagedown editor preview --- looks like crap

  - figure out pagedown editor wmd-button-bar

- truncate `unity.source`
- fix datetime display

  - moment.js?

SERVER
------

- all files in /var/www/homelessgaffer.com owned by cldershem
- move logs to /var/www/hg/tmp/log
- database copy
- database migrate (see below)
- `tty` or `askpwd` would solve sudoers issue
- fix default nginx error pages
- make requirements.txt check version numbers
- create db, add admin@hg.com with admin privileges
- migrate db

FEATURE REQUESTS
----------------

- Search
- add delete to edit page
- add cancel button
- add resend confirm email
- breadcrumbs

  - cldershem@hg.com/blog/post-name

- add index.html to staticUnity

  - really add all .html to the db
  - need to be able to add sidebar from post

- api to add pages from (so you can write them in vim)
- user features

  - can edit own posts or if admin
  - post edited on
  - profile with all posts
  - can view all drafts
  - does forgot it need to be in the admin panel?
  - registration shouldn't save unless all goes well

    - currently will save if error

  - change password
  - email on comment
  - new accounts need to be approved

- integrate bike wiki?

  - http://homelessgaffer.3821.a.hostable.me/wikitest/tikiwiki/tiki-index.php
  - create newWikiPage and newWikiPage-Discussion for each page
  - orphaned pages

    - if wikilink is orphan,

      - mark as such,
      - if not on OrpanedPagesList

        - add
      - else link to wikipage
    - allow TODO on each page

      - When TODO list is updated

        - sitewide TODO list is updated using page name to organize

  - each post can be published or draft

    - drafts or private until published?
    - post can be pushed to blog with tags
    - page/wiki/blog all the same things?
    - make draft/blog drop down

- "are you sure you want to navigate away from this page?"

SECURITY
--------

- password salt for each user

  - should password reset oldhash be the last 10 characters instead of first?

- admin email to approve each user

  - user signs up
  - admin gets email "user wants an account"
  - if admin approves

    - user gets email verification email

  - if admin doesn't approves

    - user gets email notifying them that their request was denied

BUG FIXES
---------

- Admin

  - fix redirect after password change fail

- when on page 6 of listPages page 3 in pager is None?
- fix title 'page' when reloading page from submission error
- sometimes listPosts in wrong order
- make admin redirect if not logged in..

MISC
----

- get some content
- rename unity
- replace `#!/venv/bin/python` with `!/usr/bin/env python`
- merge battleship repos
- flake8 should only check .py files
- make it so you can import MAIL and not each individual Mail_USERNAME
- do I need a robots.txt
- comments vs discussion

  - think wikipedia discussion page
  - is disqus just good enough?

    - if so remove old comment system from code

- find better way to do `@async`, celery?
- add tests/logging
- find word for create or edit if exists for unity new/edit/draft page
- tags need to be slugified

CHANGELOG
=========

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
