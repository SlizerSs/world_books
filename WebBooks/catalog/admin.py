from django.contrib import admin
from .models import Author, Book, Genre, Language, Status, BookInstance


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'language', 'display_author')
    list_filter = ('genre', 'author')
    inlines = [BooksInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('book', 'status')
    fieldsets = (
        ('Экземпляр книги', {
            'fields': ('book', 'imprint', 'inv_num')}),
        ('Статус и окончание его действия', {
            'fields': ('status', 'due_back')
        })
    )


admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Status)
# admin.site.register(Author)
# admin.site.register(Book)
# admin.site.register(BookInstance)
