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

def cupcakes(dataframe):
    dataframe = dataframe.iloc[:, 4:]
    dataframe = dataframe.iloc[:, [0,2,4,5,6,7,9,10,13,16,20,21]]
    results = dataframe.fillna(0)
    results = results.replace(to_replace='[^0]', value=1, regex=True).infer_objects()
    return results.astype(int)


def clever_max(dataframe):
    dataframe = dataframe.drop(dataframe.columns[[0, 1, 2, 3, 17, 19]], axis=1)
    results = dataframe.fillna(0)
    
    for index, row in results.iterrows():
        if row.iloc[4] == "l" or row.iloc[4] == "ü": results.at[index, results.columns[4]] = 2
        elif row.iloc[5] == 'l' or row.iloc[5] == "ü": results.at[index, results.columns[4]] = 1
        elif row.iloc[6] == 'l' or row.iloc[6] == "ü": results.at[index, results.columns[4]] = 0
    results = results.replace(to_replace='ü', value=1, regex=True).infer_objects()
    results = results.drop(results.columns[[5,6]], axis=1)
    return results.astype(int)


def reading_mod_1(excel_data):
    # Assign worksheets to relevant variables.
    RHYMING_WORDS = excel_data["RHYMING WORDS"]
    LETTER_RECOGNITION_UPPER_CASE = excel_data["LETTER RECOGNITION_Upper case"]
    LETTER_RECOGNITION_LOWER_CASE = excel_data["LETTER RECOGNITION_Lower case"]
    CUPCAKES = excel_data["CUPCAKES"]
    CLEVER_MAX = excel_data["CLEVER MAX"]


    # Remove rows with the 2nd column containing NaN.
    RHYMING_WORDS = RHYMING_WORDS.dropna(subset=[RHYMING_WORDS.columns[1]]).reset_index().iloc[:, 1:]
    LETTER_RECOGNITION_UPPER_CASE = LETTER_RECOGNITION_UPPER_CASE.dropna(subset=[LETTER_RECOGNITION_UPPER_CASE.columns[1]]).reset_index().iloc[:, 1:]
    LETTER_RECOGNITION_LOWER_CASE = LETTER_RECOGNITION_LOWER_CASE.dropna(subset=[LETTER_RECOGNITION_LOWER_CASE.columns[1]]).reset_index().iloc[:, 1:]
    CUPCAKES = CUPCAKES.dropna(subset=[CUPCAKES.columns[1]]).reset_index().iloc[:, 1:]
    CLEVER_MAX = CLEVER_MAX.dropna(subset=[CLEVER_MAX.columns[1]]).reset_index().iloc[:, 1:]

    output_data = RHYMING_WORDS.iloc[:, :3]

    output_data = pd.concat([output_data, rhyming_words(RHYMING_WORDS)], axis=1, ignore_index=True)
    output_data = pd.concat([output_data, letter_recognition_upper_case(LETTER_RECOGNITION_UPPER_CASE)], axis=1, ignore_index=True)
    output_data = pd.concat([output_data, letter_recognition_lower_case(LETTER_RECOGNITION_LOWER_CASE)], axis=1, ignore_index=True)
    output_data = pd.concat([output_data, cupcakes(CUPCAKES)], axis=1, ignore_index=True)
    output_data = pd.concat([output_data, clever_max(CLEVER_MAX)], axis=1, ignore_index=True)

    score_sum = output_data.iloc[:, 3:].sum(axis=1)
    output_data['Score'] = score_sum
    scale_score = output_data.pop(2)
    output_data['Scale'] = scale_score

    first_names = output_data.iloc[:, 0].tolist()
    last_names = output_data.iloc[:, 1].tolist()
    student_marks = output_data.iloc[:, 2:].values.tolist()
    
    return first_names,last_names,student_marks

