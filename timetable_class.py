from pprint import pprint
import random

class Room:
    def __init__(self, room_number, is_lab=False ,capacity=None):
        self.room_number = room_number
        self.is_lab = is_lab
        self.capacity = capacity
        

class Teacher:
    """Represents a teacher with details like ID, name, subjects, preferences, and timetable."""
    def __init__(self, teacher_id, name, subjects, preferred_sections, is_assistant=False, assigned_section=None):
        """
        Initializes a Teacher object with the provided details.

        Args:
            teacher_id (str): Unique identifier for the teacher.
            name (str): Name of the teacher.
            subjects (list): List of subject codes the teacher can teach.
            preferred_sections (list): List of preferred section IDs.
            is_assistant (bool, optional): Flag indicating if the teacher is an assistant. Defaults to False.
        """
        self.teacher_id = teacher_id  # Unique identifier for the teacher
        self.name = name  # Name of the teacher
        self.subjects = subjects  # List of subjects the teacher can teach
        self.preferred_sections = preferred_sections  # List of preferred sections
        self.is_assistant = is_assistant  # Flag indicating if the teacher is an assistant
        self.assigned_section = assigned_section  # Section ID if the teacher is a class animator

    def print_data(self):
        print(f" {self.teacher_id} " , end="")
        print(f" {self.name} " , end="")
        print(f" {self.subjects} " , end="")
        print(f" {self.preferred_sections} " , end="")
        print(f" {self.is_assistant} " , end="")
        print(f" {self.assigned_section} " , end="") 
        print("\n")

class Subject:
    """Represents a subject with details like code, name, repetitions, and type."""
    def __init__(self, subject_code, name, weekly_repetitions, is_practical, is_extracurricular,year,specialization):
        """
        Initializes a Subject object with the provided details.

        Args:
            subject_code (str): Unique code for the subject.
            name (str): Name of the subject.
            weekly_repetitions (int): Number of times the subject should be taught per week.
            is_practical (bool): Flag indicating if the subject is practical.
            is_extracurricular (bool): Flag indicating if the subject is extracurricular.
        """
        self.subject_code = subject_code  # Unique code for the subject
        self.name = name  # Name of the subject
        self.weekly_repetitions = weekly_repetitions  # Number of times the subject should be taught per week
        self.is_practical = is_practical  # Flag indicating if the subject is practical
        self.is_extracurricular = is_extracurricular  # Flag indicating if the subject is (eg. CA) extracurricular
        self.year = year
        self.specialization = specialization

    def print_data(self):
        print(f" {self.subject_code} " , end="")
        print(f" {self.name} " , end="")
        print(f" {self.weekly_repetitions} " , end="")
        print(f" {self.is_practical} " , end="")
        print(f" {self.is_extracurricular} " , end="")
        print(f" {self.year} " , end="")
        print(f" {self.specialization} " , end="")
        print("\n")

class Section:
    """Represents a section with details like ID, name, students, batch, and timetable."""
    def __init__(self, section_id, name, students, batch,year,specialization,preferred_room = None):
        """
        Initializes a Section object with the provided details.

        Args:
            section_id (str): Unique identifier for the section.
            name (str): Name of the section.
            students (list): List of student names in the section.
            batch (int): Batch of the section (0 for morning, 1 for evening).
        """
        self.section_id = section_id  # Unique identifier for the section
        self.name = name  # Name of the section
        self.students = students  # List of students in the section
        self.batch = batch  # Batch of the section (0 for morning, 1 for evening)
        self.preferred_room = preferred_room # Preferred room if any
        self.year = year
        self.specialization = specialization


    def print_data(self):
        print(f" {self.section_id} " , end="")
        print(f" {self.name} " , end="")
        print(f" {self.students} " , end="")
        print(f" {self.batch} " , end="")
        print(f" {self.year} " , end="")
        print(f" {self.specialization} " , end="")
        print(f" {self.preferred_room} " , end="")
        print("\n")

