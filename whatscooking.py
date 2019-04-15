##################################
# What's Cooking
# 
# Keith Miller
# April 9th,2019
#
# developed using Python 3.7.3

''' A lightweight app to help figure out what's for dinner.  
Enter a list of ingredients and What's Cooking will return the 
most popular recipe that uses all those ingredients.
The app then returns all of the other ingredients required to make the
chosen recipe. If a required ingredient matches two or more of the 
recipe ingredients, an additional list is generated to warn the user
about the duplicates
'''
from requests import get
from re import search,sub
from pathlib import Path
from html import unescape


RECIPE_SEARCH_URL = 'https://www.food2fork.com/api/search'
RECIPE_DETAIL_URL = 'https://www.food2fork.com/api/get'
# regex for matching user ingredients to recipe ingredients
RECIPE_REGEX = r"( |^|\,){}(s|(es))?(\,|$| )"
# Translation table for filtering punctuation out of recipe ingredients
# for better matching
PUNCTUATION = str.maketrans("","","!\"#$%&'()*+-./:;<=>?@[\]^_`{|}~")


def fetch_API_key(path):
    #retrieve API key from config.txt
    try:
        f=open(Path(path/"config.txt"),mode='r')
    except:
        print("\nNo key file found.\n"
              "Please contact the developer. keithdkm@gmail.com")
        quit()
    else:
        user_key = f.read()
        f.close()
        return user_key

def clean_text(dirty_word):
    # Accepts a string and removes superfluous whitespace 
    # characters and punctuation and makes it lowercase
    clean_word = " ".join(dirty_word.split()).translate(PUNCTUATION).lower()
    
    return clean_word  


def get_user_ingredients(): 
    #accepts user required ingredients at the command line      
    entered_ingredients = input(
        "\nPlease list ingredients you're starting with,"
        "separated by a comma: ")

    # clean up and list entered ingredients 
    entered_ingredients_clean = [clean_text(ingredient) for ingredient 
                                in entered_ingredients.split (",")]
      
    return entered_ingredients_clean


def retrieve_best_recipe(api_key,target_ingredients):
    # returns the recipe_id from foodtofork or 
    # prints error message and returns null if no recipe is found
    # or an error occurs
    search_for = {"key": api_key, 
                  "q": ",".join(target_ingredients), 
                  "sort": "r"}
    
    try:
        recipe_list = get(RECIPE_SEARCH_URL, 
                          params=search_for,timeout=5) 
                
    except:
        # handle site down or internet down errors        
        print("\nLooks like the recipe server is unavailable. "
              "Either the site is down or "
              "you don't have an internet connection\n")       
        quit()
    else:
        if recipe_list.ok:                                 
            if list(recipe_list.json().keys())[0] == 'count':        
            # Checks that site has returned recipes rather than an error
                if recipe_list.json()["count"] > 0:
                    # if recipes were found, 
                    # retrieve recipe_id of first recipe on list 
                    best_recipe = recipe_list.json()["recipes"][0]["recipe_id"] 
                    return (best_recipe)                 
                else:    
                    print ("\nThere were no recipes that"
                           " included all your ingredients\n")
                    return 
            else:          
                print ("\nYou have exceeded your daily"
                       " maximum number of queries\nGoodbye")      
                quit()
        else: 
            # handle error codes from server    
            print(
                "\nServer returned error {}\n".format(recipe_list.status_code))
            return


