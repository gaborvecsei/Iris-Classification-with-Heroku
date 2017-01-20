# Iris Classification Deployed at Heroku

This is an example how can you deploy your Machine Learning code to Heroku.

It also contains code for a really simple **Android app** which uses the deployed project.

## Setup

To deploy it at [Heroku](https://www.heroku.com/):

Set a new `Config var` at your created Heroku app:
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

## Test it!

After you made all the steps above you can go to `<your_heroku_app_name>.herokuapp.com`.
You sould see the homepage.

Try out prediction: `<your_heroku_app_name>.herokuapp.com/predict/3.4-4.1-5.1-0.3`. After that you can see the json for the prediction.

For exmaple, here is a live demo with this code:

* Homepage: [http://iris-classifier-example.herokuapp.com/](http://iris-classifier-example.herokuapp.com)
* Prediction: [http://iris-classifier-example.herokuapp.com/predict/3.4-4.1-5.1-0.3](http://iris-classifier-example.herokuapp.com/predict/3.4-4.1-5.1-0.3)

## Android Images

<img  height=600 src="http://i.imgur.com/MlpHoYi.png" />
<img  height=600 src="http://i.imgur.com/QblVzRB.png" />

## About

Vecsei Gábor

<mailto:vecseigabor.x@gmail.com>

[Personal Blog][1]

[LinkedIn][2]

[Github][3]


[1]: http://gaborvecsei.wordpress.com
[2]: http://www.linkedin.com/in/vecsei-gabor
[3]: https://github.com/gaborvecsei
