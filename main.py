from flask import Flask, request, jsonify
import openpyxl
import os
from timetable_class import Timetable
from timetable_input_output import read_data, excel_output

app = Flask(__name__)

def write_teachers_to_excel(teachers_data):
    """
    Write teacher data into the Excel sheet 'Teachers' starting at B3.
    """
    try:
        workbook = openpyxl.load_workbook("Timetable.xlsx")
        sheet = workbook["Teachers"]

        start_row = 3
        for idx, teacher in enumerate(teachers_data):
            teacher_id = teacher['teacher_id']  # Retrieve teacher ID
            name = teacher['teacher_name']
            subjects = ",".join(teacher['subjects'])
            sections = ",".join(teacher['preferred_sections'])
            # Write teacher ID to column A and the rest to subsequent columns
            sheet[f"A{start_row + idx}"] = teacher_id
            sheet[f"B{start_row + idx}"] = name
            sheet[f"C{start_row + idx}"] = subjects
            sheet[f"D{start_row + idx}"] = sections

        workbook.save("Timetable.xlsx")
        print("Teacher data successfully written to Timetable.xlsx.")
    except Exception as e:
        print(f"Error writing to Excel: {e}")

@app.route("/submit_teachers", methods=["POST"])
def submit_teachers():
    """
    Handle form submission and process teacher data.
    """
    data = request.get_json()  # Read the JSON data sent by Postman

    if 'teachers' not in data:
        return jsonify({"error": "No teachers data found"}), 400

    teachers_data = data['teachers']

    # Check if teachers data is correct
    print("Teachers data:", teachers_data)

    # Write the teacher data to Excel
    try:
        write_teachers_to_excel(teachers_data)
    except Exception as e:
        return jsonify({"error": f"Error writing data to Excel: {e}"}), 500

    # Call main function to generate timetable after writing data
    main()

    return jsonify({"message": "Teachers added successfully!"})

def main():
    """
    Main function to handle the timetable generation logic.
    """
    # excel input output file 
    excel_input_file = "Timetable.xlsx"
    
    # Take input from Excel
    timetable_data = read_data(excel_input_file)
    teachers, subjects, sections, rooms = timetable_data.read_all_data()

    # Create a timetable object
    timetable = Timetable(teachers, subjects, sections, rooms)

    # Generate the timetable
    timetable.generate_timetable()
    timetable.verify_timetable()

    get_output = excel_output(timetable, excel_input_file)
    get_output.print_output_excel_section()
    get_output.print_output_excel_teacher()
    get_output.print_output_excel_room()

    # Opening Excel file
    os.system("start EXCEL.EXE Timetable.xlsx")
    
if __name__ == "__main__":
    app.run(debug=True)
