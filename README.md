[![Build Status](https://travis-ci.com/t4christ/esusu.svg?branch=master)](https://travis-ci.com/t4christ/esusu)


## Project Title
Esusu

## Project Overview
Esusu Confam Ltd is a Co-operative organization which digitalises their operations to allow customers save a fixed amount automatically every week, month or year and then one of the members collects the money at the end of every periodic interval stated.

## Prerequistes
- django
- pip
- docker
- python3


## Installing
- install docker on your machine
- install django on your machine
- run docker-compose build to build images and install all packages in the container


## Running the test
- Run 'docker-compose exec api python manage.py test' to run all the test cases.

## Required Features
- User can sign up.
- User can sign in.
- User can delete account.
- User can update account.
- Admin user can create a co-operate account group.
- Admin user can update a co-operate account group.
- Admin user can view all members in a group.
- Admin user can send a user invite link.
- User can join a group and save.
- User can update savings account.
- User can search groups.


## API Documentation
 Access api documentation through this link [![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/2d2dfeb1272ea4deacb7)


## Base Url
Project base url can be accessed using this link [Here](http://esusudocker-env.nb2m2kzsxk.us-east-2.elasticbeanstalk.com/api/v1/)

## Built With
- python/djangorestframework


