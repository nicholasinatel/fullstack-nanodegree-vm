# Restaurant-Menu-App

Visit my Portfolio at: [nicklobo](http://nicklobo.com.br/)

# What it is
A Menu App with Flask that lists out all the restaurants in a SQLite database throw SQLAlchemy.
The app allows the user to view the menu for all the registered restaurants.
Users are also able to create, read, update and delete restaurants and menus items.
Used Flash for pop-up messages and jsonify for json api endpoints.

Technologies used:
- [SQLite](https://www.sqlite.org) - SQLite is the most used database engine in the world.
- [SQLAlchemy](https://www.sqlalchemy.org/) - SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.
- [Flask](http://flask.pocoo.org/) - Flask is a microframework for Python based on Werkzeug, Jinja 2 and good intentions.

Tools:
- [VirtualBox](https://www.virtualbox.org/) - x86 and AMD64/Intel64 virtualization.
- [Vagrant](https://www.vagrantup.com/) - Tool for building and managing virtual machine environments in a single workflow.

## Table of Contents
- [What it is](https://github.com/nicholasinatel/fullstack-nanodegree-vm/tree/master/vagrant/lessons/02-flask/09-final-project/#what-it-is)
- [Dependencies](https://github.com/nicholasinatel/fullstack-nanodegree-vm/tree/master/vagrant/lessons/02-flask/09-final-project/#dependencies)
- [Configuration](https://github.com/nicholasinatel/fullstack-nanodegree-vm/tree/master/vagrant/lessons/02-flask/09-final-project/#configuration)
- [Objective](https://github.com/nicholasinatel/fullstack-nanodegree-vm/tree/master/vagrant/lessons/02-flask/09-final-project/#objective)
- [License](https://github.com/nicholasinatel/fullstack-nanodegree-vm/tree/master/vagrant/lessons/02-flask/09-final-project/#license)

## Dependencies
Install the following softwares
- [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) - Install the platform package for your operating system. There is no need for installing the extension pack or the SDK. Do not launch Virtual Box, the Vagrant software will run it.
- [Vagrant](https://www.vagrantup.com/downloads.html) - Download the version of your operating system.


## Configuration
1 - **Start the virtual machine** by going to the installed folder and executing `vagrant up` , once the command finishes running, type `vagrant ssh`

2 - **Inside the vagrant environment**, run `cd /vagrant` for the shared folder with access to the Virtual Machine, your current OS and the project files.

3 - Execute ```python lotsofemnus.py``` to create the example database

4 - Execute ```python finalproject.py``` and go to the following url: ```localhost:5001```

## Objective
Practice skills on building webapp from previous planning, this is the sketch i made to plan for this project:
- [Sketch](https://github.com/nicholasinatel/fullstack-nanodegree-vm/tree/master/vagrant/lessons/02-flask/09-final-project/resources/Menu-App-Sketc.pdf)

## License
MIT License

Copyright (c) [2018] [Nicholas Lobo]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.