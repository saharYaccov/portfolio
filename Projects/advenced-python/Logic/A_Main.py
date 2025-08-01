from sqlalchemy.orm import orm_insert_sentinel

from AdvancedPythonProject.logic.Course import Course
from AdvancedPythonProject.logic.Student import Students,Registered_Status
from AdvancedPythonProject.logic.Teacher import Teacher
from AdvancedPythonProject.logic.Parent import Parent
from AdvancedPythonProject.logic.General_Worker import General_Worker
from AdvancedPythonProject.logic.Task import Task , TaskStatus
from AdvancedPythonProject.logic.Manager import Manager
from AdvancedPythonProject.logic.Payment import Payment
from AdvancedPythonProject.logic.Employee import Employee, Seniority
from AdvancedPythonProject.logic.Queue_wait import Queue_wait
from AdvancedPythonProject.logic.Person import Person , State

from AdvancedPythonProject.Data_Layer import sql
sql_ = sql.sql()
sql_.create_db("university_dataBase_data")
sql_.db_name = "university_dataBase_data"

def add_data_to_sql(new_dataFrame_table_name , current_df_of_table_name):

    df_students = pd.DataFrame([student.__dict__ for student in list_students])
    df_courses = pd.DataFrame([course.__dict__ for course in list_courses])
    df_teachers = pd.DataFrame([teacher.__dict__ for teacher in list_teachers])
    df_general_employees = pd.DataFrame([worker.__dict__ for worker in list_general_employees])
    df_managers = pd.DataFrame([manager.__dict__ for manager in list_managers])
    df_parents = pd.DataFrame([parent.__dict__ for parent in list_parents])
    df_queues = pd.DataFrame([queue.__dict__ for queue in list_queues])

    # חשוב: אסור שיהיה רווח בשם של הטבלאות !!!!!!!!!
    dictionary_all = {
        'Course': "_course_id INT AUTO_INCREMENT PRIMARY KEY,_course_size INT,_name VARCHAR(100) NOT NULL,_student_list TEXT",

        'general_worker': "_id INT AUTO_INCREMENT PRIMARY KEY,_name VARCHAR(100) NOT NULL,_age INT NOT NULL,_phone_number VARCHAR(10),_status TEXT ,_salary INT ,_seniority TEXT ,_tasks_list TEXT",

        'Manager': "_id INT AUTO_INCREMENT PRIMARY KEY,_name VARCHAR(100) NOT NULL,_age INT NOT NULL,_phone_number VARCHAR(15),_status TEXT,_salary INT NOT NULL,_seniority TEXT,_worker_list TEXT,_teacher_list TEXT",

        'Parent': "_id INT AUTO_INCREMENT PRIMARY KEY,_name VARCHAR(100) NOT NULL,_age INT NOT NULL,_phone_number VARCHAR(15),_status TEXT,_payment TEXT, _childrenList TEXT",

        'Student': "_id INT AUTO_INCREMENT PRIMARY KEY,_name VARCHAR(100) NOT NULL,_age INT NOT NULL,_phone_number VARCHAR(15),_status TEXT,_grade_course TEXT,_registered TEXT",

        'Teacher': "_id INT AUTO_INCREMENT PRIMARY KEY,_name VARCHAR(100) NOT NULL,_age INT NOT NULL,_phone_number VARCHAR(15),_status TEXT,_salary INT,_seniority TEXT,_course_list TEXT,_student_list TEXT",

        'Wait_Queue': "_id INT AUTO_INCREMENT PRIMARY KEY,_course_of_queue TEXT,_queue TEXT"

    }
    for key, val in dictionary_all.items():
        sql_.create_table(key, val)

    all_df_in_school = [df_students, df_teachers, df_courses, df_general_employees, df_managers, df_parents, df_queues]
    tableName = ['Student', 'Teacher', 'Course', 'general_worker', 'Manager', 'Parent', 'Wait_Queue']

    for i, df_item in enumerate(all_df_in_school):
        table_name = tableName[i]
        sql_.add_df_to_table(table_name, df_item)
    sql_.add_df_to_table(new_dataFrame_table_name,current_df_of_table_name)