class Timetable:
    def __init__(self, teachers,subjects, sections,rooms):
        """Initializes a Timetable object with teacher, section, and subject data.

        Args:
            teachers (list): List of Teacher objects.
            sections (list): List of Section objects.
            subjects (list): List of Subject objects.
        """
        self.teachers = teachers
        self.sections = sections
        self.subjects = subjects
        self.rooms = rooms
        self.teacher_timetable = {}
        self.section_timetable = {}
        self.room_timetable = {}


        self.total_classes = 0 #Total needed classes - (4 subjects * 3 rep + 1 Practical * 2 rep )/Per section(4 Sections ) = 56

        # Initialize teacher, section and room timetables
        for teacher in self.teachers:
            self.teacher_timetable[teacher.teacher_id] = {}
            for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
                self.teacher_timetable[teacher.teacher_id][day] = {}
                for period in range(1, 9):
                    self.teacher_timetable[teacher.teacher_id][day][period] = None
        
        for section in self.sections:
            self.section_timetable[section.section_id] = {}
            for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
                self.section_timetable[section.section_id][day] = {}
                for period in range(1, 9):
                    self.section_timetable[section.section_id][day][period] = None

        for room in self.rooms:
            self.room_timetable[room.room_number] = {}
            for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
                self.room_timetable[room.room_number][day] = {}
                for period in range(1, 9):
                    self.room_timetable[room.room_number][day][period] = None


    def add_class(self, teacher_id, section_id, subject_code, day, period,room_number):
        """Adds a class to the teacher and section timetables.

        Args:
            teacher_id (str): ID of the teacher assigned the class.
            section_id (str): ID of the section taking the class.
            subject_code (str): Code of the subject being assigned.
            day (str): Day of the week for the class.
            period (int): Period number for the class.

        Raises:
            ValueError: If the class is already assigned to the teacher or section.
        """
        
        
        # Check if the class is already assigned to the teacher
        if self.teacher_timetable[teacher_id][day].get(period) is not None:
            raise ValueError(f"Teacher {teacher_id} is already assigned a class for {day} period {period}")

        # Check if the class is already assigned to the section
        if self.section_timetable[section_id][day].get(period) is not None:
            raise ValueError(f"Section {section_id} is already assigned a class for {day} period {period}")
        

        self.total_classes+=1

        # Update teacher timetable
        self.teacher_timetable[teacher_id][day][period] = (section_id, subject_code,room_number)

        # Update section timetable
        self.section_timetable[section_id][day][period] = (subject_code, teacher_id,room_number)

        # Update room timetable
        self.room_timetable[room_number][day][period] = (section_id, subject_code ,teacher_id)

    def is_available_period(self,teacher_id,section_id,day,period):
        # Check if the class is already assigned to the teacher
        if self.teacher_timetable[teacher_id][day].get(period) is not None:
            print(f"Teacher {teacher_id} is already assigned a class for {day} period {period}")
            return False

        # Check if the class is already assigned to the section
        if self.section_timetable[section_id][day].get(period) is not None:
            print(f"Section {section_id} is already assigned a class for {day} period {period}")
            return False
        
        return True

    def find_suitable_room(self, section, day, period, subject):
        """Finds a suitable room for a given section, day, period, and subject.

        Args:
            section (Section): The section object.
            day (str): The day of the week.
            period (int): The period number.
            subject (Subject): The subject object.

        Returns:
            str: The room number if found, otherwise None.
        """

        if subject.is_practical:
            for room in self.rooms:
                if room.is_lab and self.is_room_available(room.room_number, day, period):
                    return room.room_number
        else:
            preferred_room = section.preferred_room if section.preferred_room else None
            if preferred_room and self.is_room_available(preferred_room, day, period):
                return preferred_room

            for room in self.rooms:
                if self.is_room_available(room.room_number, day, period):
                    return room.room_number

        return None

    def is_room_available(self, room_number, day, period):
        return self.room_timetable[room_number][day].get(period) is None

    # def total_required_classes(self):
    #     section_per_year = [8,7,6]
    #     total_classes = 0
    #     for sub in self.subjects:
    #         print(f"Subject - {sub.name} , total classes - {total_classes} , weekely rep - {sub.weekly_repetitions} and total section - {section_per_year[sub.year-1]}")
    #         total_classes += sub.weekly_repetitions * section_per_year[sub.year-1]
            
    #     return total_classes
            


    def get_section_batch(self,section):
        """Returns the batch (morning/evening) of a section."""
        return [1,2,3,4] if section.batch == 0 else [5,6,7,8]
    
    def get_subject(self, subject_code):
        """Retrieves a subject object based on its subject code.

        Args:
            subject_code (str): The code of the subject to retrieve.

        Returns:
            Subject: The subject object if found, otherwise None.
        """

        for subject in self.subjects:
            if subject.subject_code == subject_code:
                return subject
        return None


    def get_required_subject(self,section, day):

        """Determines required subjects for a section based on weekly repetitions."""
        required_subjects = []
        section_timetable = self.section_timetable[section.section_id]  # Access section timetable through Timetable instance

        for subject in self.subjects:
            # print(f"section -{section.section_id} Subject Year - {subject.year} Section Year - {section.year} section Specialisation - {section.specialization} Subejct specialisations - ")
            # pprint(subject.specialization)
            if (subject.year == section.year and section.specialization in subject.specialization) == False:
                continue
            # print(f"Section - {section.section_id} and subject - {subject.subject_code}")

            # To check the subject is taught or not on a particular day 
            is_taught_on_day = False
            for classes in section_timetable.get(day, {}).values():
                if classes is not None and subject.subject_code in classes:
                    is_taught_on_day=True
            
            if not is_taught_on_day:  # Check if subject not assigned for the day
                # To check how many times the particular subject is taught in a week
                subject_count = 0
                for week_day in section_timetable:
                    for classes in section_timetable.get(week_day, {}).values():
                        if classes is not None and subject.subject_code in classes :
                            subject_count+=1
                if subject_count < subject.weekly_repetitions:  # Check if required repetitions not met
                    required_subjects.append(subject.subject_code)

        random.shuffle(required_subjects)
        return required_subjects

    def is_teacher_available(self,teacher_id, day, period):
        """Checks if a teacher is available for a given day and period."""
        
        return self.teacher_timetable[teacher_id][day].get(period) is None  # Check if the period is free

    def find_suitable_teacher(self,subject_code, section, day, period, is_assistant=False):
        """Finds a suitable teacher for a given subject, section, day, and period."""
        for teacher in self.teachers:
             
            subject = self.get_subject(subject_code)

            # Check if the subject is extracurricular and for class animator
            if subject.is_extracurricular and teacher.assigned_section and section.section_id == teacher.assigned_section and self.is_teacher_available(teacher.teacher_id, day, period):
                # print("IN EC")
                return teacher.teacher_id
        
            if subject_code in teacher.subjects and \
            section.section_id in teacher.preferred_sections and \
            self.is_teacher_available(teacher.teacher_id, day, period) and \
            teacher.is_assistant == is_assistant:
                return teacher.teacher_id
        return None  # Return None if no suitable teacher found

    def handle_practical_subject(self, section, day, period, subject_code,room_number):
        """Handles allocation of practical subjects with main and assistant teachers.

        Args:
            section (Section): Section object for which the subject is being assigned.
            day (str): Day of the week.
            period (int): Period number.
            subject_code (str): Code of the practical subject.

        Returns:
            bool: True if successful, False otherwise.
        """

        # Find main teacher
        main_teacher_id = self.find_suitable_teacher(subject_code, section, day, period, False)
        if not main_teacher_id:
            # print(f"Main teacher not found for subject - {subject_code} and section {section} and day - {day}")
            return False

        # Find assistant teacher
        assistant_teacher_id = self.find_suitable_teacher(subject_code, section, day, period + 1, True)
        if not assistant_teacher_id:
            # print(f"Assistant teacher not found for subject - {subject_code} and section {section} and day - {day}")
            return False

        # Combine teacher IDs
        practical_teachers = f"{main_teacher_id} & {assistant_teacher_id}"

        # Update teacher timetables
        self.teacher_timetable[main_teacher_id][day][period] = (section.section_id, subject_code,room_number)
        self.teacher_timetable[main_teacher_id][day][period + 1] = (section.section_id, subject_code,room_number)
        self.teacher_timetable[assistant_teacher_id][day][period] = (section.section_id, subject_code,room_number)
        self.teacher_timetable[assistant_teacher_id][day][period + 1] = (section.section_id, subject_code,room_number)

        # Update section timetable
        self.section_timetable[section.section_id][day][period] = (subject_code, practical_teachers,room_number)
        self.section_timetable[section.section_id][day][period + 1] = (subject_code, practical_teachers,room_number)

        # Update room timetable
        self.room_timetable[room_number][day][period] = (section.section_id, subject_code ,practical_teachers)
        self.room_timetable[room_number][day][period+1] = (section.section_id, subject_code ,practical_teachers)

        self.total_classes+=2

        return True


    def generate_timetable(self):

        # print("In generate time table for ","xl")
        # # Testing purpose for input
        # for test_teacher in self.teachers:
        #     test_teacher.print_data()

        # for test_section in self.sections:
        #     test_section.print_data()

        # for test_subject in self.subjects:
        #     test_subject.print_data()

        for section in self.sections:
            total_classes_for_section = 0
            print(f"In section - {section.section_id}")
            for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
                period = 1
                while period<9:  # Assuming 8 periods per day

                    period_consumed = 1
                    # Check the batch 
                    if period not in self.get_section_batch(section):
                        period+=period_consumed
                        continue
                        
                    required_subjects = self.get_required_subject(section, day)
                    # print(f"Inside generate tt for day - {day} and period - {period}  and  Subject - " , end="")
                    # print(required_subjects)

                    # CHeck if no subject is required 
                    if required_subjects is None:
                        period+=period_consumed
                        continue

                    subject_dict = {subject.subject_code: subject for subject in self.subjects}
                    for subject_code in required_subjects:
                        
                        room_number = self.find_suitable_room(section, day, period, subject_dict[subject_code])
                        if not room_number:
                            # Handle case where no room is available
                            # print("No room found")
                            continue
                            
                        subject = subject_dict[subject_code]  # Access subject using dictionary
                        if subject.is_practical:
                            # print(f"Practical check for section {section.section_id}")
                            # Iterating to next subject if 2 period are not free for practical
                            if (section.batch == 0 and period == 4) or (section.batch == 1 and period == 8 ):
                                continue
                            success = self.handle_practical_subject(section, day, period, subject_code,room_number)
                            if success:
                                period_consumed += 1
                                total_classes_for_section+=2
                                break
                            # else:
                            #     print(f"Error in handling practical for section id - {section.section_id}")
                        else:
                            teacher_id = self.find_suitable_teacher(subject_code, section, day, period, False)
                            if teacher_id:
                                self.add_class(teacher_id, section.section_id, subject_code, day, period,room_number)
                                total_classes_for_section+=1
                                break
                    period += period_consumed
            print(f"Section ID - {section.section_id} and total classes = {total_classes_for_section}")

        # return timetable

    def verify_timetable(self):
        for section in self.sections:

            # First we will see if there is any required subjects
            req_sub_for_section = []
            section_timetable = self.section_timetable[section.section_id]  # Access section timetable through Timetable instance
            for subject in self.subjects:

                if (subject.year == section.year and section.specialization in subject.specialization) == False:
                    continue
            
                # To check how many times the particular subject is taught in a week
                subject_count = 0
                for week_day in section_timetable:
                    for classes in section_timetable.get(week_day, {}).values():
                        if classes is not None and subject.subject_code in classes :
                            subject_count+=1
                if subject_count < subject.weekly_repetitions:  # Check if required repetitions not met
                    req_sub_for_section.append(subject.subject_code)

            # if required subject list length > 0 then there is a problem
            if len(req_sub_for_section) > 0:
                print(f"Classes are needed for section - {section.section_id} and the required subjects are - ")
                print(req_sub_for_section)

                # Try to resolve the problem 
                # and if not then why is it not resolving
                for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
                    period = 1
                    while period<9:  # Assuming 8 periods per day

                        period_consumed = 1
                        # Check the batch 
                        if period not in self.get_section_batch(section):
                            period+=period_consumed
                            continue

                        # checking if the period is empty or None
                        # if section_timetable[section.section_id][day][period] is not None:
                        #     period+=period_consumed
                        #     continue

                        # if section_timetable.get(section.section_id, {}).get(day, {}).get(period) is not None:
                        #     # Process period
                        #     period += period_consumed
                        #     continue

                        # Check if the class is already assigned to the section
                        if self.section_timetable[section.section_id][day].get(period) is not None:
                            # print(f"Section {section.section_id} is already assigned a class for {day} period {period}")
                            period+=period_consumed
                            continue

                        print(f"For section - {section.section_id} , day - {day} and period - {period}")

                        required_subjects = self.get_required_subject(section, day)

                        # CHeck if no subject is required 
                        if required_subjects is None:
                            period+=period_consumed
                            continue

                        subject_dict = {subject.subject_code: subject for subject in self.subjects}
                        for subject_code in required_subjects:
                            
                            room_number = self.find_suitable_room(section, day, period, subject_dict[subject_code])
                            if not room_number:
                                # Handle case where no room is available
                                print(f"No room found for section - {section.section_id}")
                                continue
                                
                            subject = subject_dict[subject_code]  # Access subject using dictionary
                            if subject.is_practical:
                                if (section.batch == 0 and period == 4) or (section.batch == 1 and period == 8 ):
                                    print(f"The subject - {subject_code} is practical and the period free is 4 or 8 for section - {section.section_id}")
                                    continue
                                success = self.handle_practical_subject(section, day, period, subject_code,room_number)
                                if success:
                                    print(f"The subject - {subject_code} is practical and the class is assigned for section - {section.section_id}")
                                    period_consumed += 1 
                                    break
                                else:
                                    print(f"Not able to handle practical for section id - {section.section_id}")
                            else:
                                teacher_id = self.find_suitable_teacher(subject_code, section, day, period, False)
                                if teacher_id is None:
                                    print(f"Not able to find teacher for section {section.section_id} and for subject - {subject_code} on day - {day}")
                                else:
                                    # Check if the class is already assigned to the teacher
                                    if self.teacher_timetable[teacher_id][day].get(period) is not None:
                                        print(f"Teacher {teacher_id} is already assigned a class for {day} period {period}")
                                        period+=period_consumed
                                        continue
                                    
                                    self.add_class(teacher_id, section.section_id, subject_code, day, period,room_number)
                                    break
                        period += period_consumed
        print(f"Total classes Expected for - 297 and Total classes Occuring - {self.total_classes}")



# # Sample data
# # Data type needed - String,String,list,list,bool,String,
# teachers = [
#     Teacher("T1", "Teacher 1 test2.py", ["MATH", "VB","VB-P"], ["III A", "III B"], False ,"III A"),
#     Teacher("T2", "Teacher 2", ["MATH", "VB","VB-P"], ["III C", "III D"], False ,"III B"),
#     Teacher("T3", "Teacher 3", ["MATH", "VB","VB-P"], ["III E", "III F"], False ,"III E"),
#     Teacher("T4", "Teacher 4", ["DS"], ["III A", "III B","III E"], False , "III C"),
#     Teacher("T22", "Teacher 4", ["DS"], ["III C", "III D","III F"], False ),
#     Teacher("T5", "Teacher 5", ["VB","VB-P"], ["III A", "III B","III E"], True, "III D"),  # Assistant teacher
#     Teacher("T6", "Teacher 6", ["VB","VB-P"], ["III C", "III D","III F"], True, "III F"),  # Assistant teacher

#     Teacher("T7", "Teacher 7", ["JP","J-P"], ["II A", "II B","II C","II D"], False , "II A"),
#     Teacher("T8", "Teacher 8", ["JP","J-P"], ["II E" , "II F" ,"II G"], False , "II B"),
#     Teacher("T9", "Teacher 9", ["JP","J-P"], ["II A", "II B","II C","II D"], True,"II C"),  # Assistant teacher
#     Teacher("T10", "Teacher 10", ["JP","J-P"], ["II E" , "II F" ,"II G"], True,"II D"),  # Assistant teacher
#     Teacher("T11", "Teacher 11", ["STAT"], ["II A", "II B","II C","II D","II E" , "II F" ,"II G"], False , "II E"),
#     Teacher("T12", "Teacher 12", ["OS", "PYR"], ["II A", "II B","II C","II D","II E" , "II F" ,"II G"], False , "II F"),
#     Teacher("T13", "Teacher 13", ["ENG"], ["II A", "II B","II C","II D","II E" , "II F" ,"II G"], False , "II G"),

