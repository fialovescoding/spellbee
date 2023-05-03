import pandas as pd
import pandas_ods_reader as por

# Read tables from file
users = por.read_ods(r"spellbee/data/data.ods", sheet='users')
users['difficult-words'] = users['difficult-words'].astype(str)
words = por.read_ods(r"spellbee/data/data.ods", sheet='words')

# users.info()

# Filter GIS students and teachers
# students = users[(users['role'] == 'student') & (users['school-id'] == 1)]
teachers = users[(users['role'] == 'teacher') & (users['school-id'] == 1)]

# Go thru list of all teachers
for _, rt in teachers.iterrows():
    # Print Teacher's Name
    print(rt['name'])

    # Filter all students of the teacher
    students = users[(users['role'] == 'student') & \
                      (users['class'] == rt['class']) & \
                        (users['section'] == rt['section'])]
    
    # Go thru list of all students
    # for _, rs in students.iterrows():
    #     print(rs['name'])

    #     # Get list of difficult word IDs
    #     if rs['difficult-words'] is not None:
    #         dw = [int(x) for x in rs['difficult-words'].split(',')]
    #         difficult_words = words[words['id'].isin(dw)]
    #         print(difficult_words)

    # print(difficult_words)

min_class = 2
max_class = 4

my_words = words[(words['min-class'] == 2)]

print(my_words)