from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django_jalali.db import models as jmodels
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Person(models.Model):
    """
    مدل پایه برای اطلاعات پرسنلی (دانشجو، استاد، پرسنل، و...)
    """

    class Meta:
        verbose_name = "شخص"
        verbose_name_plural = "اشخاص"
        db_table = "Person"
        abstract = True

    GENDER_CHOICES = {
        True: "مرد",
        False: "زن",
    }
    MARITAL_STATUS_CHOICES = {
        True: 'مجرد',
        False: 'متاهل',
    }
    NATIONALITY_CHOICES = {
        True: "ایرانی",
        False: "اتباع",
    }
    BLOOD_TYPE_CHOICES = {
        "AB": "AB",
        "AB+": "AB+",
        "AB-": "AB-",
        'A': "A",
        "A+": "A+",
        "A-": "A-",
        'B': "B",
        "B+": "B+",
        "B-": "B-",
        'O': "O",
        "O+": "O+",
        "O-": "O-"
    }

    first_Name = models.CharField(
        max_length=50,
        validators=[RegexValidator(
            regex=r"^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,50}$",
            message="نام کاربر حداقل 3 حرف و فاقد عدد باید باشد"
        )],
        verbose_name="نام", )
    last_Name = models.CharField(
        max_length=50,
        validators=[RegexValidator(
            regex=r"^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,50}$",
            message="نام خانوادگی کاربر حداقل 3 حرف و فاقد عدد باید باشد"
        )],
        verbose_name="نام خانوادگی", )
    father_Name = models.CharField(
        max_length=50,
        validators=[RegexValidator(
            regex=r"^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,50}$",
            message="نام پدر، کاربر حداقل 3 حرف و فاقد عدد باید باشد"
        )],
        verbose_name="نام پدر")
    birth_Date = jmodels.jDateField(verbose_name="تاریخ تولد")
    gender = models.BooleanField(choices=GENDER_CHOICES, default=True, verbose_name="جنسیت")
    marital_status = models.BooleanField(choices=MARITAL_STATUS_CHOICES, default=True, verbose_name="وضعیت تاهل", )
    blood_Type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES, default="B+", verbose_name="گروه خونی")
    nationality = models.BooleanField(choices=NATIONALITY_CHOICES, default=True, verbose_name="ملیت")
    national_ID = models.CharField(
        max_length=10,
        primary_key=True,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='کد ملی باید ۱۰ رقم باشد'
            )
        ],
        verbose_name="کد ملی")
    profile_Image = models.ImageField(upload_to="account/profiles", default="account/profiles/default_User.png",
                                      verbose_name="عکس پروفایل")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    def __str__(self):
        return self.national_ID

class Employee(Person):
    """
    مدل پایه برای تمامی کارکنان دانشگاه
    """
    class Meta:
        verbose_name = "کارمند"
        verbose_name_plural = "کارمندان"
        db_table = "Employee"
        abstract = True
        unique_together = ['national_ID', 'personnel_code']

    EMPLOYMENT_STATUS_CHOICES = {
        'Full-time': 'تمام وقت',
        'Part-time': 'نیمه وقت',
        'Temporary': 'پاره وقت',
        'Contract': 'قراردادی'
    }

    Faculty = models.ForeignKey("Faculty", on_delete=models.PROTECT, verbose_name="دانشکده")
    personnel_code = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message="کد پرسنلی باید 10 رقم باشد"
            )
        ],
        verbose_name="کد پرسنلی")
    agreement_image = models.ImageField(upload_to="account/contracts", verbose_name="عکس قرارداد")
    contract_Date = jmodels.jDateField(verbose_name="تاریخ استخدام")
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="میزان حقوق (ریال)")
    employment_status = models.CharField(max_length=20, choices=EMPLOYMENT_STATUS_CHOICES, verbose_name="وضعیت استخدام")
    last_promotion_date = models.DateField(null=False, blank=True, verbose_name="تاریخ آخرین ترفیع")
    contract_end_date = models.DateField(null=False, blank=True, verbose_name="تاریخ پایان قرارداد (کارکنان قراردادی)")

