# OpenCV, Keras, Flask Sample and Example

## Setup

To deploy it at [Heroku](https://www.heroku.com/):

Set a new **Config var** at Heroku:
`KERAS_BACKEND=theano` !!!

```
git init
git add --all
git commit -m "init"

heroku apps:create your-app-name
heroku buildpacks:add https://github.com/gaborvecsei/conda-buildpack

git push heroku master

heroku ps:scale web=1
```

And you are done! :sunglasses: