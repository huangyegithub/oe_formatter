import pandas as pd

def writing_mod_2_data_extraction(all_sheets):
    THE_LUNCH_BOXES = all_sheets['THE LUNCH BOXES']
    # Remove rows with the 2nd column containing NaN.
    working_data = THE_LUNCH_BOXES.dropna(subset=[THE_LUNCH_BOXES.columns[1]]).reset_index().iloc[:, 1:]
    output_data = working_data.iloc[:, :3]
    # Drop the 3rd and 4th columns.
    working_data = working_data.drop(working_data.columns[[2, 3]], axis=1)
    number_of_questions = 9
    question_results = pd.DataFrame(0, index=range(output_data.shape[0]), columns=range(number_of_questions))
    marks = [0, 1, 2, 3, 0, 1, 2, 3, 4, 5, 6, 7, 0, 1, 2, 3, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 0, 1, 2, 3, 4, 5]
    for col in range(2, working_data.shape[1]):
        for row in range(working_data.shape[0]):
            if not pd.isna(working_data.iloc[row, col]):
                if col >= 2 and col <= 5:
                    question_results.iloc[row, 0] = marks[col - 2]
                elif col >= 6 and col <= 13:
                    question_results.iloc[row, 1] = marks[col - 2]
                elif col >= 14 and col <= 17:
                    question_results.iloc[row, 2] = marks[col - 2]
                elif col >= 18 and col <= 22:
                    question_results.iloc[row, 3] = marks[col - 2]
                elif col >= 23 and col <= 27:
                    question_results.iloc[row, 4] = marks[col - 2]
                elif col >= 28 and col <= 32:
                    question_results.iloc[row, 5] = marks[col - 2]
                elif col >= 33 and col <= 37:
                    question_results.iloc[row, 6] = marks[col - 2]
                elif col >= 38 and col <= 41:
                    question_results.iloc[row, 7] = marks[col - 2]
                else:
                    question_results.iloc[row, 8] = marks[col - 2]
    output_data = pd.concat([output_data, question_results], axis=1, ignore_index=True)
    score_sum = output_data.iloc[:, 3:].sum(axis=1)
    output_data['Score'] = score_sum
    scale_score = output_data.pop(2)
    output_data['Scale'] = scale_score
    
    first_names = output_data.iloc[:, 0].tolist()
    last_names = output_data.iloc[:, 1].tolist()
    student_marks = output_data.iloc[:, 2:].values.tolist()
    return first_names, last_names, student_marks