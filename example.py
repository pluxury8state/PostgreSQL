import psycopg2 as pg


def create_db(cur): # создает таблицы

    cur.execute('''
    create table if not exists Student(student_id serial primary key,
        name  varchar(100) not null, gpa numeric(10,2), birth timestamp with time zone);
    ''')

    cur.execute('''
    create table if not exists Course(course_id serial primary key,
        name varchar(100) not null);
    ''')
    cur.execute('''
    insert into Course(name) values(%s);
    ''', ('Phyton',))
    cur.execute('''
        insert into Course(name) values(%s);
        ''', ('JavaScript',))
    cur.execute('''
        insert into Course(name) values(%s);
        ''', ('HTML',))
    cur.execute('''create table if not exists StudentsCourses(c_id integer references Course(course_id), s_id integer references Student(student_id),CONSTRAINT "s_c" PRIMARY KEY (c_id, s_id));''')


def get_students(cur,course_id): # возвращает студентов определенного курса
    cur.execute(f'''
    select * from StudentsCourses where c_id = {course_id}
    ''')
    court_of_stud = []
    for i in cur.fetchall():
        court_of_stud.append(i[1])
    return court_of_stud


def add_students(cur,course_id, students): # создает студентов и записывает их на курс

    cur.execute('''
    insert into Student (name, gpa, birth) values(%s, %s, %s);
    ''', (students['name'], students['gpa'], students['birth']))

    cur.execute('''
    SELECT * FROM Student WHERE student_id=(SELECT MAX(student_id) FROM Student);
    ''')

    id = cur.fetchone()[0]

    cur.execute(f'''
    insert into StudentsCourses(c_id, s_id) values(%s, %s)
    ''',(course_id, id))


def add_student(student):           # просто создает студента
    student_dict = {}

    studens_list = student.split(',')

    student_dict['name'] = studens_list[0]

    student_dict['gpa'] = float(studens_list[1])

    student_dict['birth'] = studens_list[2]

    student_dict['id_course_to_record'] = int(studens_list[3])

    return student_dict


def get_student(cur, stud_id):
    cur.execute(f'''
    select name, gpa, birth from Student where student_id = {stud_id}
    ''')
    print(cur.fetchone())


def delete_table(cur): # создает таблицы
    cur.execute('''
    drop table StudentsCourses
    ''')
    cur.execute('''
    drop table Student
    ''')
    cur.execute('''
    drop table Course
    ''')


def get_students_2(cur, course_id):
    cur.execute(f'''
    select s.name, s.gpa, s.birth, c.name from StudentsCourses sc 
    join Student s on s.student_id = sc.s_id
    join Course c on c.course_id = sc.c_id
    where sc.c_id = {course_id}
    ''')

    for i in cur.fetchall():
        print(i)




if __name__ == '__main__':
    params_to_connect = 'dbname=STUDENTSandCOURSES user=STUDENTSandCOURSES password=qwert host=pg.codecontrol.ru port=59432'

    with pg.connect(params_to_connect) as connection:
        cur = connection.cursor()

        delete_table(cur)#удаление таблиц

        create_db(cur)

        count = int(input('введите количество студентов, которых вы хотете внести в базу данных:'))

        students_to_identify_list = []

        while count != 0:

            #example = 'Moris,4.78,2000-04-01 15:56,1'

            student_info = input('введите имя, средний балл, дату рождения,курс ,на который нужно записать(через запятые):')

            students_to_identify_list.append(add_student(student_info))

            count -= 1

        for a in students_to_identify_list:
            add_students(cur, a['id_course_to_record'], a)


        cur.execute('''
        select * from Student;
        ''')

        print('\nДанные таблицы Студент:')
        for i in cur.fetchall():
            print(i)

        cur.execute('select * from StudentsCourses;')

        print('\nДанные таблицы Студент-Курс:')
        for i in cur.fetchall():
            print(i)

        course = int(input('введите id курса , студентов которого хотите просмотреть:'))

        for i in get_students(cur, course):
            get_student(cur, i)     # данные без склейки

        print('=====================================================================')

        get_students_2(cur, course)# нашел данные методом склейки таблиц(показывает название изучаемого языка, в отличие от get_student)
