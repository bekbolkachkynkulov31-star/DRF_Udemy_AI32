from django.contrib import admin

from .models import (User, Category, SubCategory, Course, CourseImage, Lesson, Assignment,
                     SolveAssignment, Exam, Question, Variants, Certificate,
                     Review, Favorite)


class CourseImageInline(admin.TabularInline):
    model = CourseImage
    extra = 1


admin.site.register(User)
admin.site.register(Lesson)
admin.site.register(Assignment)
admin.site.register(SolveAssignment)
admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(Variants)
admin.site.register(Certificate)
admin.site.register(Review)
admin.site.register(Favorite)


from modeltranslation.admin import TranslationAdmin
@admin.register( Category, SubCategory)
class AllAdmin(TranslationAdmin):

    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
                'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

@admin.register(Course)
class ProductAdmin(TranslationAdmin):
    inlines = [CourseImageInline]

    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
                'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }





