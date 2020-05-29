# Influenza Estimator Web Tool

## To run, open a terminal and follow the following commands:

cd into the folder of choice and enter:
```commandline
git pull https://github.com/Hephaestus12/applications.git
cd applications/gsoc_application_projects/2020/influenza/web/
```

### Installing pip

pip is the reference Python package manager. It’s used to install and update packages. You’ll need to make sure you have the latest version of pip installed.

You can make sure that pip is up-to-date by running:
```commandline
py -m pip install --upgrade pip
```

### Installing virtualenv

Note: If you are using Python 3.3 or newer, the venv module is the preferred way to create and manage virtual environments. venv is included in the Python standard library and requires no additional installation. If you are using venv, you may skip this section.

virtualenv is used to manage Python packages for different projects. Using virtualenv allows you to avoid installing Python packages globally which could break system tools or other projects. You can install virtualenv using pip.

```commandline
python3 -m pip install virtualenv
```
### Creating a virtual environment

venv (for Python 3) and virtualenv (for Python 2) allow you to manage separate package installations for different projects. They essentially allow you to create a “virtual” isolated Python installation and install packages into that virtual installation. When you switch projects, you can simply create a new virtual environment and not have to worry about breaking the packages installed in the other environments. It is always recommended to use a virtual environment while testing Python applications.

To create a virtual environment, go to your project’s directory and run venv. If you are using Python 2, replace venv with virtualenv in the below commands.
```commandline
python3 -m venv env
```

The second argument is the location to create the virtual environment. Generally, you can just create this in your project and call it env.

venv will create a virtual Python installation in the env folder.


### Activating a virtual environment

Before you can start installing or using packages in your virtual environment you’ll need to activate it. Activating a virtual environment will put the virtual environment-specific python and pip executables into your shell’s PATH.
```commandline
source env/bin/activate
```

You can confirm you’re in the virtual environment by checking the location of your Python interpreter, it should point to the env directory.
```commandline
which python
.../env/bin/python
```

As long as your virtual environment is activated pip will install packages into that specific environment and you’ll be able to import and use packages in your Python application.

### Installing packages

Now that you’re in your virtual environment you can install packages.
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





