import pandas as pd
from OE_Formatter_Functions.extract_type import extract_type
from OE_Formatter_Functions.assessment_date import assessment_date
from OE_Formatter_Functions.copy_template import copy_template
from OE_Formatter_Functions.data_extraction_numeracy_mod_1 import numeracy_mod_1_data_extraction
from OE_Formatter_Functions.data_extraction_writing_mod_1 import writing_mod_1_data_extraction
from OE_Formatter_Functions.reading_mod_2 import reading_mod_2
from OE_Formatter_Functions.speak_learn_mod_2 import speak_learn_mod_2
from OE_Formatter_Functions.data_extraction_numeracy_mod_2 import numeracy_mod_2_data_extraction
from OE_Formatter_Functions.data_extraction_writing_mod_2 import writing_mod_2_data_extraction
from OE_Formatter_Functions.speak_learn_mod_1 import speak_learn_mod_1
from OE_Formatter_Functions.reading_mod_1 import reading_mod_1

def raw_data_cleanse(assessment_files, current_dir, data_years, assessments, formatted_school, templates_directory, school_name):
    for assessment in assessment_files:
        assessment_file_path = current_dir+"\\"+assessment
        classes = set()

        excel_data = pd.read_excel(assessment_file_path, sheet_name=None)
        sheet_names = list(excel_data.keys())
        # Skip Excel files without a sheet called "Summary".
        if "Summary" in sheet_names:
            assessment_type, assessment_name, module = extract_type(str(excel_data["Summary"].iloc[2].values[0]))
        else:
            continue
        
        module_number = module[-1]
        if int(module_number) in [3, 4]:
            continue
        elif int(module_number) not in [1, 2]:
            raise ValueError("Invalid module or module never encountered before")
        
        class_name = str(excel_data["Summary"].iloc[0]) + assessment_type
        
        assessment_period = excel_data["Summary"].iloc[1].values[0]

        completed_date, assessment_year = assessment_date(assessment_period) # This is ok
        
        formatted_school_year = formatted_school + "\\" + assessment_year
        assessment_type_year = assessment_type + " " + assessment_year
        if(assessment_year not in data_years):
            data_years.add(assessment_year)
            try:
                os.mkdir(formatted_school_year)
            except:
                print("School Year file exists")

        # Create the template if first time dealing with assessment type
        #On_Entry_Module_1_-_Numeracy_(Curriculum_linked),Useless_Loop_Primary_School.xlsx
        if assessment_type_year not in assessments:
            #Getting name of template to copy to formatted
            template_name = assessment_type + " BOT Template.xlsx"
            template_path = templates_directory+"\\"+template_name
            template_destination = formatted_school_year+"\\"+"On_Entry_Module_"+module_number+"_-_"+assessment_name+"_(Curriculum_linked),"+school_name+".xlsx"


            copy_template(template_path,template_destination)
            assessments[assessment_type_year] = [[],[],[],template_path,template_destination,""]

        # Given the template type we must call the function here somewhere
        # I believe we will add the class name the call it and the functions shall return a first names list, last names list and a student_marks list
        if class_name not in classes:
            classes.add(class_name)

            # Run assessment type function with assessment type as input
            
            #print("assessment_Type: ", assessment_type)
            # Add if statement after asking for module type
            module_number = int(module_number)
            if("Speaking" in assessment_type):
                if module_number == 1:
                    first_names_class, last_names_class, student_marks_class = speak_learn_mod_1(excel_data)
                else:
                    first_names_class, last_names_class, student_marks_class = speak_learn_mod_2(excel_data)
            if("Reading" in assessment_type):
                if module_number == 1:
                    first_names_class, last_names_class, student_marks_class = reading_mod_1(excel_data)
                else:
                    first_names_class, last_names_class, student_marks_class = reading_mod_2(excel_data)
            if("Writing" in assessment_type):
                if module_number == 1:
                    first_names_class, last_names_class, student_marks_class = writing_mod_1_data_extraction(excel_data)
                else:
                    first_names_class, last_names_class, student_marks_class = writing_mod_2_data_extraction(excel_data)
            if("Numeracy" in assessment_type):
                if module_number == 1:
                    first_names_class, last_names_class, student_marks_class = numeracy_mod_1_data_extraction(excel_data)
                else:
                    first_names_class, last_names_class, student_marks_class = numeracy_mod_2_data_extraction(excel_data)

            # Adding all new values to respective lists in the assessments dictionary

            assessments[assessment_type_year][0].extend(first_names_class)

            assessments[assessment_type_year][1].extend(last_names_class)

            assessments[assessment_type_year][2].extend(student_marks_class)
            
            assessments[assessment_type_year][5] = completed_date
    return assessments