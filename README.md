###DONT FORGET TO
- pip -r requirements.py
- secret key
- ckeditor
- kinetic.js
- less
- redo users with bcrypt

###TODO
- git hook
    - push github, web
    - check flake8
    - restart nginx, uwsgi
- Search
- ckeditor css
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
- redirect after login/register
- add tests
- fix default nginx error pages
- Admin
    - fix redirect after password change fail

###CHANGELOG
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

##GITHOOKS
mv .git/hooks .git/hooks.bak
ln -s /path/to/repo/.githooks/ /path/to/repo/.git/hooks
