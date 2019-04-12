import psycopg2 as pg

dbname = 'mydb'
user = 'rk0f'


def create_db():
    with pg.connect(dbname=dbname, user=user) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                create table IF NOT EXISTS Student (
                    id serial PRIMARY KEY,
                    name varchar(100) not null,
                    gpa numeric(10,2),
                    birth timestamp with time zone
                    );
                """)
            cur.execute("""
                create table IF NOT EXISTS Course (
                    id serial PRIMARY KEY,
                    name varchar(100) not null
                    );
                """)
            cur.execute("""
                create table IF NOT EXISTS Student_Course (
                    id serial PRIMARY KEY,
                    student_id INTEGER REFERENCES Student(id) ON DELETE CASCADE,
                    course_id INTEGER REFERENCES Course(id) ON DELETE CASCADE
                    );
                """)


def get_students(course_id):
    with pg.connect(dbname=dbname, user=user) as conn:
        with conn.cursor() as cur:
            cur.execute("""      
                select s.id, s.name, course.name from student s
                join student_course on student_course.student_id = s.id
                join course on course.id = (%s)""", (course_id,))
            return cur.fetchall()


def add_student(student):
    with pg.connect(dbname=dbname, user=user) as conn:
        with conn.cursor() as cur:
            cur.execute("""
               insert into student (name, gpa, birth) values (%s, %s, %s) RETURNING id;
               """, (student['name'], student['gpa'], student['birth']))
            return cur.fetchone()[0]


def add_student(student):
    with psycopg2.connect(NAME_DB) as conn:
        with conn.cursor() as curs:
            curs.execute("""insert into students (name, gpa, birth) values (%s, %s, %s) RETURNING id;""",
                         (student['name'], student['gpa'], student['birth']))
            return curs.fetchone()

def get_student(student_id):
    with pg.connect(dbname=dbname, user=user) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                select * from student where id = (%s);
                """, (student_id,))
            return cur.fetchone()


if __name__ == '__main__':
    students = [{'name': 'iii', 'gpa': 5, 'birth': '1994-01-01'},
                {'name': 'bbb', 'gpa': 5, 'birth': '1994-01-01'}]
    add_students(1, students)
