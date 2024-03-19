def extract_type(assessment_string):
    items = assessment_string.split(":")[1]
    items = items.split("-")
    module = "Mod 1"
    if "Module 2" in items[-1]:
        module = "Mod 2"
        
    assessment_name = items[0].strip()
    assessment_type = "OE " + module + " " + assessment_name
    return assessment_type, assessment_name, module