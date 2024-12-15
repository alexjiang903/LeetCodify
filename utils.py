# All utility/helper functions are located here
import pandas as pd
import random

def convertToSlug(title):
    return title.lower().replace(' ', '-')

def getRandomQuestion(all_q_df):
    question_col = all_q_df["Problem Name"] # Column containing names of all all past LC questions done 
    question_bank = []
    for i in range(len(question_col)):
        question_bank.append(question_col[i])

    chosen_question = ""
    random_idx = random.randint(0, len(question_bank) - 1)
    chosen_question = question_bank[random_idx]

    print(f"The question to review will be : {chosen_question}")
    return chosen_question



def getProblemData(problem_data):
    print(f"Link to question: {problem_data['link']}")
    print(f"Difficulty: {problem_data['difficulty']}")

    q_tags = problem_data['topicTags'] # Array of tags from API response
    relevant_topics = []

    for item in q_tags:
        relevant_topics.append(item["name"])

    print(f"Question Topics: {relevant_topics}")