#     Teacher("T14", "Teacher 14", ["PC","P-P-C"], ["I A", "I B","I C"], False , "I A"),
#     Teacher("T15", "Teacher 15", ["PC","P-P-C"], ["I D","I E" , "I F" ], False , "I B"),
#     Teacher("T23", "Teacher 15", ["PC","P-P-C"], ["I G" , "I H"], False),
#     Teacher("T16", "Teacher 16", ["PCCF"], ["I A", "I B","I C","I D"], False , "I C"),
#     Teacher("T25", "Teacher 25", ["PCCF"], ["I E" , "I F" ,"I G" , "I H"], False ),
#     Teacher("T17", "Teacher 17", ["ENG"], ["I A", "I B","I C","I D"], False , "I D"),
#     Teacher("T24", "Teacher 18", ["ENG"], ["I E" , "I F" ,"I G" , "I H"], False ),
#     Teacher("T18", "Teacher 19", ["ELE"], ["I A", "I B","I C","I D","I E" , "I F" ,"I G" , "I H"], False , "I E"),
#     Teacher("T19", "Teacher 20", ["STAN", "IOTI"], ["I A", "I B","I C","I D","I E" , "I F" ,"I G" , "I H"], False , "I F"),
#     Teacher("T20", "Teacher 21", ["PC","P-P-C"], ["I A", "I B","I C","I D"], True,"I G"),  # Assistant teacher
#     Teacher("T21", "Teacher 22", ["PC","P-P-C"], ["I E" , "I F" ,"I G" , "I H"], True,"I H"),  # Assistant teacher
#     # Teacher("T25", "Teacher 20", ["VB","DS","VB-P","CA","MATH"], ["III A", "III B","III C","III D","III E" , "III F" ], False , ["I F"]),
#     # Teacher("T26", "Teacher 20", ["JP","STAT","J-P","CA","OS","ENG","PYR"], ["II A", "II B","II C","II D","II E" , "II F" ,"II G" ], False , ["I F"]),
#     # Teacher("T27", "Teacher 20", ["PC","ELE","P-P-C","CA","PCCF","ENG","STAN","IOTI"], ["I A", "I B","I C","I D","I E" , "I F" ,"I G" , "I H"], False , ["I F"]),
# ]

