from django.shortcuts import render
from catalog.constants import LOAN_STATUS
# Create your views here.
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic
from django.shortcuts import get_object_or_404
from . import constants

def index(request):
    """View function for the home page of site."""
    
    # Generate counts of some of the main objects
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact=LOAN_STATUS['available']).count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    paginate_by = constants.BOOK_LIST_VIEW_PAGINATE
    context_object_name = 'book_list'
    template_name = 'catalog/book_list.html'

class BookDetailView(generic.DetailView):
    model = Book
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        context['copies'] = book.bookinstance_set.all()
        context['STATUS_AVAILABLE'] = constants.AVAILABLE
        context['STATUS_MAINTENANCE'] = constants.MAINTENANCE
        context['status_labels'] = dict(constants.LOAN_STATUS)
        return context

def book_detail_view(request, primary_key):
    book = get_object_or_404(Book, pk=primary_key)
    return render(request, 'catalog/book_detail.html', context={'book': book})
