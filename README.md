# flake8: noqa
###INSTALLATION
- clone repo
- Git-hooks
    - mv .git/hooks .git/hooks.bak
    - ln -s /path/to/repo/.githooks/ /path/to/repo/.git/hooks
    - set baseDir in .githooks/post-receive
    - add to /etc/sudoers
        - "cldershem ALL= NOPASSWD: /usr/sbin/service nginx *"
        - "cldershem ALL= NOPASSWD: /usr/sbin/service uwsgi *"
    -cp secrets.py

###TODO
- push github, web at same time?
- Search
- flask-principal
- user
    - can edit own posts or if admin
    - post edited on
    - profile with all posts
    - forgot password
    - registration shouldn't save unless all goes well
        - currently will save if error
- add delete to edit page/post
- fix datetime display
    - moment.js?
- edit page doesn't work
- add tests
- fix default nginx error pages
- Admin
    - fix redirect after password change fail
- flake8 should only check .py files
- update "basedir" in post and pre hooks to BASE-DIR and use it correctly
- find better way to do async

###CHANGELOG
- user confirm email uses token
- user can only login after confirmation
- added confirmation email
- flask-mail is async
- flask-mail setup
- added constants.py
- dateTimeNow depricated, DATE-TIME-NOW replaces (underscores not hyphens)
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
