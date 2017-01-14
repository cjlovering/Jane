# Jane
a facebook chat bot capable of incredible things

# Authors

### Set Up
* install dependencies with
```bashe
pip install -r requirements.txt
```
* install heroku command line at
```
https://devcenter.heroku.com/articles/heroku-cli
```

### Being able to talk to Jane
* go to facebook developers, accept request
* go to https://www.facebook.com/Jane-1332708036751329/
* send message

### link git repo with existing heroku app
```
git remote add heroku git@heroku.com:jane-bot.git
heroku git:remote -a jane-bot
```
Then go ahead make changes.

Then do the following:
```
git add changed-file-name
git commit -m "clear message"
git pull origin master
# fix merge conflicts
git push origin master
git push heroku master
```


