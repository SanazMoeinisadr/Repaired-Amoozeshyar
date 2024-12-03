from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (FacultyViewSet, ProfessorViewSet, StudentViewSet,
                   CourseViewSet, SemesterViewSet, ClassScheduleViewSet,
                   EnrollmentViewSet)

router = DefaultRouter()
router.register(r'faculties', FacultyViewSet)
router.register(r'professors', ProfessorViewSet)
router.register(r'students', StudentViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'semesters', SemesterViewSet)
router.register(r'class-schedules', ClassScheduleViewSet)
router.register(r'enrollments', EnrollmentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
] 