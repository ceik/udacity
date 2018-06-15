# FSND Project 3 - Catalog

Catalog App that implements a category tree, Google OAuth, and user permissions

## Dependencies

The project is built with Python2 and uses:
- flask
- sqlalchemy
- requests
- oauth2client
- httplib2

The course also provides a VirtualBox & Vagrant Setup that already contains some of the dependency libraries. See
here for install instructions: https://classroom.udacity.com/nanodegrees/nd004/parts/af045689-1d81-46e7-8a3b-ad05de1142ce/modules/353202897075460/lessons/3423258756/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0

## To Run
- Run `vagrant up` & `vagrant ssh` in the vagrant folder
- Once in the VM, navigate to `/vagrant/catalog`
- Create the database by running `database_setup.py`
- (Optionally) Create some dummy data by running `create_data.py`
- Make the project run on localhost by running `catalog.py`