import pandas as pd
stu_state = State.state_student
Students_miki = Students('Miki','123456789',19,"0526573644" , stu_state, {1:88,2:88},Registered_Status.UNREGISTERED )
Students_ron = Students('Ron', '123456781', 21, "0526758492", stu_state, {3:92, 1:85}, Registered_Status.REGISTERED)
Students_noa = Students('Noa', '123456782', 20, "0526583945", stu_state, {1:78, 3:91}, Registered_Status.UNREGISTERED)
Students_avi = Students('Avi', '123456783', 22, "0526738541", stu_state, {5:95, 2:88}, Registered_Status.REGISTERED)
Students_david = Students('David', '123456784', 24, "0526789524", stu_state, {1: 91, 7: 84}, Registered_Status.UNREGISTERED)
Students_ronit = Students('Ronit', '123456785', 25, "0526892345", stu_state, {5: 83, 4: 90}, Registered_Status.REGISTERED)
Students_sara = Students('Sara', '123456786', 19, "0526958794", stu_state, {4: 75, 5: 89}, Registered_Status.UNREGISTERED)
#student in queue
Students_or_in_queue = Students('Or', '999999999', 24, "0527788277", stu_state, {1: 100, 7: 56}, Registered_Status.UNREGISTERED)
Students_ori_in_queue = Students('Ori', '999999998', 25, "0523092900", stu_state, {5: 55, 4: 55}, Registered_Status.REGISTERED)
Students_mosh_in_queue = Students('Mosh', '999999997', 19, "0522918377", stu_state, {4: 80, 5: 0 , 6:100 }, Registered_Status.REGISTERED)

course_size = 10
course_math = Course('Math' , '100000000' ,course_size, [Students_avi,Students_miki,Students_noa])
course_bio = Course('Bio' , '200000000' , course_size,[Students_miki,Students_ron])
course_english = Course('English' , '300000000' , course_size, [Students_david,Students_sara,Students_ronit,Students_noa])
course_economics = Course('Economics' , '400000000' , course_size, [Students_ronit,Students_david,Students_avi,Students_miki,Students_noa])
course_law = Course('law' , '500000000' , course_size, [Students_ron,Students_avi,Students_miki,Students_noa])

queue_math = Queue_wait([Students_or_in_queue,Students_ori_in_queue],id=99990,course_of_queue=course_math)
queue_bio = Queue_wait([Students_mosh_in_queue,Students_ori_in_queue],course_bio,id=99991)
queue_english = Queue_wait([Students_or_in_queue,Students_ori_in_queue,Students_mosh_in_queue.id],course_english,id=99992)
queue_economics = Queue_wait([Students_or_in_queue,Students_ori_in_queue],course_economics,id=99993)
queue_law = Queue_wait([Students_or_in_queue,Students_avi,Students_miki],course_law,id=99994)

teacher_state = State.state_teacher
teacher_ben = Teacher('Ben','121212121',24,"0524534566",teacher_state,4500,Seniority.MASTER,course_list=[course_bio,course_english],student_list=[Students_noa , Students_miki])
teacher_sara = Teacher('Sara', '212121212', 32, "0524534568", teacher_state, 5200, Seniority.EXPERT, course_list=[course_math], student_list=[Students_ron, Students_avi])
teacher_lior = Teacher('Lior', '131313131', 38, "0524534569", teacher_state, 4800, Seniority.SENIOR, course_list=[course_english,course_math], student_list=[Students_ron, Students_miki])
teacher_yaron = Teacher('Yaron', '313131313', 25, "0524534570", teacher_state, 4600, Seniority.JUNIOR, course_list=[course_economics, course_law], student_list=[Students_noa, Students_avi])

task_clean = Task('666666666','clean class',TaskStatus.WAIT)
task_organize = Task('166666666', 'organize office', TaskStatus.EXECUTION)
task_report = Task('266666666', 'prepare report', TaskStatus.COMPLETE)
task_train = Task('366666666', 'conduct training', TaskStatus.WAIT)
task_manage = Task('466666666', 'manage team', TaskStatus.EXECUTION)
task_prepare = Task('566666666', 'prepare materials', TaskStatus.COMPLETE)
task_file = Task('766666666', 'file documents', TaskStatus.WAIT)
task_design = Task('866666666', 'design presentation', TaskStatus.EXECUTION)
task_research = Task('966666666', 'research topic', TaskStatus.COMPLETE)
task_present = Task('066666666', 'present report', TaskStatus.EXECUTION)
task_update = Task('606666666', 'update database', TaskStatus.COMPLETE)