class Professor(Employee):
    """
    استاد
    """
    class Meta:
        verbose_name = "استاد"
        verbose_name_plural = "اساتید"
        db_table = "Professor"

    ACADEMIC_RANK_CHOICES = {
        'Assistant_Professor': 'استادیار',
        'Associate_Professor': 'دانشیار',
        'Professor': 'استاد',
        'Lecturer': 'مدرس',
        'Instructor': 'مربی'
    }

    academic_rank = models.CharField(
        max_length=20,
        choices=ACADEMIC_RANK_CHOICES,
        verbose_name="مرتبه علمی"
    )
    Department = models.ManyToManyField("Department", verbose_name="دپارتمان")
    courses_taught = models.ManyToManyField('Course', blank=True, verbose_name="دروس ارایه شده")
    publications = models.TextField(blank=True, verbose_name="مقالات")

    def __str__(self):
        return f"{self.first_Name} - {self.last_Name}"

class Student(Person):
    """
    دانشجو
    """

    class Meta:
        verbose_name = "دانشجو"
        verbose_name_plural = "دانشجویان"
        db_table = "Student"
        unique_together = ['student_ID', 'national_ID']

    student_ID = models.CharField(
        max_length=14,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{14}$',
                message="کد دانشجویی باید 14 رقم باشد"
            )
        ],
        verbose_name="کد دانشجویی")
    enrollment_date = jmodels.jDateField(verbose_name="تاریخ ثبت ‌نام")
    DEGREE_CHOICES = [
        ('associate', 'کاردانی'),
        ('bachelor', 'کارشناسی'),
        ('master', 'کارشناسی ارشد'),
        ('phd', 'دکتری'),
    ]
    degree = models.CharField(max_length=20, choices=DEGREE_CHOICES, verbose_name="مقطع تحصیلی")
    is_active = models.BooleanField(default=True, verbose_name="وضعیت تحصیلی")
    major = models.CharField(max_length=50, verbose_name="رشته تحصیلی اصلی")
    minor = models.CharField(max_length=50, blank=True, verbose_name="رشته تحصیلی فرعی")
    gpa = models.DecimalField(max_digits=4, decimal_places=2, blank=True, verbose_name="میانگین نمرات")
    Department = models.ForeignKey("Department", on_delete=models.PROTECT, verbose_name="دپارتمان")

    def __str__(self):
        return f"{self.first_Name} - {self.last_Name} - {self.student_ID}"

class ContactInfo(models.Model):
    """
    مدل پایه برای اطلاعات تماس و ایمیل اشخاص
    """

    class Meta:
        verbose_name = "اطلاعات تماس"
        verbose_name_plural = "اطلاعات تماس"
        db_table = "ContactInfo"
        abstract = True

    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # person = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

class PhoneNumber(ContactInfo):
    """
    اطلاعات تماس
    """

    class Meta:
        verbose_name = "شماره تلفن"
        verbose_name_plural = "شماره تلفن ها"
        db_table = "Phone Number"

    PHONE_TYPE_CHOICES = [
        ('mobile', 'موبایل'),
        ('home', 'منزل'),
        ('work', 'محل کار'),
        ('other', 'سایر'),
    ]

    phone_type = models.CharField(
        max_length=10,
        choices=PHONE_TYPE_CHOICES,
        default="mobile",
        verbose_name="نوع تلفن"
    )
    number = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                regex=r'^(0|\+98)?(9\d{9}|[1-8]\d{7})$',
                message='شماره تلفن معتبر نیست'
            )
        ],
        verbose_name="شماره تلفن"
    )

    def __str__(self):
        return self.phone_type + "\t" + self.number

