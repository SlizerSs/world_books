from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound
from .models import Book, Author, BookInstance
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AuthorsForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView


class BookInstanceCreateFromBook(CreateView):
    model = BookInstance
    fields = '__all__'
    success_url = reverse_lazy('books')

    def get_initial(self):
        """Добавляет в initial объект Book"""

        initial = super().get_initial()
        book_id = self.kwargs.get('book_id')
        book = Book.objects.get(id=book_id)
        self.book = book
        initial['book'] = book
        return initial

    def get_success_url(self):
        """Редирект на страницу с конкретной Book"""

        return reverse_lazy('book-detail', kwargs={
            'pk': self.object.book.pk})


class BookInstanceCreate(CreateView):
    model = BookInstance
    fields = '__all__'
    success_url = reverse_lazy('books')


class BookInstanceUpdate(UpdateView):
    model = BookInstance
    fields = '__all__'

    def get_success_url(self):
        book_id = self.kwargs.get('book_id')
        book = Book.objects.get(id=book_id)
        self.book = book
        return reverse_lazy('book-detail', kwargs={
            'pk': self.object.book.pk})


class BookInstanceDelete(DeleteView):
    model = BookInstance

    def get_success_url(self):
        book_id = self.kwargs.get('book_id')
        book = Book.objects.get(id=book_id)
        self.book = book
        return reverse_lazy('book-detail', kwargs={
            'pk': self.object.book.pk})


class BookCreate(CreateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')


class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')


class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10


class BookDetailView(generic.DetailView, generic.list.MultipleObjectMixin):
    model = Book
    paginate_by = 3

    def get_context_data(self, **kwargs):
        object_list = BookInstance.objects.filter(book=self.get_object())
        context = super(BookDetailView, self).get_context_data(
            object_list=object_list,
            **kwargs)
        return context


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 3


class LoanedBooksByUserListView(generic.ListView, LoginRequiredMixin):
    """Представление для отображения списка забронированных
    экземплров книг для конкретного пользователя"""

    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        """Возвращает отсортированный список экземпляров книг по их статусу"""

        return BookInstance.objects.filter(
            borrower=self.request.user).filter(
                status__exact='2').order_by('due_back')


def index(request):
    """Представление начальной страницы сайта"""

    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(
        status__exact=2).count()
    num_authors = Author.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    return render(request, 'index.html',
                  context={'num_books': num_books,
                           'num_instances': num_instances,
                           'num_instances_available': num_instances_available,
                           'num_authors': num_authors,
                           'num_visits': num_visits,
                           })


def catalog_info(request):
    """Представление для отображения некоторой информации по сайту"""

    books = Book.objects.all()
    authors = Author.objects.all()
    return render(request, 'catalog/catalog_info.html',
                  context={'book_list': books,
                           'authors': authors})


def authors_add(request):
    """Представление для отображения списка Author
    и формой добавления нового Author"""

    author = Author.objects.all()
    authorsform = AuthorsForm()
    return render(request,
                  "catalog/authors_add.html",
                  {"form": authorsform, "author": author})


def create(request):
    """Представление для добавления Author в БД"""

    if request.method == "POST":
        author = Author()
        author.first_name = request.POST.get("first_name")
        author.last_name = request.POST.get("last_name")
        author.date_of_birth = request.POST.get("date_of_birth")
        author.date_of_death = request.POST.get("date_of_death")
        author.save()
        return HttpResponseRedirect("/authors_add/")


def delete(request, id):
    """Представление для удаления Author из БД"""

    try:
        author = Author.objects.get(id=id)
        author.delete()
        return HttpResponseRedirect("/authors_add/")
    except Author.DoesNotExist:
        return HttpResponseNotFound("<h2>Aвтop не найден</h2>")


def edit1(request, id):
    """Представление для изменения полей Author в БД"""

    author = Author.objects.get(id=id)
    if request.method == "POST":
        author.first_name = request.POST.get("first_name")
        author.last_name = request.POST.get("last_name")
        author.date_of_birth = request.POST.get("date_of_birth")
        author.date_of_death = request.POST.get("date_of_death")
        author.save()
        return HttpResponseRedirect("/authors_add/")
    else:
        return render(request, "edit1.html", {"author": author})
