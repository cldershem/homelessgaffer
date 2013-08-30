# flake8: noqa
###INSTALLATION
- download and install in /path/to/repo/static/js
    - ckeditor
    - kinetic.js
    - less
- scp secrets.py
- Git-hooks
    - mv .git/hooks .git/hooks.bak
    - ln -s /path/to/repo/.githooks/ /path/to/repo/.git/hooks
- restart nginx, uwsgi

###TODO
- git hook
    - push github, web
- Search
- ckeditor css a:hover
- flask-principal
- user
    - can edit own posts or if admin
    - post edited on
    - profile with all posts
    - forgot password
    - confirm email
- add delete to edit page/post
- fix datetime display
    - moment.js?
- edit page doesn't work
- add tests
- fix default nginx error pages
- Admin
    - fix redirect after password change fail
- fix users and permissions
    - including /etc/sudoers
- flake8 should only check .py files

###CHANGELOG
- git hook restarts nginx, uwsgi PROPERLY!?!?!?
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
