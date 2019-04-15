# Welcome to What's Cooking
 A lightweight app to help you figure out what's for dinner.  
Enter all of the ingredients you want and the app will find the most popular 
recipe that uses all of those ingredients and  will list all of the other 
ingredients required to make the that recipe. 

If a required ingredient matches two or more of the 
recipe ingredients, an additional list is generated to warn the user
about the duplicates.

## One-time Installation and Setup
1. Clone the What's Cooking repository to a your chosen target directory. A new directory called Whats-Cooking will be created in there
1. Open the email that you received from me with the subject line What's Cooking.
1. Save the "config.txt" file attached to that email into your new What's Cooking directory created in Step 1. This file contains the API key for food2fork.com and the app will not run without it
1. Open a terminal window and activate the Python environment into which you wish to install What's Cooking
1. Change directory the Whats-Cooking directory in step 1 and enter "pip install -r requirements.txt" to install all of the dependencies required by What's Cooking into your chosen environment.


## Running What's Cooking
1. Navigate to the Whats-Cooking directory and enter python whatscooking.py at the command line.

## Using What's Cooking
1. At the prompt, enter as many ingredients as you wish. Be as specific as you can for the best results
1. What's Cooking will recommend a recipe and follow it with a list of the rest of the ingredients
1. If the any of the required ingredients match more than one recipe ingredient, an additional list is generated to warn you that you may also have to buy those items as well.   