# # Current Specialisation - General,Analytics & IOT for 1st Year
# #                          General & Analytics for 2nd Year
# #                          General for 3rd Year


# # Data type needed - String,String,int,bool,bool,int,list
# subjects = [
#     Subject("PC", "Programming in C", 3, False, False,1,["General","Analytics","IOT"]),
#     Subject("ELE", "Electronics", 3, False, False,1,["General"]),
#     Subject("P-P-C", "Practical of C Programming", 2, True, False,1,["General","Analytics","IOT"]),
#     Subject("CA", "Current_Affair", 1, False, True,1,["General","Analytics","IOT"]),
#     Subject("PCCF", "Compter Fundamentals", 3, False, False,1,["General","Analytics","IOT"]),
#     Subject("ENG", "English", 3, False, False,1,["General","Analytics","IOT"]),
#     Subject("STAN", "Stastics and Analytics", 3, False, False,1,["Analytics"]),
#     Subject("IOTI", "Internet Of Things Introduction", 3, False, False,1,["IOT"]),

#     Subject("JP", "Java Programming", 3, False, False,2,["General","Analytics"]),
#     Subject("STAT", "Stastics", 3, False, False,2,["General","Analytics"]),
#     Subject("J-P", "Java Practical", 2, True, False,2,["General","Analytics"]),
#     Subject("CA", "Current_Affair", 1, False, True,2,["General","Analytics"]),
#     Subject("OS", "Operating System", 3, False, False,2,["General"]),
#     Subject("ENG", "English", 3, False, False,2,["General","Analytics"]),
#     Subject("PYR", "Python and R", 3, False, False,2,["Analytics"]),

