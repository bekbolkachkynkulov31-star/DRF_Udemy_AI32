from .models import Course, Category, SubCategory
from modeltranslation.translator import TranslationOptions, register

@register(Course)
class ProductTranslationOptions(TranslationOptions):
    fields = ('course_name', 'description')

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)

@register(SubCategory)
class SubCategoryTranslationOptions(TranslationOptions):
    fields = ('subcategory_name',)