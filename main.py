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

all_q_df = pd.DataFrame(data) # Data frame of all questions completed so far

question_bank = []
question_col = all_q_df["Problem Name"] # Column containing names of all all past LC questions done 

for i in range(len(question_col)):
    question_bank.append(question_col[i])

chosen_question = ""
random_idx = random.randint(0, len(question_bank) - 1)
chosen_question = question_bank[random_idx]

print(f"The question to review will be : {chosen_question}")


# Make an API call to get more info about question:
title_slug = ut.convertToSlug(chosen_question)

api_URL = f"https://alfa-leetcode-api.onrender.com/select?titleSlug={title_slug}"

response = requests.get(api_URL)


if response.status_code == 200:
    problem_data = response.json() # raw API response data
    print(f"Link to question: {problem_data['link']}")
    print(f"Difficulty: {problem_data['difficulty']}")

    q_tags = problem_data['topicTags'] # Array of tags from API response
    relevant_topics = []

    for item in q_tags:
        relevant_topics.append(item["name"])

    print(f"Question Topics: {relevant_topics}")

else:
    print(f"Error Code: {response.status_code}")







