import pandas as pd

# file_path = 'S:\Staff Folders\Davis\'s Stuff\OE Functions\Mod 2\\numeracy_raw_data_mod_2.xls'
# all_sheets = pd.read_excel(file_path, sheet_name=None)

def number_recognition_and_sequence_processing(dataframe):
    dataframe = dataframe.drop(dataframe.columns[[0, 1, 2, 3, 12, 13, 14, 23, 25, 27]], axis=1)
    results = dataframe.fillna(0)
    results.iloc[:, 7] = pd.to_numeric(results.iloc[:, 7], downcast='integer')
    for row in range(results.shape[0]):
        if isinstance(results.iloc[row, 7], str):
            results.iloc[row, 7] = 1
        else:
            results.iloc[row, 7] = 0
    results = results.replace(to_replace='[^0]', value=1, regex=True)
    return results.astype(int)

def principles_of_counting_processing(dataframe):
    dataframe = dataframe.iloc[:, [4, 6, 8, 9]]
    results = dataframe.fillna(0)
    results = results.replace(to_replace='[^0]', value=1, regex=True)
    return results.astype(int)

def partitioning_processing(dataframe):
    dataframe = dataframe.iloc[:, [4, 5, 6, 7, 12, 17, 22]]
    results = dataframe.fillna(0)
    results = results.replace(to_replace='[^0]', value=1, regex=True)
    results = pd.concat([results.iloc[:, :3].sum(axis=1), results.iloc[:, 3:]], axis=1, ignore_index=True)
    return results.astype(int)

def addition_mental_strategies_processing(dataframe):
    dataframe = dataframe.drop(dataframe.columns[[0, 1, 2, 3, 11, 12, 13, 15, 16, 17]], axis=1)
    results = dataframe.fillna(0)
    results = results.replace(to_replace='[^0]', value=1, regex=True)
    return results.astype(int)

def number_problems_processing(dataframe):
    dataframe = dataframe.iloc[:, [4, 8, 13, 18, 23, 28]]
    results = dataframe.fillna(0)
    results = results.replace(to_replace='[^0]', value=1, regex=True)
    return results.astype(int)

def money_fractions_pattern_processing(dataframe):
    dataframe = dataframe.drop(dataframe.columns[[0, 1, 2, 3, 11, 12, 15]], axis=1)
    results = dataframe.fillna(0)
    results = results.replace(to_replace='[^0]', value=1, regex=True)
    return results.astype(int)

def measurement_and_shape_processing(dataframe):
    dataframe = dataframe.drop(dataframe.columns[[0, 1, 2, 3, 5, 6, 7, 14, 16]], axis=1)
    results = dataframe.fillna(0)
    results = results.replace(to_replace='[^0]', value=1, regex=True)
    return results.astype(int)

def numeracy_mod_2_data_extraction(all_sheets):
    # Assign worksheets to relevant variables.
    NUMBER_RECOGNITION_AND_SEQUENCE = all_sheets['NUMBER RECOGNITION AND SEQUENCE']
    PRINCIPLES_OF_COUNTING = all_sheets['PRINCIPLES OF COUNTING']
    PARTITIONING = all_sheets['PARTITIONING']
    ADDITION_MENTAL_STRATEGIES = all_sheets['ADDITION MENTAL STRATEGIES']
    NUMBER_PROBLEMS = all_sheets['NUMBER PROBLEMS']
    MONEY_FRACTIONS_PATTERN = all_sheets['MONEY, FRACTIONS, PATTERN']
    MEASUREMENT_AND_SHAPE = all_sheets['MEASUREMENT AND SHAPE']
    
    # Remove rows with the 2nd column containing NaN.
    NUMBER_RECOGNITION_AND_SEQUENCE = NUMBER_RECOGNITION_AND_SEQUENCE.dropna(subset=[NUMBER_RECOGNITION_AND_SEQUENCE.columns[1]]).reset_index().iloc[:, 1:]
    PRINCIPLES_OF_COUNTING = PRINCIPLES_OF_COUNTING.dropna(subset=[PRINCIPLES_OF_COUNTING.columns[1]]).reset_index().iloc[:, 1:]
    PARTITIONING = PARTITIONING.dropna(subset=[PARTITIONING.columns[1]]).reset_index().iloc[:, 1:]
    ADDITION_MENTAL_STRATEGIES = ADDITION_MENTAL_STRATEGIES.dropna(subset=[ADDITION_MENTAL_STRATEGIES.columns[1]]).reset_index().iloc[:, 1:]
    NUMBER_PROBLEMS = NUMBER_PROBLEMS.dropna(subset=[NUMBER_PROBLEMS.columns[1]]).reset_index().iloc[:, 1:]
    MONEY_FRACTIONS_PATTERN = MONEY_FRACTIONS_PATTERN.dropna(subset=[MONEY_FRACTIONS_PATTERN.columns[1]]).reset_index().iloc[:, 1:]
    MEASUREMENT_AND_SHAPE = MEASUREMENT_AND_SHAPE.dropna(subset=[MEASUREMENT_AND_SHAPE.columns[1]]).reset_index().iloc[:, 1:]

    output_data = NUMBER_RECOGNITION_AND_SEQUENCE.iloc[:, :3]
    output_data = pd.concat([output_data, number_recognition_and_sequence_processing(NUMBER_RECOGNITION_AND_SEQUENCE)], axis=1, ignore_index=True)
    output_data = pd.concat([output_data, principles_of_counting_processing(PRINCIPLES_OF_COUNTING)], axis=1, ignore_index=True)
    output_data = pd.concat([output_data, partitioning_processing(PARTITIONING)], axis=1, ignore_index=True)
    output_data = pd.concat([output_data, addition_mental_strategies_processing(ADDITION_MENTAL_STRATEGIES)], axis=1, ignore_index=True)
    output_data = pd.concat([output_data, number_problems_processing(NUMBER_PROBLEMS)], axis=1, ignore_index=True)
    output_data = pd.concat([output_data, money_fractions_pattern_processing(MONEY_FRACTIONS_PATTERN)], axis=1, ignore_index=True)
    output_data = pd.concat([output_data, measurement_and_shape_processing(MEASUREMENT_AND_SHAPE)], axis=1, ignore_index=True)

    
    score_sum = output_data.iloc[:, output_data.columns >= 3].sum(axis=1)
    output_data['Score'] = score_sum
    scale_score = output_data.pop(2)
    output_data['Scale'] = scale_score

    first_names = output_data.iloc[:, 0].tolist()
    last_names = output_data.iloc[:, 1].tolist()
    student_marks = output_data.iloc[:, 2:].values.tolist()
    return first_names, last_names, student_marks

# numeracy_mod_2_data_extraction(all_sheets)