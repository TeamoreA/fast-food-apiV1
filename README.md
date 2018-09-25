# orders-api

 ###### This is an API having endpoints to get a list of all order items, get a singe order item by specifying its id, update an order item and finally can delete the order item .


[![Build Status](https://travis-ci.com/TeamoreA/fast-food-apiV1.svg?branch=fixes-160551023)](https://travis-ci.com/TeamoreA/fast-food-apiV1)
[![Test Coverage](https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/test_coverage)](https://codeclimate.com/github/codeclimate/codeclimate/test_coverage)
[![Maintainability](https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/maintainability)](https://codeclimate.com/github/codeclimate/codeclimate/maintainability)


## Aimed Functionalities Endpoints 
- A user can view all orders
- A user can view a specific order.
- A user can create an order.
- A user can update an order.
- A user can delete an order.


## How to use locally

- Clone the repo [HERE](https://github.com/TeamoreA/fast-food-apiV1).
- Install all the depedencies in requirements.txt
`pip install -r requirements.txt`
- Create a virtual environment
- Export this in your .env file
 ```
  source venv/Scripts/activate
  export FLASK_APP = 'run.py'
  export SECRET = 'Your url goes here'
  export FLASK_ENV = 'development'
  export DATABASE_URL = "Your database url goes here"
```
- In the project folder run `flask run`


## How to use it

- After the above installations use post man to test the following end-points
    ##In order to start you must be reqistered run the POST method with route - `/api/v1/users`
    ##The login to get the x-acces-token for authorization with GET method wit route - `/api/v1/login`
    ##To see all users run the GET route - `/api/v1/users`
    ##To see one user run the GET route - `/api/v1/users/<int:user_id>`
    ##To update one user run the PUT route - `/api/v1/orders/<int:user_id>`
    ##To see all orders run the GET route - `/api/v1/orders`
    ##To see one order run the GET route - `/api/v1/orders/<int:order_id>`
    ##To create an order run the POST route - `/api/v1/orders`
    ##To update an order run the PUT route - `/api/v1/orders/<int:order_id>`
    ##To delete an order run the DELETE route - `/api/v1/orders/<int:order_id>`
    
## Sample screenshots
 
