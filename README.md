# Mock Drive Thru

A mock drive thru ordering system that allows users to place and cancel their orders using AI.

The user will input the order details in natual language.
The user can opt to order the following items 
1. Burgers
2. Fries
3. Drinks. 

The user will be able to see the order history and the counter for total number of burgers, fries, and drinks.

Example:
User enters "I would like to order a burger and fries" -> an order of 1 burger and 1 fries will be created and the burger count and fries count will be updated.

# Setup

See backend/README.md and frontend/README.md for setup instructions

## Frontend
To setup the frontend navigate to the frontend directory and run the following commands:
1. npm install
2. npm run dev

## Backend
To setup the backend navigate to the backend follow the steps below. 
1. Create a virtual environment. [python3 -m venv myvenv]
2. Activate the virtual environment. [source myvennv/bin/activate]
3. Install all dependencies. [Run command: poetry install] 
4. Create an env variable to hold the Open AI API key [export OPEN_AI_API_KEY = "your_key"]
4. Finally run the app using the following command: poetry run python main.py

# Demo

Here is a small demo of the app. 

Demo1: Placing an order.

[![Demo1](https://github.com/user-attachments/assets/d4dfbb56-526a-47f0-bd45-34613f693919.jpeg)](https://github.com/user-attachments/assets/d4dfbb56-526a-47f0-bd45-34613f693919)


Demo2: Cancelling the order. 
https://github.com/user-attachments/assets/21afb10c-4b23-43da-8d0e-872994107ec8


