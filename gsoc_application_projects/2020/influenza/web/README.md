# Influenza Estimator Web Tool

## To run, open a terminal and follow the following commands:

cd into the folder of choice and enter:
```commandline
git pull https://github.com/Hephaestus12/applications.git
cd applications/gsoc_application_projects/2020/influenza/web/
```

### Prepare the Environment

Make sure your have a python environment with Python 3.5
You will have to manually compile and install Shogun from source into that environment. Only then will you be able to run the webapp.

You can find the instructions for doing that [here](http://blog.detoni.me/2018/10/08/Compile-Shogun-with-Conda/).

### Installing packages

You have to install the following packages into your python environment.
```commandline
pip install -r requirements.txt
```

### Running the application
```commandline
export FLASK_APP=influenza_estimator
export FLASK_ENV=development
flask run
```

Your flask application should be successfully running once this is done.



# Influenza API Guide

#### GET the Live influenza ESTIMATE numbers as a JSON file for all countries.
Send a GET request to the following Endpoint:
```
/api/v1.0/all/current/
```


#### GET older influenza ESTIMATE numbers as a JSON file for all countries.
Send a GET request to the following Endpoint:
```
/api/v1.0/all/weekly/estimate/<int:year>/<int:week>/
```


#### GET older influenza INCIDENCE numbers as a JSON file for all countries.
Send a GET request to the following Endpoint:
```
/api/v1.0/all/weekly/incidence/<int:year>/<int:week>/
```


#### GET the Live influenza ESTIMATE number as a JSON file for one country.
Send a GET request to the following Endpoint:
```
/api/v1.0/specific/current/<string:country>
```


#### GET the older influenza ESTIMATE number as a JSON file for one country..
Send a GET request to the following Endpoint:
```
/api/v1.0/specific/weekly/estimate/<int:year>/<int:week>/<string:country>
```


#### GET the older influenza INCIDENCE number as a JSON file for one country.
Send a GET request to the following Endpoint:
```
/api/v1.0/specific/weekly/incidence/<int:year>/<int:week>/<string:country>
```