def retrieve_recipe_ingredients(api_key, recipe_id):
    # returns all of the ingredients listed for a specific recipe id
    search_for = {"key":api_key,
                  "rId":recipe_id}
    try:
        recipe_detail = get(RECIPE_DETAIL_URL, params=search_for, timeout=5)  
    except:
        # handle site down or internet down errors
        print("\nLooks like the recipe server is unavailable. "
              "Either the site is down or you don't" 
              "have an internet connection\n")      
        quit()   
    else:
        if recipe_detail.ok:            
            if list(recipe_detail.json().keys())[0] == 'recipe':
            # check that food2fork returned a recipe and not an error     
                if recipe_detail.json() == []:
                    # catches empty recipes.  Unlikely error
                    print ("\nSorry, there were no recipes"
                           " that included all of your ingredients\n")           
                    return
                else:    
                    recipe_ingredients = recipe_detail.json()["recipe"]["ingredients"]     
                    recipe_name = recipe_detail.json()["recipe"]["title"]  
            else:
                print ("\nYou have exceeded your daily"
                       " maximum number of queries\nGoodbye")      
                quit()                                  
        else: 
            # handle error codes from server      
            print("\nServer returned error {}\n".format(
                                                     recipe_detail.status_code))  
            return
    
    
        # remove the new line character appended to last returned ingredient                          
        recipe_ingredients[-1] = recipe_ingredients[-1].rstrip("\n")                       
        return (recipe_name,recipe_ingredients)


def recommend_recipe(recipe_name):
    
    # used html.unescape to properly display apostrophes
    print("{:<80}".format("\n\nWhat's Cooking today is {},"
          "which is the most popular recipe " 
          "using all of your ingredients").format(unescape(recipe_name))
     )


def you_need_list(target_ingredients,recipe_ingredients):
    
    ingredients_needed = [ingredient for ingredient in recipe_ingredients 
                         if not any([search(
                                    RECIPE_REGEX.format(target_ingredient),
                                    clean_text(ingredient))
                                    for target_ingredient in 
                                        target_ingredients])]
    
    
    print("\nTo make this recipe, you will need the following additional "
          "ingredients: \n")
    
    for i,ingredient in enumerate(ingredients_needed):
            print("{}. {}".format(i+1,unescape(ingredient)))           
    
    
def you_may_need_list(target_ingredients,recipe_ingredients):    
    you_may_need = []
    # For each user ingredient, see it if matches more than one item in    
    # the recipe ingredients list. If so add all those items
    # to a "you may need" list
    for target_ingredient in target_ingredients:
        # Match each ingredient in the user ingredient list to one or more 
        # ingredients in selected recipe 
        #       
        # Regex ensures whole string matches only and accommodates 
        # most plurals
        ingredient_matches = ([ingredient for ingredient in recipe_ingredients 
                              if search(RECIPE_REGEX.format(target_ingredient),
                              clean_text(ingredient))!=None])
        if len(ingredient_matches)>1: 
            you_may_need.append(ingredient_matches)
        # If there is more than one ingredient match, 
        # add all matched ingredients to "You may need list"
  
    if you_may_need: 
        print("\nSome of your required ingredients matched 2 "
              "or more recipe ingredients, so you may also need:")
        
        for i,duplicate_matches in enumerate(you_may_need):
            print("{}. ".format(i+1),end=" ")
            [print("{}  OR  ".format(unescape(duplicate_match)),end=" ") 
                for duplicate_match in duplicate_matches[:-1]]
            print("{}.".format(unescape(duplicate_matches[-1])))

           
##########################################################################

print("\n\n")        
print("{:^80}".format("Welcome. This is What's Cooking"))

user_key = fetch_API_key(Path(__file__).resolve().parent) 
# fetches food2fork API key from the config.txt - system independent

print("{:^80}".format("Here to help you decide what's for dinner " 
                       "tonight and tell you what you need to buy "
                       "to make it happen"))

while True:
    
    user_ingredients = get_user_ingredients()
    
    best_recipe_id = retrieve_best_recipe(user_key,user_ingredients)    
    if best_recipe_id:
        # if a suitable recipe was found, retrieve its name and ingredients
        best_recipe_name,all_ingredients = retrieve_recipe_ingredients(
                                                                user_key,
                                                                best_recipe_id)
        recommend_recipe(best_recipe_name)
        you_need_list(user_ingredients,all_ingredients)
        you_may_need_list(user_ingredients,all_ingredients)
