# FSND Project 2 - Multi User Blog

## Dependencies
- Python 2
- gcloud (https://cloud.google.com/sdk/)

Udacity notes on installing gcloud: https://drive.google.com/file/d/0Byu3UemwRffDc21qd3duLW9LMm8/view

If Python3 is also installed, make sure Python2 is used by default for dev_appserver.py (located in google-cloud-sdk/bin/). Change `#!/usr/bin/env python` in the first line to `#!/usr/bin/env python2`

## Deploy

To deploy locally run `dev_appserver.py .` in the directory of the project.

To deploy to Google App Engine, run `gcloud app deploy app.yaml index.yaml` in the directory of the project. This will deploy to the project selected when setting up gcloud on your machine.

## Config

Create a file called `config.py` containing a variable `SECRET` and set SECRET to a random long string.
