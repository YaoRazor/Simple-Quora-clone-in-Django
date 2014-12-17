
# Simple-Quora-clone-in-Django

## Overview

This is a clone of Quora using Django framwork. <br/>
Currently in beta


## Versions

### [0.6] 
- Requriment 1, 2, 3, 4, 8, 9 completed

### [0.7] 
- Requriment 5 completed
- You can add tags to your questions and click on a specific tag will give you all the questions that have the tag sorted by the   question publication time
- 

### [1.0]
- All requirements are completed with some additional function implemented for fun
- 

## Design

### Project architecture
This project is designed using Django and deployed to Heroku cloud platform using PostGreSQL as the database to store data. 
Under the top-level folder of the project, there are three apps. Polls app is the core function of this project, Authentication app is used to handle the user registration and login. Smarturlize app is used to detect the hyperlink in text. Django-photologue app is integrated to provide the photos and gallerys function. 

Project basically is developed purely in Django, using interface proviede by Heroku to deply

### Polls App
This app is developed using Django's MVC pattern. Templates folder store the view of the page, urls.py is servelet dispacher, views.py is the controller, models.py stores the data model. All templates inherit base template to provide consistent ui. Static fiels are stored in public/static folder. Media files are stored in public/media folder.


### Functions
Basically, all the 10 requirements are implemented. The usage of these functions are pretty straightforward. If you have problem testing the function, please inform me!
Additional function
1. In the question list page, I displayed the number of answers of this question.
2. In the Image upload module, you can track your activity
3. When you click a tag, all the related questions will be displayed in order of creation time


## Instruction

### How to use

before you can create or answer questions, you need an account. With no account, you can only view questions.
I have one for you. 

As always, you can register you own username

#### Home page (http://shielded-escarpment-9491.herokuapp.com/polls/)
Feel free to register an account and play


## Thanks
- Professor Jeffery Korn
- Grader LiangFang and Shancong Fu

