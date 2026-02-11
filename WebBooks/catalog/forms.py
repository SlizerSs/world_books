from django import forms
from datetime import date
from django.forms import ModelForm
from .models import Book, BookInstance


class AuthorsForm(forms.Form):
    """класс формы для модели Author"""

    first_name = forms.CharField(label="Имя автора")
    last_name = forms.CharField(label="Фамилия автора")
    date_of_birth = forms.DateField(label="Дaтa рождения",
                                    initial=format(date.today()),
                                    widget=forms.widgets.DateInput(
                                        attrs={'type': 'date'}))
    date_of_death = forms.DateField(label="Дaтa смерти",
                                    initial=format(date.today()),
                                    widget=forms.widgets.DateInput(
                                        attrs={'type': 'date'}))


class BookInstanceForm(ModelForm):
    """класс формы для модели BookInstance"""

    class Meta:
        model = BookInstance
        fields = ['book', 'inv_num',
                  'imprint', 'status',
                  'due_back', 'borrower',
                  'postup_date']


class BookModelForm(ModelForm):
    """класс формы для модели Book"""

    class Meta:
        model = Book
        fields = ['title', 'genre',
                  'language', 'author',
                  'summary', 'isbn']