#     Subject("VB", "VB.net", 3, False, False,3,["General"]),
#     Subject("DS", "Data Structures", 3, False, False,3,["General"]),
#     Subject("VB-P", "VB.net Practical", 2, True, False,3,["General"]),
#     Subject("CA", "Current_Affair", 1, False, True,3,["General"]),
#     Subject("MATH", "Maths", 3, False, False,3,["General"]),
# ]

# # Data type needed - String,String,list,int,int,string,string
# sections = [
#     Section("I A", "Section A", ["Student1"], 0 , 1 , "General" ,"R108"),  # Morning section
#     Section("I B", "Section B", ["Student3"], 1 , 1 , "General" ,"R109"),  # Evening section
#     Section("I C", "Section C", ["Student1"], 0 , 1 , "General" ,"R110"),
#     Section("I D", "Section D", ["Student1"], 1 , 1 , "General" ,"R108"),
#     Section("I E", "Section E", ["Student1"], 0 , 1 , "General" ,"R109"),
#     Section("I F", "Section F", ["Student1"], 1 , 1 , "Analytics" ,"R110"),
#     Section("I G", "Section G", ["Student1"], 0 , 1 , "Analytics" ,"R111"),
#     Section("I H", "Section H", ["Student1"], 1 , 1 , "IOT" ,"R111"),

