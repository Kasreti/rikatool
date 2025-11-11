# Rikatool - Rikatisyï Dictionary and Tool
welcome to rikatool. this is sort of a remastered version of my csia, without the in-app conlang customizability, and solely focused on providing accurate information about rikatisyï.
note that i'm not particularly good of a programmer, so expect weird programming

# Installation guide
downloand and unzip a release (although for now just clone the repos)
you will need to have python 3 installed on your device (online or fm microsoft store also ok)
```
cd <file directory>
.venv\Scripts\Activate
```
note: currently the venv folder is missing from the repos, so run
```
py -3 -m venv .venv
pip install flask flask_migrate flask_sqlalchemy flask_wtf
```

# Running the application
there will be an online-hosted version of this programme at https://rikatool.onrender.com/ (sometimes up. sometimes)
otherwise, cd to the file directory and run
```
.venv\Scripts\Activate
flask run
```
it'll be hosted at localhost:5000

# Updating the dictionary
simply ctrl+a, ctrl+c and ctrl+v the entireity of the hayalese dict. into the dict.txt, followed by hitting the "refresh dictionary" button in-app. any errors will be displayed in console -- those are normally due to improper entry formatting.
