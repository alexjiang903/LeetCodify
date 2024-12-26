import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
import requests
import utils as ut


scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file('client_secret.json', scopes=scope)
client = gspread.authorize(creds)

sheet = client.open("LeetCode Problems Tracker")
worksheet = sheet.get_worksheet(0)
data = worksheet.get_all_records()
pandasDataframe = pd.DataFrame(data) # All worksheet data in a pandas dataframe
all_languages = pandasDataframe["Language"].unique()
all_difficulties = pandasDataframe["Difficulty"].unique()


print("\nWelcome to Leetcodify!")
print("What question would you like to review today?")
print("\nThe current languages and difficulties available are:\n")
# Print out all available languages and difficulties tracked in the worksheet
print(f"Languages: {', '.join(all_languages)}")
print(f"Difficulties: {', '.join(all_difficulties)}\n")

user_select_diff = input("Easy, medium, or hard question to review?: ").lower().capitalize()

if (user_select_diff not in ["Easy", "Medium", "Hard"]):
    print("Invalid difficulty level entered. Please try again.\n")
    exit()

user_select_lang = input("What language do you want to review?: ").lower().capitalize()
chosen_question = ut.getRandomQuestion(pandasDataframe, user_select_diff, user_select_lang)

# Make an API call to get more info about question:
title_slug = chosen_question.lower().replace(' ', '-')
api_URL = f"https://alfa-leetcode-api.onrender.com/select?titleSlug={title_slug}"

response = requests.get(api_URL)

if response.status_code == 200:
    problem_data = response.json() # raw API response data
    if not problem_data:
        print("Error occurred in fetching problem data. Please try again.\n")
        exit()
    ut.getProblemData(problem_data, worksheet)

elif response.status_code == 429:
    print("\nLeetCode API is busy. Please try again later.")
    try:
        print(f"Response body:{response.text}\n")
    except Exception as e:
        print(f"Error getting details: {e}\n")
        print(response)

    exit()

else:
    print(f"Error code encountered: {response.status_code}\n")
    exit()