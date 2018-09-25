# orders-api

 ###### This is an API having endpoints to get a list of all order items, get a singe order item by specifying its id, update an order item and finally can delete the order item .


[![Build Status](https://travis-ci.com/TeamoreA/fast-food-apiV1.svg?branch=fixes-160551023)](https://travis-ci.com/TeamoreA/fast-food-apiV1)
[![Coverage Status](https://coveralls.io/repos/github/TeamoreA/fast-food-apiV1/badge.svg?branch=fixes-160551023)](https://coveralls.io/github/TeamoreA/fast-food-apiV1?branch=fixes-160551023)
[![Maintainability](https://api.codeclimate.com/v1/badges/875efc35a9ff3f32e748/maintainability)](https://codeclimate.com/github/TeamoreA/fast-food-apiV1/maintainability)


## Aimed Functionalities Endpoints 
- A user can view all orders
- A user can view a specific order.
- A user can create an order.
- A user can update an order.
- A user can delete an order.


## How to test locally

- Clone the repo [HERE](https://github.com/TeamoreA/fast-food-apiV1).
- cd to project folder `fast-food-apiV1`
- Install virtual environment and activate it
 ```pip install virtualenv
    source venv/Scripts/activate
  ```   
- Install all the depedencies in requirements.txt
`pip install -r requirements.txt`
- Export this in your .env file
 ```
  source venv/Scripts/activate
  export FLASK_APP = 'run.py'
  export SECRET = 'Your url goes here'
  export FLASK_ENV = 'development'
```
- In the project folder run `flask run`


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

 
