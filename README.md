<!--flake8: noqa-->
###INSTALLATION
```
git clone /var/www/homelessgaffer.com
cd /home/$USER
git init --bare homelessgaffer.git
mv homelessgaffer.git/hooks homelessgaffer.git/hooks.bak
ln -s /var/www/homelessgaffer.com/.githooks ./homelessgaffer.git/hooks
```
- /var/www/homelessgaffer.com must be owned by user, add write to group?
- if needed set "baseDir" in homelessgaffer.git/hooks/post-receive
- add to /etc/sudoers
```
cldershem ALL= NOPASSWD: /usr/sbin/service nginx \*
cldershem ALL= NOPASSWD: /usr/sbin/service uwsgi \*
```
- cp secrets.py

TODAY
=====
- all files in /var/www/homelessgaffer.com owned by cldershem
- move logs to /var/www/hg/tmp/log
- database copy
- database migrate (see below)
- tty or askpwd would solve sudoers issue
- add pwdhash to pwdreset token

###TODO
- Search
- user
    - can edit own posts or if admin
    - post edited on
    - profile with all posts
    - does forgot it need to be in the admin panel?
    - registration shouldn't save unless all goes well
        - currently will save if error
    - change password
    - email on comment
    - new accounts need to be approved
- add delete to edit page
- fix datetime display
    - moment.js?
- add tests
- fix default nginx error pages
- Admin
    - fix redirect after password change fail
- flake8 should only check .py files
- find better way to do async
- make it not look like crap
- disqus for comments?
- get some content
- make some better classes
    - user should have an update method?
- admin approval of new users
- draft mode for new pages and posts
    - @adminOrAuthorRequired
    - hg.com/page/newpagetitle/draft (uses new/edit template)
- api to add pages from (so you can write them in vim)
- integrate bike wiki?
    - moinmoin?
    - is another framework really necessary?
    - roll your own wiki?
        - similar/same as/ replace 'page' blueprint as wiki?
        - create newWikiPage and newWikiPage-Discussion for each page
        - blog/page/wiki selector?
        - orphaned pages
            if wikilink is orphan,
                mark as such,
                if not on OrpanedPagesList
                    add
            else link to wikipage
        - breadcrumbs
        - allow TODO on each page
            - When TODO list is updated
                - sitewide TODO list is updated using page name to organize
        - each post can be published or draft
            - drafts or private until published?
            - post can be pushed to blog with tags
            - page/wiki/blog all the same things?
- add sidebar to blog
    - sidebar has categories, related posts, etc
- fix resume
    - embed pdf
    - resume push to release updates website
- add drop down menus to nav bar
- shorten homelessgaffer.com when smaller viewport
- fix title 'page' when reloading page from submission error
- fix alignment on login page with the "or"s
- fix spacing between header and first line
- fix blog list markdown stripping looking dumb
- fix pagedown editor preview --- looks like crap
    - figure out pagedown editor wmd-button-bar
- fix form css in general
- comments vs discussion
    - think wikipedia discussion pae
- make it so you can import MAIL and not each individulal Mail_USERNAME
- find word for create or edit if exists for unity new/edit/draft page
- do i need a robots.txt
- tags need to be slugified
- make admin redirect if not logged in..
- add cancel button
- add resend confirm email
- sometimes listposts in wrong order
- "are you sure you want to navigate away from this page?"
- create db, add admin@hg.com with admin privlidges
- migrate db
- make requirements.txt check version numbers
- trunicate 'source'
- merge battleship repos
- create random salt for every user?

###CHANGELOG
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

###NOTES
- blog
    - food
    - bike
- dev
    - battleship
- about
    - contact
    - resume