class Address(ContactInfo):
    """
    اطلاعات آدرس
    """

    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس ها"
        db_table = "Address"

    ADDRESS_TYPE_CHOICES = [
        ('home', 'منزل'),
        ('work', 'محل کار'),
        ('other', 'سایر'),
    ]
    PROVINCE_CHOICES = {'Tehran': 'تهران', 'Alborz': 'البرز', 'Isfahan': 'اصفهان', 'Fars': 'فارس',
                        'Khorasan_Razavi': 'خراسان رضوی', 'Kerman': 'کرمان', 'Mazandaran': 'مازندران',
                        'Zanjan': 'زنجان',
                        'Azarbaijan_Shargi': 'آذربایجان شرقی', 'Azarbaijan_Gharbi': 'آذربایجان غربی',
                        'Ardabil': 'اردبیل',
                        'Ilam': 'ایلام', 'Bushehr': 'بوشهر', 'Chahar_Mahal': 'چهارمحال و بختیاری', 'Gilan': 'گیلان',
                        'Golestan': 'گلستان', 'Khorasan_Shomali': 'خراسان شمالی', 'Khorasan_Jonobi': 'خراسان جنوبی',
                        'Khuzestan': 'خوزستان', 'Kermanshah': 'کرمانشاه', 'Kohgiluyeh': 'کهگیلویه و بویراحمد',
                        'Kurdistan': 'کردستان', 'Lorestan': 'لرستان', 'Markazi': 'مرکزی', 'Qazvin': 'قزوین',
                        'Qom': 'قم',
                        'Semnan': 'سمنان', 'Sistan': 'سیستان و بلوچستان', 'Yazd': 'یزد'}
    province = models.CharField(choices=PROVINCE_CHOICES, max_length=50, verbose_name="استان", default="Tehran")
    city = models.CharField(max_length=50, verbose_name="شهر")
    district = models.CharField(max_length=50, verbose_name="منطقه")
    street = models.CharField(max_length=50, verbose_name="خیابان")
    alley = models.CharField(max_length=50, verbose_name="کوچه")
    no = models.IntegerField(verbose_name="پلاک")
    floor = models.IntegerField(verbose_name="طبقه")
    post_ID = models.CharField(
        max_length=10,
        primary_key=True,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='کد پستی باید ۱۰ رقم باشد'
            )
        ],
        verbose_name="کدپستی")

    def __str__(self):
        return self.post_ID

class EmailAddress(ContactInfo):
    """
    آدرس ایمیل
    """

    class Meta:
        verbose_name = "آدرس ایمیل"
        verbose_name_plural = "آدرس‌ ایمیل ها"
        db_table = "Email Address"

    EMAIL_TYPE_CHOICES = [
        ('personal', 'شخصی'),
        ('work', 'کاری'),
        ('academic', 'دانشگاهی'),
        ('other', 'سایر'),
    ]

    email_type = models.CharField(
        max_length=10,
        choices=EMAIL_TYPE_CHOICES,
        verbose_name="نوع ایمیل"
    )

    email = models.EmailField(
        max_length=254,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                message='ایمیل باید معتبر باشد'
            )
        ],
        verbose_name="آدرس ایمیل")

    def __str__(self):
        return f"{self.email_type}: {self.email}"

class Course(models.Model):
    """
    اطلاعات دروس ارائه شده
    """
    class Meta:
        verbose_name = "درس"
        verbose_name_plural = "دروس"
        db_table = "Course"

    name = models.CharField(max_length=50, verbose_name="نام درس")
    code = models.CharField(
        max_length=7,
        primary_key=True,
        validators=[
            RegexValidator(
                regex=r'^\d{7}$',
                message="کد درس باید 7 رقم باشد"
            )
        ],
        verbose_name="کد درس")
    units = models.PositiveSmallIntegerField(
        verbose_name="تعداد واحد",
        validators=[
            RegexValidator(
                regex=r'[1-3]',
                message="تعداد واحد باید حداقل 1 و حداکثر 3 واحد باشد"
            )
        ])
    prerequisites = models.ManyToManyField('self', blank=True, verbose_name="پیش ‌نیاز ها")
    department = models.ForeignKey("Department", on_delete=models.PROTECT, verbose_name="دپارتمان")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    def __str__(self):
        return f"{self.name} - {self.code}"

class Faculty(models.Model):
    """
    دانشکده
    """
    class Meta:
        verbose_name = "دانشکده"
        verbose_name_plural = "دانشکده‌ها"
        db_table = "Faculty"

    name = models.CharField(max_length=100, verbose_name="نام دانشکده")
    code = models.CharField(
        max_length=10,
        primary_key=True,
        verbose_name="کد دانشکده")
    establishment_Date = jmodels.jDateField(verbose_name="تاریخ تاسیس")
    website = models.URLField(blank=True, verbose_name="وبسایت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    def __str__(self):
        return self.name

class Department(models.Model):
    """
    دپارتمان دانشکده
    """
    class Meta:
        verbose_name = "دپارتمان"
        verbose_name_plural = "دپارتمان ها"
        db_table = "Department"

    name = models.CharField(max_length=50, verbose_name="نام دپارتمان")
    code = models.CharField(
        max_length=10,
        primary_key=True,
        verbose_name="کد دپارتمان")
    faculty = models.ForeignKey('Department', on_delete=models.CASCADE, verbose_name="نام دانشکده مربوطه")
    established_Date = jmodels.jDateField(verbose_name="تاریخ تاسیس")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    def __str__(self):
        return f"{self.name} - {self.faculty}"
