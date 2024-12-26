# All utility/helper functions are located here
import pandas as pd
import gspread
import random
from datetime import datetime
import json
import os


with open('formats.json', 'r') as file:
    formats = json.load(file) # Formatting for writing to Google Sheets

def getRandomQuestion(all_q_df, diff, lang):
    os.system('clear')
    df = all_q_df[['Problem Name', 'Difficulty', 'Language']]
    all_languages = all_q_df["Language"].unique()
    all_languages = [x.lower() for x in all_languages]
    
    is_valid_lang = lang.lower() in all_languages
    is_valid_diff = diff in df['Difficulty'].unique()   
    
    if not (is_valid_lang and is_valid_diff):
        lang = lang if (lang != "Javascript" and lang != "Typescript") else ("JS" if lang == "Javascript" else "TS")
        print(f"\nYou have not done any questions with language {lang} and difficulty {diff} so far!\n")
        exit()
        
    # Filter data frame by difficulty selected
    
    if (lang == "Javascript" or lang == "Typescript"):
        lang = lang.replace("s", "S") #edge case for JS/TS where the first letter isn't the only one capitalized

    
    df_filtered = df.query('Difficulty == @diff and Language == @lang')    
    
    if (df_filtered.empty):
        lang = lang if (lang != "JavaScript" and lang != "TypeScript") else ("JS" if lang == "JavaScript" else "TS")
        print(f"\nNo matching questions found with {lang} and difficulty {diff}.\n")
        exit()

    chosen_question = df_filtered["Problem Name"].sample(1).iloc[0] #Randomly sample one question from data frame
    print(f"\nThe question to review will be: {chosen_question}")
    return chosen_question


def getProblemData(problem_data, sheet_ref):
    if 'link' not in problem_data:
        print(f"Link to problem could not be found.")
        print(f"Problem data recieved: {problem_data}\n")
        exit()
    
    else:
        print(f"\nLink to question: {problem_data['link']}")
        print(f"Difficulty: {problem_data['difficulty']}")

        q_tags = problem_data['topicTags'] # Array of tags from API response
        relevant_topics = [item.get("name", "") for item in q_tags if "name" in item] 
        
        print(f"Question Topics: {', '.join(relevant_topics)}")

        trackLastReview(problem_data["questionTitle"], sheet_ref) # sheet_ref is the worksheet containing all tracked questions


def trackLastReview(q_name, sheet_ref):
    # will write to sheet and add last review date column
    sheet_data = sheet_ref.get_all_records()
    df = pd.DataFrame(sheet_data)

    '''
        if 'Most Recent Review' not in df.columns:
        print("this shouldn't get triggered anymore... (Most Recent Review already exists in the sheet)")
        df['Most Recent Review'] = None #initialize column if last review date missing
        sheet_ref.update_acell("J1", "Most Recent Review")
        sheet_ref.format('J1', formats["header_format"])
     
    '''   
  
    # Find the corresponding question:
    current_date = datetime.now().strftime("%Y-%m-%d")

    print(f"\nSearching for {q_name}...")
    
    row_index = df.query(' `Problem Name` == @q_name ').index

    if not row_index.empty:
        df.at[row_index[0], 'Most Recent Review'] = current_date 

        # Write the data back to the sheet (insert/add to "Most Recent Review" column) 
        sheet_ref.update_acell(f"J{row_index[0] + 2}", current_date)
        sheet_ref.format(f"J{row_index[0] + 2}", formats["text_entry_format"])
        print(f"Successfully updated last review date {current_date} for {q_name}\n")
    else:
        print("Error, row index not found.\n")
        exit()
        