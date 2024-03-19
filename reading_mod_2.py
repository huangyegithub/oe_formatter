import pandas as pd
import numpy as np

def rhyming_words(dataframe):
    dataframe = dataframe.iloc[:, 4:]
    results = dataframe.fillna(0)
    results = results.replace(to_replace='[^0]', value=1, regex=True).infer_objects()
    return results.astype(int)

def letter_recognition_upper_case(dataframe):
    dataframe = dataframe.iloc[:, 6:]
    results = dataframe.fillna(0)
    results = results.replace(to_replace='[^0]', value=1, regex=True).infer_objects()
    return results.astype(int)

def letter_recognition_lower_case(dataframe):
    dataframe = dataframe.iloc[:, 6:]
    results = dataframe.fillna(0)
    results = results.replace(to_replace='[^0]', value=1, regex=True).infer_objects()
    return results.astype(int)

def ick_words(dataframe):
    dataframe = dataframe.iloc[:, 4:]
    results = dataframe.fillna(0)
    results = results.replace(to_replace='[^0]', value=1, regex=True).infer_objects()
    return results.astype(int)

def the_beach_ball(dataframe):
    dataframe = dataframe.iloc[:, [4, 6, 12, 16, 20, 24, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]]
    results = dataframe.fillna(0)
    results = results.replace(to_replace='[^0]', value=1, regex=True).infer_objects()
    return results.astype(int)


def the_lunch_boxes(dataframe):
    dataframe = dataframe.drop(dataframe.columns[[0, 1, 2, 3, 11]], axis=1)
    results = dataframe.fillna(0)
    
    for index, row in results.iterrows():
        if row.iloc[3] == "l" or row.iloc[3] == "ü": results.at[index, results.columns[3]] = 2
        elif row.iloc[4] == 'l' or row.iloc[4] == "ü": results.at[index, results.columns[3]] = 1
        elif row.iloc[5] == 'l' or row.iloc[5] == "ü": results.at[index, results.columns[3]] = 0
    results = results.replace(to_replace='ü', value=1, regex=True).infer_objects()
    results = results.drop(results.columns[[4,5]], axis=1)
    return results.astype(int)


def reading_mod_2(excel_data):
    # Assign worksheets to relevant variables.
    RHYMING_WORDS = excel_data["RHYMING WORDS"]
    LETTER_RECOGNITION_UPPER_CASE = excel_data["LETTER RECOGNITION_Upper case"]
    LETTER_RECOGNITION_LOWER_CASE = excel_data["LETTER RECOGNITION_Lower case"]
    ICK_WORDS = excel_data["ICK WORDS"]
    THE_BEACH_BALL = excel_data["THE BEACH BALL"]
    THE_LUNCH_BOXES = excel_data["THE LUNCH BOXES"]


    # Remove rows with the 2nd column containing NaN.
    RHYMING_WORDS = RHYMING_WORDS.dropna(subset=[RHYMING_WORDS.columns[1]]).reset_index().iloc[:, 1:]
    LETTER_RECOGNITION_UPPER_CASE = LETTER_RECOGNITION_UPPER_CASE.dropna(subset=[LETTER_RECOGNITION_UPPER_CASE.columns[1]]).reset_index().iloc[:, 1:]
    LETTER_RECOGNITION_LOWER_CASE = LETTER_RECOGNITION_LOWER_CASE.dropna(subset=[LETTER_RECOGNITION_LOWER_CASE.columns[1]]).reset_index().iloc[:, 1:]
    ICK_WORDS = ICK_WORDS.dropna(subset=[ICK_WORDS.columns[1]]).reset_index().iloc[:, 1:]
    THE_BEACH_BALL = THE_BEACH_BALL.dropna(subset=[THE_BEACH_BALL.columns[1]]).reset_index().iloc[:, 1:]
    THE_LUNCH_BOXES = THE_LUNCH_BOXES.dropna(subset=[THE_LUNCH_BOXES.columns[1]]).reset_index().iloc[:, 1:]

    output_data = RHYMING_WORDS.iloc[:, :3]

    output_data = pd.concat([output_data, rhyming_words(RHYMING_WORDS)], axis=1, ignore_index=True)
    output_data = pd.concat([output_data, letter_recognition_upper_case(LETTER_RECOGNITION_UPPER_CASE)], axis=1, ignore_index=True)
    output_data = pd.concat([output_data, letter_recognition_lower_case(LETTER_RECOGNITION_LOWER_CASE)], axis=1, ignore_index=True)
    output_data = pd.concat([output_data, ick_words(ICK_WORDS)], axis=1, ignore_index=True)
    output_data = pd.concat([output_data, the_beach_ball(THE_BEACH_BALL)], axis=1, ignore_index=True)
    output_data = pd.concat([output_data, the_lunch_boxes(THE_LUNCH_BOXES)], axis=1, ignore_index=True)

    score_sum = output_data.iloc[:, 3:].sum(axis=1)
    output_data['Score'] = score_sum
    scale_score = output_data.pop(2)
    output_data['Scale'] = scale_score

    first_names = output_data.iloc[:, 0].tolist()
    last_names = output_data.iloc[:, 1].tolist()
    student_marks = output_data.iloc[:, 2:].values.tolist()
    
    return first_names,last_names,student_marks

