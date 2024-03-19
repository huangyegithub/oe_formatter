import pandas as pd


# The input is the file path of a student information document (classlist).
# The output is a dictionary of student information with student first name and last name being the key and the year of the information.

def get_student_info_from_database(file_path):
    student_info = {}
    classlist = pd.read_excel(file_path, sheet_name=None)
    sheet_name = list(classlist.keys())

    # info_year returns the year of the student information file in type int.
    info_year = int(sheet_name[0][:4])
    classlist = classlist[sheet_name[0]]

    for index, row in classlist.iterrows():
        yr_level = row['Year']
        if yr_level in ["Foundation Year", "Year 1", "Year 2", "Year 3"]:
            key = (row['First Name'].title() + " " + row['Last Name'].title())
            # Only preserve the data in the first 6 columns.
            student_details = row[:6]
            student_info[key] = student_details
    
    return student_info, info_year