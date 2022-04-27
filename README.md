# dargs-monorepo

![IUB Logo](https://www.pngkit.com/png/full/245-2457689_iub-independent-university-bangladesh-logo.png)

# Project
Final course project for Database Management course.

# Project Structure

This repo contains two seperate applications. 
+ dargs-backend
+ dargs-frontend

`dargs-frontend` is written in python while the `dargs-backend` is forked from a nextJS template. The .gitignore file file has works for both python and node. 

# Directory Structure


    .
    ├── dargs-backend                        
    |   |─── assets                         # .csv assets here
    |   |─── dargs                          # dargs app 
    |   |─── db_project                     # django entrypoint
    |   |─── seed.py                        # seed script for db
    |   └─── docker-compose.yml             # docker file for initiating the db
    |── dargs-frontend
    |    └─── src
    |        |───api
    |        |    └───index.js              # API response formating      
    |        └───views                   
    |             └───analysis              # react components for 5 analysis 
    |                   |───analysis_1
    |                   |───analysis_2
    |                   |───analysis_3
    |                   |───analysis_4
    |                   |───analysis_5
    |                   └───analysis_6
    └── ...

# Installation
 + ## dargs-backend
    ```
    #initiates a mariaDB instance on localhost:3306
    docker-compose up -d                        
    ```
    ```
    #Create a python Virtual Environment
    python -m venv venv
    ```
    ```
    .\venv\Scripts\activate
    ```
    ```
    pip install -r requirements.txt
    ```
    ```
    #stages db migrations
    python manage.py migrate
    ```
    ```
    #appends any migrations
    python manage.py migrate
    ```
    ```
    #not mandatory, initiates database from tally sheets in ./assets folder. Expected name for tally sheets, "Tally <SEMESTER> <YEAR>.csv" in standard IUB Tally Sheet format.
    python seed.py             
    ```
    ```
    #Start the backend server
    python manage.py runserver
    ```
+ ## dargs-front-end
    ```
    npm install
    ```
    ```
    npm start
    ```