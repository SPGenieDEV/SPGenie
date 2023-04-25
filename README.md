# SP GENIE
## Predict your user story value


SP GINIE is software it generates user story value and explanation for 
given user story.

## Features

- Predict story point value for user user story
- Predict for multiple user stories
- Genarate the predicted values as csv
- Find out the explain
- Export CSVs


This text you see here is *actually- written in Markdown! To get a feel
for Markdown's syntax, type some text into the left window and
watch the results in the right.

## Tech

SP GENIE uses a number of open source projects to work properly:

- [Flask] - Flask
- [JS] - Java Script
- [Tenser flow] - Tenser Flow
- [PyTorch] - PyTorch libraries

And of course Dillinger itself is open source with a [public repository][dill]
 on GitHub.

## Installation


Install the dependencies and devDependencies and start the server.

```sh
cd SPGenie
pip install requirement.txt
-m flask run 
```
## Documentation


After the run the application you can route to the below link.

- [ http://localhost:5000/api/docs/ ] - SWAGGER DOC

## Plugins

SPGINIE is currently extended with the following plugins.
Instructions on how to use them in your own application are linked below.

| Plugin | README |
| ------ | ------ |
| GitHub | [plugins/github/README.md][PlGh] |
| Google Drive | [plugins/googledrive/README.md][PlGd] |


   [flask]: <https://flask.palletsprojects.com/en/2.2.x/installation/>
   [JS]: <https://developer.mozilla.org/en-US/docs/Web/JavaScript>
   [Tenser flow]: <https://www.tensorflow.org>
   [PyTorch]: <https://pytorch.org/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>
   [ http://localhost:5000/api/docs/ ]:"http://localhost:5000/api/docs/#/"

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
