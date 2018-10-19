# FAST-FOOD-FAST

 Thanks for choosing this API.This is a simple order management app.This RESTful-api has been written in python and flask.This api enables you to create an order, see all the orders that you have created, getting a specific order, update an order and finally to delete an order.This is the stable version (V1). Follow the guide below on how to use it.

## Badges

[![Build Status](https://travis-ci.com/TeamoreA/fast-food-apiV1.svg?branch=fixes-160551023)](https://travis-ci.com/TeamoreA/fast-food-apiV1)
[![Coverage Status](https://coveralls.io/repos/github/TeamoreA/fast-food-apiV1/badge.svg?branch=develop)](https://coveralls.io/github/TeamoreA/fast-food-apiV1?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/875efc35a9ff3f32e748/maintainability)](https://codeclimate.com/github/TeamoreA/fast-food-apiV1/maintainability)

## Basic requirements
- Python 3


## Version one endpoints 
<table>
  <tr>
    <th>Endpoint</th>
    <th>HTTPS requests</th>
    <th>Functionality</th>
  </tr>
  <tr>
    <td> /api/v1/orders </td>
    <td>GET</td>
    <td>Get all the orderss</td>
  </tr>
  </tr>
  <tr>
    <td> /api/v1/orders/(int:order_id) </td>
    <td>GET</td>
    <td>Get a specific order</td>
  </tr>
  <tr>
    <td> /api/v1/orders </td>
    <td>POST</td>
    <td>Create a new order</td>
  </tr>
  <tr>
    <td> /api/v1/orders/(int:order_id) </td>
    <td>PUT</td>
    <td>Update an order</td>
  </tr>
  <tr>
    <td> /api/v1/orders/(int:order_id) </td>
    <td>DELETE</td>
    <td>Delete an order</td>
  </tr>
</table>

## Version two endpoints 
<table>
  <tr>
    <th>Endpoint</th>
    <th>HTTPS requests</th>
    <th>Functionality</th>
  </tr>
  <tr>
    <td> /api/v2/auth/signup </td>
    <td>POST</td>
    <td>Register a new user</td>
  </tr>
 <tr>
    <td> /api/v2/auth/users/(int:user_id) </td>
    <td>PUT</td>
    <td>Update user details</td>
  </tr>
  </tr>
  <tr>
    <td> /api/v2/auth/signin </td>
    <td>POST</td>
    <td>Login a user</td>
  </tr>
  <tr>
    <td> /api/v2/promote/(int:user_id) </td>
    <td>PUT</td>
    <td>promote a user to admin</td>
  </tr>
  <tr>
    <td> /api/v2/menu </td>
    <td>POST</td>
    <td>Add a food menu</td>
  </tr>
  <tr>
    <td> /api/v2/menu </td>
    <td>GET</td>
    <td>Get a list of all menu items</td>
  </tr>
  <tr>
    <td> /api/v2/orders </td>
    <td>POST</td>
    <td>Create a new food item</td>
  </tr>
  <tr>
    <td> /api/v2/users/orders/(int:user_id) </td>
    <td>GET</td>
    <td>Get users orderlist</td>
  </tr>
  <tr>
    <td> /api/v2/orders </td>
    <td>GET</td>
    <td>Get orderlist</td>
  </tr>
  <tr>
    <td> /api/v2/orders/(int:order_id) </td>
    <td>PUT</td>
    <td>Edit order status</td>
  </tr>
  
</table>


## How to test locally

- Clone the repo [HERE](https://github.com/TeamoreA/fast-food-apiV1).
- cd to project folder `fast-food-apiV1`
- Install virtual environment and activate it
 ```pip install virtualenv
    mkvirtualenv venv
  ```   
- Install all the depedencies in requirements.txt
`pip install -r requirements.txt`
- Create a postgres database named `yourdbname`
- Export this in your .env file
 ```
  source venv/Scripts/activate
  export FLASK_APP='run.py'
  export SECRET='yoursecret'
  export FLASK_ENV='development'
  export DATABASE_URL="dbname='yourdbname' host='127.0.0.1' port='5432' user='postgres' password=''"


```
- Run this in the prompt `source .env`
- In the project folder run `flask run`

## How to run tests to get the code coverage
- Run the following command in the command line `nosetests --with-coverage --cover-erase --cover-package=app/test`
## Hosted app
- The app is hosted at heroku [HERE](https://andela-food-api.herokuapp.com/).
## How to use it

- After the above installations use *POSTMAN* to test the following end-points
    
    - To see all orders run the GET route - `/api/v1/orders`
    ![screenshot 66](https://user-images.githubusercontent.com/29709981/45215245-8a091880-b2a5-11e8-85ba-c0d8f32ef22b.png)
    - To see one order run the GET route - `/api/v1/orders/<int:order_id>`
     ![screenshot 67](https://user-images.githubusercontent.com/29709981/45215266-9b522500-b2a5-11e8-96fa-256cd04fe3db.png)
    - To create an order run the POST route - `/api/v1/orders`
    ![screenshot 68](https://user-images.githubusercontent.com/29709981/45215276-a3aa6000-b2a5-11e8-98b9-4015f78eb547.png)
    - To update an order run the PUT route - `/api/v1/orders/<int:order_id>`
    ![screenshot 69](https://user-images.githubusercontent.com/29709981/45215281-a9a04100-b2a5-11e8-9d8d-d33ffc740a8e.png)
    - To delete an order run the DELETE route - `/api/v1/orders/<int:order_id>`
    ![screenshot 70](https://user-images.githubusercontent.com/29709981/45215293-b58c0300-b2a5-11e8-9c34-ce431663f814.png)

 
