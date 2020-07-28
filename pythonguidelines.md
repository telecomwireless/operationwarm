* filenames should be all lowercase, with underscores if that improves readability. Similarly, directory names should be all lowercase, without underscores if at all avoidable.

`Do This: awesomething/data/load_settings.py`
`NOT This: awesomething/Data/LoadSettings.py`

* Any Python (.py) file is a module, and a bunch of modules in a directory is a package. To make a dir in to package there should be __init__.py file. 

* Example project structure here https://dev.to/codemouse92/dead-simple-python-project-structure-and-imports-38c6

* To generate requirements file from pip  

`pip3 freeze > requirements.txt`