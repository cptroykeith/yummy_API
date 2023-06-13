[![CircleCI](https://dl.circleci.com/status-badge/img/gh/cptroykeith/yummy_API/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/cptroykeith/yummy_API/tree/main)
[![Coverage Status](https://coveralls.io/repos/github/cptroykeith/yummy_API/badge.svg?branch=main)](https://coveralls.io/github/cptroykeith/yummy_API?branch=main)

# YUM RECIPES FLASK-API

A Flask API for the Yum-Recipes that handles:

  * User authentication
  * Creating, reading, updating and deleting of categories
  * Creating, reading, updating and deleting of recipes
  
 ### To get started:
 #### 1. clone the repository.  
   In your root directory create a virtual environment using the virtualenv tool:  
   We will create a virtual environment for handling our dependencies  
   
   ```
    $ pip install virtualenv  
    $ virtualenv <environment-name>  
   ```  
   Then navigate into the environment youve created and activate scripts:    
    e.g. If my environment is called env. I would do something like this.  
    
   ```   
    $ cd env   
    $ Scripts\activate   
    $ cd ..   
   ```   
    
 #### 2. Next you'll want to install the dependencies:  
   
   for windows use:   
    
   ```
    $ pip install -r requirements.txt
   ```   
   for mac or linux use:   
    
   ```
    $ pip3 install -r requirements.txt
   ```   
   
 #### 3. Next we'll create a database and run migrations:  
   
   ```   
    
    $ flask db init    
    $ flask db migrate   
    $ flask db upgrade   
    
   ```    
  #### 4. Envirnoment variables:   
  
  create a file with the .env extention within the root directory and paste the following lines of code   
  ```
  FLASK_DEBUG = 1   
  FLASK APP = app
  ```   
  
  #### 5.  run the app:   
        
   ```  
   $ py run.py
   ```   
   or   
   ```
   $ python server.py
   ```   
   #### 6. View the swagger UI documentation:   
   After starting the server, paste this url in a browser of your choice    
   ```
   http://localhost:8080/apidocs
   ```   
   
  
   
