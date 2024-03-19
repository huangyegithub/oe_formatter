import pandas as pd

def number_and_quantity_processing(dataframe):
    # Drop the 3rd and 4th columns.
    dataframe = dataframe.drop(dataframe.columns[[0, 1, 2, 3]], axis=1)
    results = dataframe.fillna(0)
    results = results.replace(to_replace='[^0]', value=1, regex=True).infer_objects()
    return results.astype(int)

def number_sequence_processing(dataframe):
    dataframe = dataframe.iloc[:, [4, 8, 12, 13, 14, 15, 16, 17]]
    results = dataframe.fillna(0)
    results.iloc[:, 1:] = results.iloc[:, 1:].replace(to_replace='[^0]', value=1, regex=True).infer_objects()
    return results.astype(int)

def principles_of_counting_processing(dataframe):
    dataframe = dataframe.iloc[:, [4, 5, 6, 7, 8, 10, 12, 13]]
    results = dataframe.fillna(0)
    results = results.replace(to_replace='[^0]', value=1, regex=True).infer_objects()
    return results.astype(int)

def partitioning_processing(dataframe):
    dataframe = dataframe.iloc[:, [4, 5, 6, 7, 12]]
    results = dataframe.fillna(0)
    results = results.replace(to_replace='[^0]', value=1, regex=True).infer_objects()
    results = pd.concat([results.iloc[:, :3].sum(axis=1), results.iloc[:, 3:]], axis=1, ignore_index=True)
    return results.astype(int)

def pattern_position_and_shape_processing(dataframe):
    dataframe = dataframe.drop(dataframe.columns[[0, 1, 2, 3, 6, 14, 16, 18, 20, 22]], axis=1)
    results = dataframe.fillna(0)
    results = results.replace(to_replace='[^0]', value=1, regex=True).infer_objects()
    return results.astype(int)

def measurement_processing(dataframe):
    dataframe = dataframe.iloc[:, [4, 8, 9, 13, 14]]
    results = dataframe.fillna(0)
    results = results.replace(to_replace='[^0]', value=1, regex=True).infer_objects()
    return results.astype(int)

def numeracy_mod_1_data_extraction(all_sheets):
    # Assign worksheets to relevant variables.
    NUMBER_AND_QUANTITY = all_sheets['NUMBER AND QUANTITY']
    NUMBER_SEQUENCE = all_sheets['NUMBER SEQUENCE']
    PRINCIPLES_OF_COUNTING = all_sheets['PRINCIPLES OF COUNTING']
    PARTITIONING = all_sheets['PARTITIONING']
    PATTERN_POSITION_AND_SHAPE = all_sheets['PATTERN, POSITION AND SHAPE']
    MEASUREMENT = all_sheets['MEASUREMENT']
    
    # Remove rows with the 2nd column containing NaN.
    NUMBER_AND_QUANTITY = NUMBER_AND_QUANTITY.dropna(subset=[NUMBER_AND_QUANTITY.columns[1]]).reset_index().iloc[:, 1:]
    NUMBER_SEQUENCE = NUMBER_SEQUENCE.dropna(subset=[NUMBER_SEQUENCE.columns[1]]).reset_index().iloc[:, 1:]
    PRINCIPLES_OF_COUNTING = PRINCIPLES_OF_COUNTING.dropna(subset=[PRINCIPLES_OF_COUNTING.columns[1]]).reset_index().iloc[:, 1:]
    PARTITIONING = PARTITIONING.dropna(subset=[PARTITIONING.columns[1]]).reset_index().iloc[:, 1:]
    PATTERN_POSITION_AND_SHAPE = PATTERN_POSITION_AND_SHAPE.dropna(subset=[PATTERN_POSITION_AND_SHAPE.columns[1]]).reset_index().iloc[:, 1:]
    MEASUREMENT = MEASUREMENT.dropna(subset=[MEASUREMENT.columns[1]]).reset_index().iloc[:, 1:]

    output_data = NUMBER_AND_QUANTITY.iloc[:, :3]
    output_data = pd.concat([output_data, number_and_quantity_processing(NUMBER_AND_QUANTITY)], axis=1, ignore_index=True)
    output_data = pd.concat([output_data, number_sequence_processing(NUMBER_SEQUENCE)], axis=1, ignore_index=True)
    output_data = pd.concat([output_data, principles_of_counting_processing(PRINCIPLES_OF_COUNTING)], axis=1, ignore_index=True)
    output_data = pd.concat([output_data, partitioning_processing(PARTITIONING)], axis=1, ignore_index=True)
    output_data = pd.concat([output_data, pattern_position_and_shape_processing(PATTERN_POSITION_AND_SHAPE)], axis=1, ignore_index=True)
    output_data = pd.concat([output_data, measurement_processing(MEASUREMENT)], axis=1, ignore_index=True)

    score_sum = output_data.iloc[:, (output_data.columns != 31) & (output_data.columns >= 3)].sum(axis=1)
    output_data['Score'] = score_sum
    scale_score = output_data.pop(2)
    output_data['Scale'] = scale_score

    first_names = output_data.iloc[:, 0].tolist()
    last_names = output_data.iloc[:, 1].tolist()
    student_marks = output_data.iloc[:, 2:].values.tolist()
    return first_names, last_names, student_marks