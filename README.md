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

## How to use it

- Clone the repo [HERE](https://github.com/TeamoreA/fast-food-apiV1).
- Install all the depedencies in requirements.txt
- Run the file orders.py (python orders.py)
- Using Postman app to test the endpoints
    ##In order to start you must be reqistered run the POST method with route - /api/v1/users
    ##The login to get the x-acces-token for authorization with GET method wit route - /api/v1/login
    ##To see all users run the GET route - /api/v1/users
    ##To see one user run the GET route - /api/v1/users/<int:user_id>
    ##To update one user run the PUT route - /api/v1/orders/<int:user_id>
    ##To see all orders run the GET route - /api/v1/orders
    ##To see one order run the GET route - /api/v1/orders/<int:order_id>
    ##To create an order run the POST route - /api/v1/orders
    ##To update an order run the PUT route - /api/v1/orders/<int:order_id>
    ##To delete an order run the DELETE route - /api/v1/orders/<int:order_id>
