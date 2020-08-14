from django.views import generic
from django.shortcuts import render
from . import models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse,reverse_lazy
import datetime
from .forms import RenewBookForm



class Home(generic.TemplateView):
    template_name = 'Djapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_books'] = models.Book.objects.all().count()
        context['num_instances'] = models.BookInstance.objects.all().count()
        context['num_instances_available'] = models.BookInstance.objects.filter(status__exact='a').count()
        context['num_authors'] = models.Author.objects.count()
        return context

class BookListView(generic.ListView):
    model = models.Book
    context_object_name = 'book_list'
    template_name = 'Djapp/book_list.html'

class BookDetailView(generic.DetailView):
    model = models.Book
    context_object_name = 'book'
    template_name = 'Djapp/book_detail.html'

class AuthorListView(generic.ListView):
    model = models.Author
    context_object_name = 'author_list'
    template_name = 'Djapp/author_list.html'

class AuthorDetailView(generic.DetailView):
    model = models.Author
    context_object_name = 'author'
    template_name = 'Djapp/author_detail.html'

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = models.BookInstance
    template_name ='Djapp/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return models.BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

#@permission_required('Djapp.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst=get_object_or_404(models.BookInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instancecatalog and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('my-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'Djapp/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})

class AuthorCreate(generic.CreateView):
    model = models.Author
    fields = '__all__'
    initial={'date_of_death':'05/01/2018',}

class AuthorUpdate(generic.UpdateView):
    model = models.Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']

class AuthorDelete(generic.DeleteView):
    model = models.Author
    success_url = reverse_lazy('Djapp:authors')

# def index(request):
#     """
#     View function for home page of site.
#     """
#     # Generate counts of some of the main objects
#     num_books=models.Book.objects.all().count()
#     num_instances=models.BookInstance.objects.all().count()
#     # Available books (status = 'a')
#     num_instances_available=models.BookInstance.objects.filter(status__exact='a').count()
#     num_authors=models.Author.objects.count()  # The 'all()' is implied by default.
#
#     # Render the HTML template index.html with the data in the context variable
#     return render(
#         request,
#         'Djapp/index.html',
#         context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors},
#     )
