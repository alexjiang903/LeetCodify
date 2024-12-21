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

user_select_diff = input("Easy, medium, or hard question to review?: ").lower().capitalize()

if (user_select_diff not in ["Easy", "Medium", "Hard"]):
    print("Invalid difficulty level entered. Please try again.")
    exit()

user_select_lang = input("What language do you want to review?: ").lower().capitalize()

chosen_question = ut.getRandomQuestion(pd.DataFrame(data), user_select_diff, user_select_lang)

# Make an API call to get more info about question:

title_slug = chosen_question.lower().replace(' ', '-')
api_URL = f"https://alfa-leetcode-api.onrender.com/select?titleSlug={title_slug}"

response = requests.get(api_URL)

if response.status_code == 200:
    problem_data = response.json() # raw API response data
    ut.getProblemData(problem_data, worksheet)

elif response.status_code == 429:
    print("LeetCode API is busy. Please try again later.")
    try:
        print("Response body:", response.text)
    except Exception as e:
        print("Error getting details:", e)
        print(response)

    exit()

else:
    print(f"Error code encountered: {response.status_code}")
    exit()