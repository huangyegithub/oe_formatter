#Given a folder of tests for a school, and school classlist of current year
#Given that classlist is of current year if the file of data is from a previous year must back track student year level, using year difference
#Look through each test, identify type and create appropriate formatting template by copying from templates
#Put all students from test into template and name match with classlist, when name matched add date of birth and year level in
# Also given test assessment period five appropiate completed date

#Question: Do we add all different classes for a single assessment type to one formatted template or do we make multiple on for each class
# Answer: put all classes for assessment in same template however ensure no duplicate classes, for example, a school sends the same file for a class twice, thus we must check, if duplicate skip

import os
import pandas as pd
import shutil
from datetime import datetime
import numpy as np
from OE_Formatter_Functions.extract_student_info import get_student_info_from_database
from OE_Formatter_Functions.assessment_file_processing import raw_data_cleanse

def ReturnMatchesFunction(a,b):
    return [x for x in b if x in a]

def ReturnNotMatchesFunction(a,b):
    return [x for x in b if x not in a]

# Need to do the year level stuff
def format_school(school_directory, school_file_name):
    year_level_map = {0:"Foundation Year", 1:"Year 1", 2:"Year 2", 3:"Year 3", 4:"Year 4", 5:"Year 5"}

    data_years = set()
    assessments = {}

    school_name = school_file_name

    print(school_name)

    # Getting all the directories formatter will be working in
    working_directory = os.path.dirname(os.path.dirname(school_directory))
    formatted_directory = working_directory+"\\Formatted"
    templates_directory = working_directory+"\\Templates"
    # Assuming unformatted file is there enter unformatted OE school file
    # If we were to loop through multiple schools we put the loop here
    current_dir=school_directory
    os.chdir(current_dir)


    #Try and make directory in formatted file for school
    formatted_school = formatted_directory+"\\"+school_name
    try:
        os.mkdir(formatted_school)
    except:
        print("Formatted School File exists")
    formatted_school = formatted_school+"\\"+"ONENTRY"
    try:
        os.mkdir(formatted_school)
    except:
        pass

    # Finding the classlist then grabbing the contents
    assessment_files = os.listdir()
    try:
        classlist = [file for file in assessment_files if "Students" in file][0]
    except:
        print("No classlist file.")
    assessment_files.remove(classlist)
    classlist_path = current_dir + "\\" + classlist
    print(classlist_path)

    try:
        # Gets a dictionary of classlist where keys are first name + last name
        classlist_students, classlist_year = get_student_info_from_database(classlist_path)
    except Exception as error:
        print("Classlist does not exist")
        print(error)

    # Clean raw assessment data into acceptable format for further document creation.
    assessments = raw_data_cleanse(assessment_files, current_dir, data_years, assessments, formatted_school, templates_directory, school_name)

    for key,value in assessments.items():
        # We need to end a function here or the loop and add to a dictionary for the assessment type
        assessment_year = int(key[-4:])
        # We are assuming the classlist is always the latest version thus year_difference will always be greater than or equal to 0
        year_difference = classlist_year - assessment_year

        first_names = value[0]
        last_names = value[1]
        student_marks = value[2]
        template_path = value[3]
        template_destination = value[4]
        completed_date = value[5]

        combined_names = [(first + ' ' + last).title() for first, last in zip(first_names, last_names)]
        
        # Create a dictionary where keys are combined names and values are tuples of first name and last name
        name_dict = {combined_name: (first.title(), last.title(), marks) for combined_name, first, last, marks in zip(combined_names, first_names, last_names, student_marks)}
        #print(name_dict)
        

        # A list of student names
        student_classlist = list(classlist_students.keys())


        # Matches students from assessments with class list from school
        matched_list = ReturnMatchesFunction(combined_names, student_classlist)
        unmatched_list = ReturnNotMatchesFunction(student_classlist, combined_names)
        

        template_file = pd.read_excel(template_destination)

        data = []

        #Appending the matched students first to keep the excel file in the format of matched students then non-matched students
        if(year_difference > 0):
            for student in matched_list:
                student_list = classlist_students[student]
                date_of_birth = student_list[5].strftime("%d/%m/%Y")
                
                test_year_level = student_list[3]
                if "Foundation" not in test_year_level:
                    test_year_level_int = int(test_year_level[-1]) - year_difference
                    test_year_level = year_level_map[test_year_level_int]

                student = name_dict[student]
                marks = student[2]
                                #Given name, family name, testyearlevel, dob, completed date, marks
                row_values = [student_list[0],student_list[2],test_year_level,date_of_birth,completed_date] + marks
                data.append(row_values)
                #print(matched_df)
        else:
            for student in matched_list:
                student_list = classlist_students[student]
                date_of_birth = student_list[5].strftime("%d/%m/%Y")

                student = name_dict[student]
                marks = student[2]
                                #Given name, family name, testyearlevel, dob, completed date, marks
                row_values = [student_list[0],student_list[2],student_list[3],date_of_birth,completed_date] + marks
                data.append(row_values)
                #print(matched_df)


        for student in unmatched_list:
            student_list = name_dict[student]

            marks = student_list[2]
            row_values = [student_list[0],student_list[1],"","",completed_date] + marks
            data.append(row_values)

        columns = ["Given name", "Family name", "TestYearLevel", "DOB", "Completed date"] + [f"Q{i}" for i in range(1, len(marks)-1)] + ["Score", "Scale"]
            #print(columns)

        # Create a DataFrame from the list of row values and column names
        template_file = pd.DataFrame(data, columns=columns)
        
        formatted_df = pd.concat([template_file], ignore_index=True)
        

        # Assuming data and columns are defined somewhere before this code snippet

        # Convert 'DOB' and 'Completed date' columns to datetime objects
        formatted_df['DOB'] = pd.to_datetime(formatted_df['DOB'], format='%d/%m/%Y', errors='coerce')
        formatted_df['Completed date'] = pd.to_datetime(formatted_df['Completed date'], format='%d/%m/%Y', errors='coerce')
        
        
        # Convert the dates by using Excel serial date rules.
        reference_date = datetime(1899, 12, 30)
        formatted_df['DOB'] = formatted_df['DOB'].apply(lambda x: (x - reference_date).days)
        formatted_df['Completed date'] = formatted_df['Completed date'].apply(lambda x: (x - reference_date).days)
      

        formatted_df.to_excel(template_destination, index=False)

        # Puts dd/mm/yyyy format on columns D and E, these are the date columns for the excel dataframe
        with pd.ExcelWriter(template_destination, engine='xlsxwriter') as writer:
            formatted_df.to_excel(writer, index=False, sheet_name='Sheet1')

            # Access the workbook and worksheet objects
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']

            # Add a date format
            date_format = workbook.add_format({'num_format': 'dd/mm/yyyy'})

            # Apply the date format to the date columns
            worksheet.set_column('D:E', None, date_format)



        # Write the DataFrame to an Excel file, create a writer so we can format the date columns so they are in the correct format for upload
        

    print(school_name + ": Done")

# Upgrades: make new functions for mod1 S&L and Reading, make the functions in the format of the others
