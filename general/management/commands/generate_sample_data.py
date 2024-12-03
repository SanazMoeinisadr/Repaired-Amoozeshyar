from django.core.management.base import BaseCommand
from django.db import transaction
from general.models import Faculty, Professor, Student, Course, Semester, ClassSchedule, Enrollment
from datetime import date, time, timedelta
import random

class Command(BaseCommand):
    help = 'Generates sample data for university database'

    def handle(self, *args, **kwargs):
        try:
            with transaction.atomic():
                self.stdout.write('Generating sample data...')
                
                # ایجاد دانشکده‌ها
                faculties = [
                    ('دانشکده مهندسی کامپیوتر', 'CE'),
                    ('دانشکده مهندسی برق', 'EE'),
                    ('دانشکده مهندسی مکانیک', 'ME'),
                    ('دانشکده علوم پایه', 'SC'),
                    ('دانشکده مدیریت', 'MG'),
                ]
                
                faculty_objects = []
                for name, code in faculties:
                    faculty = Faculty.objects.create(name=name, code=code)
                    faculty_objects.append(faculty)
                
                # ایجاد اساتید
                first_names = ['علی', 'محمد', 'حسین', 'رضا', 'مریم', 'زهرا', 'فاطمه', 'سارا']
                last_names = ['محمدی', 'حسینی', 'رضایی', 'کریمی', 'موسوی', 'هاشمی', 'علوی', 'نوری']
                academic_ranks = ['assistant', 'associate', 'full']
                
                professor_objects = []
                for i in range(20):
                    professor = Professor.objects.create(
                        first_name=random.choice(first_names),
                        last_name=random.choice(last_names),
                        national_code=f'00{str(i+1).zfill(8)}',
                        birth_date=date(1960 + random.randint(0, 30), 
                                     random.randint(1, 12),
                                     random.randint(1, 28)),
                        gender=random.choice(['M', 'F']),
                        marital_status=random.choice(['S', 'M']),
                        faculty=random.choice(faculty_objects),
                        personnel_code=f'P{str(i+1).zfill(5)}',
                        academic_rank=random.choice(academic_ranks),
                        hire_date=date(2000 + random.randint(0, 20), 
                                    random.randint(1, 12),
                                    random.randint(1, 28))
                    )
                    professor_objects.append(professor)
                
                # ایجاد دانشجویان
                student_objects = []
                for i in range(50):
                    entry_year = 1395 + random.randint(0, 6)
                    student = Student.objects.create(
                        first_name=random.choice(first_names),
                        last_name=random.choice(last_names),
                        national_code=f'11{str(i+1).zfill(8)}',
                        birth_date=date(1375 + random.randint(0, 10), 
                                     random.randint(1, 12),
                                     random.randint(1, 28)),
                        gender=random.choice(['M', 'F']),
                        marital_status=random.choice(['S', 'M']),
                        faculty=random.choice(faculty_objects),
                        student_number=f'{entry_year}{str(i+1).zfill(5)}',
                        entry_year=entry_year,
                        degree=random.choice(['bachelor', 'master', 'phd']),
                        is_active=random.choice([True, True, True, False])  # 75% احتمال فعال بودن
                    )
                    student_objects.append(student)
                
                # ایجاد دروس
                courses_data = [
                    ('برنامه‌نویسی پیشرفته', 'CE101', 3),
                    ('پایگاه داده', 'CE102', 3),
                    ('هوش مصنوعی', 'CE103', 3),
                    ('شبکه‌های کامپیوتری', 'CE104', 3),
                    ('سیستم‌های عامل', 'CE105', 3),
                    ('مدارهای الکتریکی', 'EE101', 3),
                    ('الکترونیک', 'EE102', 3),
                    ('مکانیک سیالات', 'ME101', 3),
                    ('ریاضی ۱', 'SC101', 3),
                    ('فیزیک ۱', 'SC102', 3),
                ]
                
                course_objects = []
                for name, code, units in courses_data:
                    course = Course.objects.create(
                        name=name,
                        code=code,
                        units=units,
                        faculty=next(f for f in faculty_objects if f.code == code[:2])
                    )
                    course_objects.append(course)
                
                # ایجاد ترم‌ها
                semester_objects = []
                for year in range(1400, 1403):
                    for sem in ['1', '2', '3']:
                        semester = Semester.objects.create(
                            year=year,
                            semester=sem,
                            is_active=(year == 1402 and sem == '1')
                        )
                        semester_objects.append(semester)
                
                # ایجاد کلاس‌ها
                class_schedule_objects = []
                for semester in semester_objects[-3:]:  # فقط برای سه ترم آخر
                    for course in course_objects:
                        for _ in range(random.randint(1, 2)):  # هر درس 1 یا 2 گروه
                            class_schedule = ClassSchedule.objects.create(
                                course=course,
                                professor=random.choice(professor_objects),
                                semester=semester,
                                capacity=random.randint(20, 40),
                                day=str(random.randint(0, 4)),
                                start_time=time(random.randint(8, 15), 0),
                                end_time=time(random.randint(16, 18), 0)
                            )
                            class_schedule_objects.append(class_schedule)
                
                # ایجاد ثبت‌نام‌ها
                for student in student_objects:
                    # هر دانشجو در 3-5 کلاس ثبت‌نام می‌کند
                    for class_schedule in random.sample(class_schedule_objects, 
                                                      random.randint(3, 5)):
                        Enrollment.objects.create(
                            student=student,
                            class_schedule=class_schedule,
                            grade=random.uniform(10, 20) if random.random() > 0.2 else None
                        )
                
                self.stdout.write(self.style.SUCCESS('Sample data generated successfully!'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error generating sample data: {str(e)}'))
            raise e 