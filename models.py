from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

class Faculty(models.Model):
    """
    دانشکده‌های دانشگاه را نگهداری می‌کند.
    
    این مدل برای ذخیره اطلاعات دانشکده‌های مختلف دانشگاه استفاده می‌شود.
    
    نمونه داده:
        - نام: "دانشکده مهندسی کامپیوتر", کد: "CE"
        - نام: "دانشکده برق", کد: "EE"
        - نام: "دانشکده مکانیک", کد: "ME"
    """
    name = models.CharField(max_length=100, verbose_name="نام دانشکده")
    code = models.CharField(max_length=10, unique=True, verbose_name="کد دانشکده")
    
    class Meta:
        verbose_name = "دانشکده"
        verbose_name_plural = "دانشکده‌ها"
    
    def __str__(self):
        return self.name

class Person(models.Model):
    """
    مدل پایه برای اطلاعات پرسنلی دانشجویان و اساتید
    """
    GENDER_CHOICES = [
        ('M', 'مرد'),
        ('F', 'زن'),
    ]
    MARITAL_STATUS_CHOICES = [
        ('S', 'مجرد'),
        ('M', 'متاهل'),
    ]
    TYPE_CHOICES = [
        ('student', 'دانشجو'),
        ('professor', 'استاد'),
    ]

    first_name = models.CharField(max_length=100, verbose_name="نام")
    last_name = models.CharField(max_length=100, verbose_name="نام خانوادگی")
    national_code = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(regex=r'^\d{10}$', message='کد ملی باید ۱۰ رقم باشد')],
        verbose_name="کد ملی"
    )
    birth_date = models.DateField(verbose_name="تاریخ تولد")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="جنسیت")
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_CHOICES, verbose_name="وضعیت تاهل")
    person_type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name="نوع شخص")
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT, verbose_name="دانشکده")
    phone = models.CharField(
        max_length=11,
        validators=[RegexValidator(regex=r'^(0|\+98)?(9\d{9}|[1-8]\d{7})$', message='شماره تلفن معتبر نیست')],
        verbose_name="شماره تلفن"
    )
    email = models.EmailField(unique=True, verbose_name="ایمیل")
    address = models.TextField(verbose_name="آدرس")
    postal_code = models.CharField(
        max_length=10,
        validators=[RegexValidator(regex=r'^\d{10}$', message='کد پستی باید ۱۰ رقم باشد')],
        verbose_name="کد پستی"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        verbose_name = "شخص"
        verbose_name_plural = "اشخاص"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def clean(self):
        try:
            if not self.postal_code.isdigit() or len(self.postal_code) != 10:
                raise ValidationError(_('کد پستی باید ۱۰ رقم باشد'))
        except Exception as e:
            raise ValidationError(f'خطا در اعتبارسنجی کد پستی: {str(e)}')

class Student(models.Model):
    """
    اطلاعات تکمیلی دانشجویان
    """
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name="شخص")
    student_number = models.CharField(max_length=10, unique=True, verbose_name="شماره دانشجویی")
    entry_year = models.IntegerField(verbose_name="سال ورود")
    DEGREE_CHOICES = [
        ('associate', 'کاردانی'),
        ('bachelor', 'کارشناسی'),
        ('master', 'کارشناسی ارشد'),
        ('phd', 'دکتری'),
    ]
    degree = models.CharField(max_length=20, choices=DEGREE_CHOICES, verbose_name="مقطع تحصیلی")
    is_active = models.BooleanField(default=True, verbose_name="وضعیت تحصیلی")

    class Meta:
        verbose_name = "دانشجو"
        verbose_name_plural = "دانشجویان"

    def __str__(self):
        return f"{self.person.first_name} {self.person.last_name} - {self.student_number}"

class Professor(models.Model):
    """
    اطلاعات تکمیلی اساتید
    """
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name="شخص")
    personnel_code = models.CharField(max_length=10, unique=True, verbose_name="کد پرسنلی")
    ACADEMIC_RANK_CHOICES = [
        ('assistant', 'استادیار'),
        ('associate', 'دانشیار'),
        ('full', 'استاد تمام'),
    ]
    academic_rank = models.CharField(max_length=50, choices=ACADEMIC_RANK_CHOICES, verbose_name="مرتبه علمی")
    hire_date = models.DateField(verbose_name="تاریخ استخدام")

    class Meta:
        verbose_name = "استاد"
        verbose_name_plural = "اساتید"

    def __str__(self):
        return f"{self.person.first_name} {self.person.last_name} - {self.personnel_code}"

