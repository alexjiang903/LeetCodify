# API Key: AIzaSyCO8XFcVSocbx4ZEkkX6UiqqClitvq1Lpo

# API endpoint: https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{SHEET_NAME}!A1:Z?alt=json&key={API_KEY}

SHEET_ID = "15DI1H9-EqIZ2KEXeIguB98tmE3vQECJEVUZOnU6AQRE"
SHEET_NAME = "LeetCode%20Problems%20Tracker"
API_KEY = "AIzaSyCO8XFcVSocbx4ZEkkX6UiqqClitvq1Lpo"

print(f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{SHEET_NAME}!A:Z?alt=json&key={API_KEY}")

import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials










