import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
import random
import requests
import utils as ut

scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file('client_secret.json', scopes=scope)
client = gspread.authorize(creds)

sheet = client.open("LeetCode Problems Tracker")
worksheet = sheet.get_worksheet(0)
data = worksheet.get_all_records()

user_select = input("Easy, medium, or hard question to review?: ").lower().capitalize()

if (user_select not in ["Easy", "Medium", "Hard"]):
    print("Invalid difficulty level. Please try again.")
    exit()

chosen_question = ut.getRandomQuestion(pd.DataFrame(data), user_select)

# Make an API call to get more info about question:
title_slug = ut.convertToSlug(chosen_question)

api_URL = f"https://alfa-leetcode-api.onrender.com/select?titleSlug={title_slug}"

response = requests.get(api_URL)

if response.status_code == 200:
    problem_data = response.json() # raw API response data
    ut.getProblemData(problem_data, worksheet)



else:
    print(f"Error Code: {response.status_code}")