# class Course(models.Model):
#     """
#     اطلاعات دروس ارائه شده در دانشگاه
#     """
#     name = models.CharField(max_length=100, verbose_name="نام درس")
#     code = models.CharField(max_length=10, unique=True, verbose_name="کد درس")
#     units = models.PositiveSmallIntegerField(verbose_name="تعداد واحد")
#     faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT, verbose_name="دانشکده")
#     prerequisite = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, verbose_name="پیش‌نیاز")
    
#     class Meta:
#         verbose_name = "درس"
#         verbose_name_plural = "دروس"
    
#     def __str__(self):
#         return f"{self.name} ({self.code})"

# class Semester(models.Model):
#     """
#     اطلاعات ترم‌های تحصیلی
#     """
#     SEMESTER_CHOICES = [
#         ('1', 'نیمسال اول'),
#         ('2', 'نیمسال دوم'),
#         ('3', 'ترم تابستان'),
#     ]
    
#     year = models.IntegerField(verbose_name="سال تحصیلی")
#     semester = models.CharField(max_length=1, choices=SEMESTER_CHOICES, verbose_name="نیمسال")
#     is_active = models.BooleanField(default=False, verbose_name="ترم فعال")
    
#     class Meta:
#         verbose_name = "ترم تحصیلی"
#         verbose_name_plural = "ترم‌های تحصیلی"
#         unique_together = ['year', 'semester']
    
#     def __str__(self):
#         return f"{self.get_semester_display()} {self.year}"

# class ClassSchedule(models.Model):
#     """
#     برنامه زمانی کلاس‌های درسی
#     """
#     DAYS_OF_WEEK = [
#         ('0', 'شنبه'),
#         ('1', 'یکشنبه'),
#         ('2', 'دوشنبه'),
#         ('3', 'سه‌شنبه'),
#         ('4', 'چهارشنبه'),
#         ('5', 'پنج‌شنبه'),
#     ]
    
#     course = models.ForeignKey(Course, on_delete=models.PROTECT, verbose_name="درس")
#     professor = models.ForeignKey(Professor, on_delete=models.PROTECT, verbose_name="استاد")
#     semester = models.ForeignKey(Semester, on_delete=models.PROTECT, verbose_name="ترم")
#     capacity = models.PositiveIntegerField(verbose_name="ظرفیت")
#     day = models.CharField(max_length=1, choices=DAYS_OF_WEEK, verbose_name="روز")
#     start_time = models.TimeField(verbose_name="زمان شروع")
#     end_time = models.TimeField(verbose_name="زمان پایان")
    
#     class Meta:
#         verbose_name = "کلاس درسی"
#         verbose_name_plural = "کلاس‌های درسی"
    
#     def clean(self):
#         try:
#             if self.start_time >= self.end_time:
#                 raise ValidationError(_('زمان شروع باید قبل از زمان پایان باشد'))
#         except Exception as e:
#             raise ValidationError(f'خطا در بررسی زمان کلاس: {str(e)}')
    
#     def __str__(self):
#         return f"{self.course.name} - {self.professor}"

# class Enrollment(models.Model):
#     """
#     ثبت‌نام دانشجویان در کلاس‌ها
#     """
#     student = models.ForeignKey(Student, on_delete=models.PROTECT, verbose_name="دانشجو")
#     class_schedule = models.ForeignKey(ClassSchedule, on_delete=models.PROTECT, verbose_name="کلاس")
#     grade = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name="نمره")
#     enrollment_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت‌نام")
    
#     class Meta:
#         verbose_name = "ثبت‌نام"
#         verbose_name_plural = "ثبت‌نام‌ها"
#         unique_together = ['student', 'class_schedule']
    
#     def clean(self):
#         try:
#             if self.grade is not None and (self.grade < 0 or self.grade > 20):
#                 raise ValidationError(_('نمره باید بین 0 تا 20 باشد'))
#         except Exception as e:
#             raise ValidationError(f'خطا در بررسی نمره: {str(e)}')
    
#     def __str__(self):
#         return f"{self.student} - {self.class_schedule.course}"