#     Section("II A", "Section A", ["Student1"], 0 , 2 , "General" ,"R104"),  # Morning section
#     Section("II B", "Section B", ["Student3"], 1 , 2 , "General" ,"R105"),  # Evening section
#     Section("II C", "Section C", ["Student1"], 0 , 2 , "General" ,"R106"),
#     Section("II D", "Section D", ["Student1"], 1 , 2 , "General" ,"R104"),
#     Section("II E", "Section E", ["Student1"], 0 , 2 , "General" ,"R105"),
#     Section("II F", "Section F", ["Student1"], 1 , 2 , "Analytics" ,"R106"),
#     Section("II G", "Section G", ["Student1"], 0 , 2 , "Analytics" ,"R107"),

#     Section("III A", "Section A", ["Student1"], 0 , 3 , "General" ,"R101"),  # Morning section
#     Section("III B", "Section B", ["Student3"], 1 , 3 , "General" ,"R102"),  # Evening section
#     Section("III C", "Section C", ["Student1"], 0 , 3 , "General" ,"R103"),
#     Section("III D", "Section D", ["Student1"], 1 , 3 , "General" ,"R101"),
#     Section("III E", "Section E", ["Student1"], 0 , 3 , "General" ,"R102"),
#     Section("III F", "Section F", ["Student1"], 1 , 3 , "General" ,"R103"),
# ]

# rooms = [
#     Room("R101"),
#     Room("R102"),
#     Room("R103"),
#     Room("R104"),
#     Room("R105"),
#     Room("R106"),
#     Room("R107"),
#     Room("R108"),
#     Room("R109"),
#     Room("R110"),
#     Room("R111"),
#     Room("R112"),

#     Room("R201", is_lab=True),
#     Room("R113", is_lab=True),

# ]



def main(teachers,subjects, sections,rooms):
    # Create a timetable object
    timetable = Timetable(teachers,subjects, sections,rooms)

    # Generate the timetable
    timetable.generate_timetable()
    # timetable.generate_timetable()

    # Printing sections Timetable
    for sec in sections:
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            print("\nYear - " ,sec.year , "Section - " , sec.section_id , " and Day - ",day,"\n")
            pprint(timetable.section_timetable[sec.section_id][day])

    # # Printing Teachers Timetable
    for tec in teachers:
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            print("\nTeacher Name - " , tec.name , " and Day - ",day,"\n")
            pprint(timetable.teacher_timetable[tec.teacher_id][day])

    # Printing rooms Timetable
    # for ro in rooms:
    #     for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
    #         print("\nRoom - " , ro.room_number , " and Day - ",day,"\n")
    #         pprint(timetable.room_timetable[ro.room_number][day])

    print("Total classes Expected for - 297 and Total classes Occuring - " , timetable.total_classes)

if __name__ == "__main__":

    # main(teachers,subjects, sections,rooms)
    pass
