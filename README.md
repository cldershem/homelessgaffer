###DONT FORGET TO
- pip -r requirements.py
- secret key
- ckeditor
- kinetic.js
- less
- redo users with bcrypt

###TODO
- git hook
    - pip freeze > requirements.txt
    - push github, web
    - pip install -r requirements.txt
    - sudo service nginx restart
    - sudo service uwsgi restart
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