general_worker_state = State.state_general_worker
generalEmployee_don = General_Worker('Don','101010101',40,"0540022563",general_worker_state,8000, seniority=Seniority.SENIOR , tasks_list=[task_research , task_update]  )
generalEmployee_ron = General_Worker('Ron', '191919191', 35, "0540022564",general_worker_state, 7500, seniority=Seniority.JUNIOR, tasks_list=[task_present,task_file])
generalEmployee_noa = General_Worker('Noa', '181818181', 29, "0540022565", general_worker_state, 9000, seniority=Seniority.MASTER, tasks_list=[task_train,task_update])
generalEmployee_avi = General_Worker('Avi', '010101010', 45, "0540022566", general_worker_state, 8500, seniority=Seniority.SENIOR, tasks_list=[task_clean])
generalEmployee_maya = General_Worker('Maya', '919191919', 38, "0540022567", general_worker_state, 7700, seniority=Seniority.EXPERT, tasks_list=[task_report,task_train])

manager_state = State.state_manager
manager_avi = Manager('Avi','110011001',55,"0501191822",manager_state,16000,Seniority.SENIOR,worker_list=[generalEmployee_avi,generalEmployee_maya,generalEmployee_don,generalEmployee_ron,generalEmployee_noa],teacher_list=[teacher_ben,teacher_sara,teacher_lior,teacher_yaron])


payment1 = Payment(12000,3000)
payment2 = Payment(25000,6000)

parent_state = State.state_parent
Parent_mimi = Parent('Mimi','991199110',34,"0554256577",parent_state,payment=payment1,childrenList=['emily','moshe'])
Parent_ronit = Parent('Ronit', '881188110', 42, "0554786543", parent_state,payment=payment2, childrenList=['david', 'sara'])


# רשימות המכילות אובייקטים בלבד
list_students = [Students_noa, Students_miki, Students_ron, Students_avi, Students_david, Students_ronit, Students_sara]
list_courses = [course_math, course_bio, course_english, course_economics, course_law]
list_teachers = [teacher_ben, teacher_sara, teacher_lior, teacher_yaron]
list_general_employees = [generalEmployee_don, generalEmployee_ron, generalEmployee_noa, generalEmployee_avi, generalEmployee_maya]
list_managers = [manager_avi]
list_parents = [Parent_mimi, Parent_ronit]
list_queues = [queue_bio, queue_law, queue_math, queue_english, queue_economics]

# יצירת DataFrame מכל רשימה על ידי המרת האובייקטים למילונים
df_students = pd.DataFrame([student.__dict__ for student in list_students])
df_courses = pd.DataFrame([course.__dict__ for course in list_courses])
df_teachers = pd.DataFrame([teacher.__dict__ for teacher in list_teachers])
df_general_employees = pd.DataFrame([worker.__dict__ for worker in list_general_employees])
df_managers = pd.DataFrame([manager.__dict__ for manager in list_managers])
df_parents = pd.DataFrame([parent.__dict__ for parent in list_parents])
df_queues = pd.DataFrame([queue.__dict__ for queue in list_queues])




sql_ = sql.sql()
sql_.create_db("university_dataBase_data")
sql_.db_name = "university_dataBase_data"

#חשוב: אסור שיהיה רווח בשם של הטבלאות !!!!!!!!!
dictionary_all = {
    'Course': "_course_id INT AUTO_INCREMENT PRIMARY KEY,_course_size INT,_name VARCHAR(100) NOT NULL,_student_list TEXT",

    'general_worker': "_id INT AUTO_INCREMENT PRIMARY KEY,_name VARCHAR(100) NOT NULL,_age INT NOT NULL,_phone_number VARCHAR(10),_status TEXT ,_salary INT ,_seniority TEXT ,_tasks_list TEXT",

    'Manager': "_id INT AUTO_INCREMENT PRIMARY KEY,_name VARCHAR(100) NOT NULL,_age INT NOT NULL,_phone_number VARCHAR(15),_status TEXT,_salary INT NOT NULL,_seniority TEXT,_worker_list TEXT,_teacher_list TEXT",

    'Parent': "_id INT AUTO_INCREMENT PRIMARY KEY,_name VARCHAR(100) NOT NULL,_age INT NOT NULL,_phone_number VARCHAR(15),_status TEXT,_payment TEXT, _childrenList TEXT",

    'Student': "_id INT AUTO_INCREMENT PRIMARY KEY,_name VARCHAR(100) NOT NULL,_age INT NOT NULL,_phone_number VARCHAR(15),_status TEXT,_grade_course TEXT,_registered TEXT",

    'Teacher': "_id INT AUTO_INCREMENT PRIMARY KEY,_name VARCHAR(100) NOT NULL,_age INT NOT NULL,_phone_number VARCHAR(15),_status TEXT,_salary INT,_seniority TEXT,_course_list TEXT,_student_list TEXT",

    'Wait_Queue': "_id INT AUTO_INCREMENT PRIMARY KEY,_course_of_queue TEXT,_queue TEXT"

}
for key,val in dictionary_all.items():
    sql_.create_table(key, val)


