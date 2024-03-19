import pandas as pd
import numpy as np

def oral_language_summary(dataframe):
    dataframe = dataframe.iloc[:, 4:]
    
    results = dataframe.fillna(0)
    results = results.replace(to_replace='[C]', value=3, regex=True).infer_objects()
    results = results.replace(to_replace='[U]', value=2, regex=True).infer_objects()
    results = results.replace(to_replace='[S]', value=1, regex=True).infer_objects()
    results = results.replace(to_replace='[R]', value=0, regex=True).infer_objects()
    
    for index, row in results.iterrows():
        if row.iloc[9] == "ü" or row.iloc[9] == "l": results.at[index, results.columns[9]] = 2
        elif row.iloc[10] == 'ü' or row.iloc[10] == "l": results.at[index, results.columns[9]] = 1
        elif row.iloc[11] == 'ü' or row.iloc[11] == "l": results.at[index, results.columns[9]] = 0
    results = results.drop(results.columns[[10,11]], axis=1)
    return results.astype(int)

def oral_language_detailed(dataframe):
    dataframe = dataframe.iloc[:, 4:]
    columns_to_keep = [0,4,8,12,16,20,24,28,32,36,39,43]
    dataframe = dataframe.iloc[:, columns_to_keep]
    results = dataframe.fillna(0)
    results = results.replace(to_replace='[^0]', value=1, regex=True).infer_objects()
    return results.astype(int)

def words_and_sounds(dataframe):
    dataframe = dataframe.iloc[:, 4:]
    columns_to_keep = [0,2,4,6,8,9,10,11]
    dataframe = dataframe.iloc[:, columns_to_keep]
    results = dataframe.fillna(0)
    results = results.replace(to_replace='[^0]', value=1, regex=True).infer_objects()
    return results.astype(int)



def speak_learn_mod_2(excel_data):
    # Assign worksheets to relevant variables.
    ORAL_LANGUAGE_SUMMARY = excel_data["ORAL LANGUAGE SUMMARY"]
    ORAL_LANGUAGE_DETAILED = excel_data["ORAL LANGUAGE DETAILED"]
    WORDS_AND_SOUNDS = excel_data["WORDS AND SOUNDS"]

    # Remove rows with the 2nd column containing NaN.
    ORAL_LANGUAGE_SUMMARY = ORAL_LANGUAGE_SUMMARY.dropna(subset=[ORAL_LANGUAGE_SUMMARY.columns[1]]).reset_index().iloc[:, 1:]
    ORAL_LANGUAGE_DETAILED = ORAL_LANGUAGE_DETAILED.dropna(subset=[ORAL_LANGUAGE_DETAILED.columns[1]]).reset_index().iloc[:, 1:]
    WORDS_AND_SOUNDS = WORDS_AND_SOUNDS.dropna(subset=[WORDS_AND_SOUNDS.columns[1]]).reset_index().iloc[:, 1:]

    output_data = ORAL_LANGUAGE_SUMMARY.iloc[:, :3]
    
    output_data = pd.concat([output_data, oral_language_summary(ORAL_LANGUAGE_SUMMARY)], axis=1, ignore_index=True)
    output_data = pd.concat([output_data, oral_language_detailed(ORAL_LANGUAGE_DETAILED)], axis=1, ignore_index=True)
    output_data = pd.concat([output_data, words_and_sounds(WORDS_AND_SOUNDS)], axis=1, ignore_index=True)

    score_sum = output_data.iloc[:, 3:].sum(axis=1)
    output_data['Score'] = score_sum
    scale_score = output_data.pop(2)
    output_data['Scale'] = scale_score

    first_names = output_data.iloc[:, 0].tolist()
    last_names = output_data.iloc[:, 1].tolist()
    student_marks = output_data.iloc[:, 2:].values.tolist()

    return first_names,last_names,student_marks

