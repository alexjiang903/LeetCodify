import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
import random


scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file('client_secret.json', scopes=scope)
client = gspread.authorize(creds)

sheet = client.open("LeetCode Problems Tracker")
worksheet = sheet.get_worksheet(0)
data = worksheet.get_all_records()


all_q_df = pd.DataFrame(data) # Data frame of all questions completed so far

question_bank = []

all_qs = all_q_df["Problem Name"]# Names of all past LC questions done 

for i in range(len(all_qs)):
    question_bank.append(all_qs[i])

# print(question_bank)
chosen_question = ""

random_idx = random.randint(0, len(question_bank) - 1)
chosen_question = question_bank[random_idx]

print(f"The question to review will be : {chosen_question}")



#print(data)