all_df_in_school = [df_students,df_teachers,df_courses,df_general_employees , df_managers , df_parents,df_queues ]
tableName =        ['Student' , 'Teacher', 'Course', 'general_worker' , 'Manager' , 'Parent', 'Wait_Queue']

for i, df_item in enumerate(all_df_in_school):
    table_name = tableName[i]
    sql_.add_df_to_table(table_name, df_item)


student_add_meni = Students('Meni','000000001',19 , "0524565766",stu_state,{1:88,3:99,5:94},Registered_Status.REGISTERED)
student_add_toni = Students('Toni','000000002',19, "0524019726",stu_state,{1:70,3:88,5:100},Registered_Status.REGISTERED)
course_add_python = Course('Python','000000003',course_size,[Students_miki,Students_ron,Students_avi,Students_noa,student_add_toni])
course_add_java = Course('Java','000000004',course_size,[Students_miki,Students_ron,Students_avi,Students_noa,student_add_toni])

df_students_add = pd.DataFrame([student_add_toni.__dict__, student_add_meni.__dict__])
df_course_add = pd.DataFrame([course_add_python.__dict__, course_add_java.__dict__])





print('-'*177)

#                                --------- all methods for manager is working---------
print('manager method : ')
manager_avi.manage_queue(queue_list=list_queues)
manager_avi.assign_teacher_to_course(teacher_yaron,course_bio)

new_course_for_add = Course('Music','000000011',course_size,[Students_miki,Students_noa,Students_ron,student_add_toni])
manager_avi.create_course(new_course_for_add,list_courses)

new_gen_employee_add = General_Worker('GenEmploy','000000111',55,"0524563557",general_worker_state,15000,Seniority.MASTER,[task_design,task_file])
manager_avi.create_general_employee(new_gen_employee_add , list_general_employees)

new_par_add = Parent('mushone' , '000011111' , 45,"0545263777",parent_state,payment2,['moran','fishi'])
manager_avi.create_parent(new_par_add,list_parents)

student_add = Students('moshir','000111111',23,'0524312455',stu_state,{1:88,2:88,3:99},Registered_Status.REGISTERED)
manager_avi.create_student(student_add,list_students)

new_teacher_add = Teacher('Moni','001111111',44,"055456377",teacher_state,7600,Seniority.EXPERT,[course_math,course_english],[Students_miki,Students_noa,Students_ron])
manager_avi.create_teacher(new_teacher_add,list_teachers)

manager_avi.assign_task_to_general_employee(generalEmployee_don,task_manage)

manager_avi.create_report_income_outcome('2020',540000,340000)

#                               --------- all methods for parent is working---------
print('-'*188)
print('parent method : ')

Parent_mimi.register_child_to_course_if_course_not_full(course_math,list_courses,list_queues,'Emily','010203040',30,"0524635666",stu_state)
#print(course_math)

Parent_mimi.show_child_info('emily',list_courses)# this method must be with register method
Parent_mimi.payment_report()
Parent_mimi.show_place_in_queue('emily',list_queues)
print('='*100)


#                                --------- all methods for student is working---------
list_students[1].show_place_in_queue(list_queues)
Students_noa.show_grade(list_courses)

#                                --------- all methods for teacher is working---------
print('-'*188)
print('teacher method : ')
teacher_ben.show_student_in_course()
teacher_lior.assign_student_to_course(Students_avi)
teacher_lior.assign_grade_to_student(Students_ron,44,course_math)
teacher_lior.assign_grade_to_student(Students_ron,99,course_english)
teacher_lior.problem_report()

print('-'*188)
print('general employee method : ')
generalEmployee_don.change_task_status_of_task(task_research,new_task_status=TaskStatus.WAIT)

add_data_to_sql('Student',df_students_add)
add_data_to_sql('Course',df_course_add)




'''
course_law.check_add_student_and_full_course_size(student_add_toni,list_queues)
print(list_queues[1].course_of_queue)
print(list_queues[1].queue)
'''

manager_avi.assign_student_to_queue(Students_avi,queue_math,list_queues)
manager_avi.alert_queue(list_queues,2)