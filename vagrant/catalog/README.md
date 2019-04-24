# Udacity-Catalog-Project

Visit my Portfolio at: [nicklobo](http://nicklobo.com.br/)

# What it is
Application that provides a list of items within a variety of categories, third-party user registration and authentication system.
Registered users have the ability to post, edit, and delete their own items.

Technologies used:
- [SQLite](https://www.sqlite.org/index.html) - SQL database engine.
- [SQLAlchemy](https://www.sqlalchemy.org/) - Python SQL toolkit and Object Relational Mapper.
- [Flask](http://flask.pocoo.org/) - microframework for Python.
- [New Google Sign-in](https://developers.google.com/identity/sign-in/web/)
- [google-auth](https://google-auth.readthedocs.io/en/latest/) - Updated library as of 2019.
- [Facebook for developers](https://developers.facebook.com/docs/facebook-login/web) - Login with facebook.

Tools:
- [VirtualBox](https://www.virtualbox.org/) - x86 and AMD64/Intel64 virtualization.
- [Vagrant](https://www.vagrantup.com/) - Tool for building and managing virtual machine environments in a single workflow.

## Table of Contents
- [What it is](https://github.com/nicholasinatel/fullstack-nanodegree-vm/tree/master/vagrant/catalog/#what-it-is)
- [Dependencies](https://github.com/nicholasinatel/fullstack-nanodegree-vm/tree/master/vagrant/catalog/#dependencies)
- [Configuration](https://github.com/nicholasinatel/fullstack-nanodegree-vm/tree/master/vagrant/catalog/#configuration)
- [Run](https://github.com/nicholasinatel/fullstack-nanodegree-vm/tree/master/vagrant/catalog/#run)
- [JSON_Routes](https://github.com/nicholasinatel/fullstack-nanodegree-vm/tree/master/vagrant/catalog/#json_routes)
- [Details](https://github.com/nicholasinatel/fullstack-nanodegree-vm/tree/master/vagrant/catalog/#details)
- [License](https://github.com/nicholasinatel/fullstack-nanodegree-vm/tree/master/vagrant/catalog/#license)

## Dependencies
Install the following softwares
- [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) - Install the platform package for your operating system. There is no need for installing the extension pack or the SDK. Do not launch Virtual Box, the Vagrant software will run it.
- [Vagrant](https://www.vagrantup.com/downloads.html) - Download the version of your operating system.

After downloading the software’s, git clone the virtual machine configuration at your work station:
- [catalog](https://github.com/nicholasinatel/fullstack-nanodegree-vm/) - This will give you a folder, containing the VM files.


## Configuration
1 - **Start the virtual machine** by going to the cloned folder and executing `vagrant up` inside the vagrant directory, once the command finishes running, type `vagrant ssh`

2 - **Inside the vagrant environment**, run `cd /vagrant/catalog` for the shared folder with access to the Virtual Machine, your current OS and the project files.

In case of problems do step 3.

3 - Delete the file `catalog.db` and execute `python populateDb.py`.


# Run

1- Execute `python application.py`. If everything is fine, than go to `localhost:5000/`, you should see the initial screen of the web app. If you dont execute the step 3 at configuration and than try this procedure again.

## JSON_Routes

```
# Show all Categories
http:localhost:5000/category/JSON

# Show itens
http:localhost:5000/category/<int:category_id>/JSON
http:localhost:5000/category/<int:category_id>/item/JSON

# Show Single item
http:localhost:5000/category/<int:category_id>/item/JSON
http:localhost:5000/category/<int:category_id>/item/<int:item_id>/JSON

# Show Rentability
http:localhost:5000/category/<int:category_id>/item/<int:item_id>/rentability/JSON

# Show Single Rentability
http:localhost:5000/category/<int:category_id>/item/<int:item_id>/rentability/<int:rentability_id>/JSON
```

## Details
If you are not looged in, you will see the default demonstration user data.

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