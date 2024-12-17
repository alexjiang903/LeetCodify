# All utility/helper functions are located here
import pandas as pd
import random

def convertToSlug(title):
    return title.lower().replace(' ', '-')

def getRandomQuestion(all_q_df, diff):
    df = all_q_df[['Problem Name', 'Difficulty']]
    
    # Filter data frame by difficulty selected
    df_filtered = df.query('Difficulty == @diff')    
  
    chosen_question = df_filtered["Problem Name"].sample(1).iloc[0] #Randomly sample one question from data frame
    print(f"The question to review will be : {chosen_question}")
    return chosen_question


def getProblemData(problem_data):
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

        

