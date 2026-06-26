from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    USER_ROLE = (
    ('administrator', 'administrator'),
    ('teacher', 'teacher'),
    ('student', 'student')
    )
    role = models.CharField(max_length=13, choices=USER_ROLE, default='student')
    age = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(16), MaxValueValidator(90)])
    full_name = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    bio = models.TextField()
    phone_number = PhoneNumberField()


class Category(models.Model):
    category_name = models.CharField(max_length=72)

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory_name = models.CharField(max_length=72)

    def __str__(self):
        return self.subcategory_name


class Course(models.Model):
    course_name = models.CharField(max_length=72)
    description = models.TextField()
    category = models.CharField(max_length=32, unique=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    LEVEL_COURSE = (
    ('elementary', 'elementary'),
    ('average', 'average'),
    ('advanced', 'advanced')
    )
    level = models.CharField(max_length=10, choices=LEVEL_COURSE, default='elementary')
    price = models.PositiveSmallIntegerField(default=0)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    lesson = models.FileField(upload_to='lesson_videos/')

    def __str__(self):
        return self.course_name

    def get_avg_rating(self):
        reviews = self.users_reviews.all()
        if reviews.exists():
            return sum([i.stars for i in reviews]) / reviews.count()
        return 0

    def get_count_rating(self):
        reviews = self.users_reviews.all()
        if reviews.exists():
            return reviews.count()
        return 0


class CourseImage(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_images')
    course_image = models.ImageField(upload_to='course_images/')


class Lesson(models.Model):
    title = models.CharField(max_length=72)
    video_url = models.URLField(null=True, blank=True)
    video_file = models.FileField(upload_to='video_fields/', null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_lessons')

    def __str__(self):
        return self.title


class Assignment(models.Model):
    title = models.CharField(max_length=72)
    description = models.TextField()
    due_date = models.DateTimeField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_assignments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_assignments')

    def __str__(self):
        return self.title


class SolveAssignment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='students_name')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='assignments')
    solve_file = models.FileField(upload_to='solve_fields/', null=True, blank=True)
    solve_text = models.TextField(null=True, blank=True)


class Exam(models.Model):
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_exams')
    passing_score = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    duration = models.DateTimeField()


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='exam')
    question_name = models.CharField(max_length=250)


class Variants(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question')
    QUESTION_VARIANTS = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D')
    )
    variant = models.CharField(max_length=1, choices=QUESTION_VARIANTS, null=True, blank=True)
    variant_text = models.TextField()
    True_answer = models.BooleanField(default=False)


class Certificate(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course')
    issued_at = models.DateField(auto_now_add=True)
    certificate_url = models.URLField(null=True, blank=True)
    certificate_file = models.FileField(null=True, blank=True, upload_to='certificate_fields/')


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_reviews')
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i))for i in range(1, 6)], null=True, blank=True)
    comment = models.TextField()
    created_at = models.DateField(auto_now_add=True)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)




