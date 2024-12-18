# All utility/helper functions are located here
import pandas as pd
import gspread
import random
from datetime import datetime
# initial commit to publish branch

def convertToSlug(title):
    return title.lower().replace(' ', '-')

def getRandomQuestion(all_q_df, diff):
    df = all_q_df[['Problem Name', 'Difficulty']]
    
    # Filter data frame by difficulty selected
    df_filtered = df.query('Difficulty == @diff')    
  
    chosen_question = df_filtered["Problem Name"].sample(1).iloc[0] #Randomly sample one question from data frame
    print(f"The question to review will be : {chosen_question}")
    return chosen_question


def getProblemData(problem_data, sheet_ref):
    if 'link' not in problem_data:
        print("No link found!")
    
    else:
        print(f"Link to question: {problem_data['link']}")
        print(f"Difficulty: {problem_data['difficulty']}")

        q_tags = problem_data['topicTags'] # Array of tags from API response
        relevant_topics = []

        for item in q_tags:
            relevant_topics.append(item["name"])

        print(f"Question Topics: {relevant_topics}")

        trackLastReview(problem_data["questionTitle"], sheet_ref) #sheet_ref is the worksheet containing all tracked questions


def trackLastReview(q_name, sheet_ref):
    # will write to sheet and add last review date column
    sheet_data = sheet_ref.get_all_records()
    df = pd.DataFrame(sheet_data)

    if 'Most Recent Review' not in df.columns:
        df['Most Recent Review'] = None #initialize column if last review date missing
    
    # Find the corresponding question:
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    row_index = df.query(' `Problem Name` == @q_name ').index

    if not row_index.empty:
        df.at[row_index[0], 'Most Recent Review'] = current_date 
        print(f"Successfully updated last review date {current_date} for {q_name}")
        # Write the data back to the sheet (WIP)

    else:
        print("Error, row index not found.")
        

    

    
    

    

    








