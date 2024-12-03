from rest_framework import serializers
from .models import Faculty, Professor, Student, Course, Semester, ClassSchedule, Enrollment

class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = '__all__'

class ProfessorSerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source='faculty.name', read_only=True)
    
    class Meta:
        model = Professor
        fields = ['id', 'first_name', 'last_name', 'national_code', 'birth_date',
                 'gender', 'marital_status', 'faculty', 'faculty_name',
                 'personnel_code', 'academic_rank', 'hire_date']
        read_only_fields = ['created_at', 'updated_at']

class StudentSerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source='faculty.name', read_only=True)
    
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'national_code', 'birth_date',
                 'gender', 'marital_status', 'faculty', 'faculty_name',
                 'student_number', 'entry_year', 'degree', 'is_active']
        read_only_fields = ['created_at', 'updated_at']

class CourseSerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source='faculty.name', read_only=True)
    prerequisites_list = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'code', 'units', 'faculty', 'faculty_name',
                 'prerequisites', 'prerequisites_list']

    def get_prerequisites_list(self, obj):
        return [{'id': course.id, 'name': course.name} for course in obj.prerequisites.all()]

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = '__all__'

class ClassScheduleSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    professor_name = serializers.CharField(source='professor.get_full_name', read_only=True)
    semester_display = serializers.CharField(source='semester.__str__', read_only=True)

    class Meta:
        model = ClassSchedule
        fields = ['id', 'course', 'course_name', 'professor', 'professor_name',
                 'semester', 'semester_display', 'capacity', 'day',
                 'start_time', 'end_time']

class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    course_name = serializers.CharField(source='class_schedule.course.name', read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'student_name', 'class_schedule', 'course_name',
                 'grade', 'enrollment_date']
        read_only_fields = ['enrollment_date'] 