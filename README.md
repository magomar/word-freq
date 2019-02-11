# Word Frequency

Web app using Flask that calculates word-frequency pairs based on the text from a given URL.
This project is the output the tutorial [Flask By Example](https://realpython.com/flask-by-example-part-1-project-setup/).

That tutorial addresses the creation and deploying of a flask app on Heroku using multiple configurations (development, testing, staging, production)

In particular, two projects are created on Heroku, with two separate configurations:

```shell
heroku config:set APP_SETTINGS=config.StagingConfig --remote stage
heroku config:set APP_SETTINGS=config.ProductionConfig --remote pro
```
