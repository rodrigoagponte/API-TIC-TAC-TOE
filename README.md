# API Project - Tic Tac Toe

This project was proposed to me by my new company as the onboarding project.
It consists of the application of a game of Tic Tac Toe which is played via HTTP Requests.


# Endpoints

Here you can find the available endpoints for the **API Project - Tic Tac Toe**.\
For each endpoint, you will find the URL, the allowed HTTP method, the request body (if needed), and the authType (if needed).

## Index

##### /

##### GET

<br/>

## Register

##### /auth/register/

##### POST

##### {"username": _username_, "password": _password_, "email": _email_}

<br/>

## Log in

##### /auth/login/

##### POST

##### {"username": _username_, "password": _password_}

<br/>

## Log out

##### /auth/logout/

##### GET

##### authType: Bearer _TOKEN_ \*

<br/>

## Get Stats

##### /tictactoe/

##### GET

##### authType: Bearer _TOKEN_

<br/>

## Get All Games

##### /tictactoe/games/

##### GET

##### authType: Bearer _TOKEN_

<br/>

## Get One Game

##### /tictactoe/games/`game_id`/

##### GET

##### authType: Bearer _TOKEN_

<br/>

## Create Game

##### /tictactoe/games/create/

##### POST

##### authType: Bearer _TOKEN_


<br/>

## Join Game

##### /tictactoe/games/`game_id`/join/

##### PATCH

##### authType: Bearer _TOKEN_

<br/>

## Play Game

##### /tictactoe/games/`game_id`/play/

##### POST

##### authType: Bearer _TOKEN_

<br/>