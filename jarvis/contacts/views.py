from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import date, timedelta
from django.db.models import Q

from .models import Contact
from .forms import ContactForm

# Create your views here.

@login_required
def contact_list_view(request, page=1):
    """
    Renders the contact list page. This view requires the user to be logged in.

    Args:
    request (HttpRequest): The request object used to generate this response.
    page (int): The page number of the contacts to display. Defaults to 1.

    Returns:
    HttpResponse: The rendered contact list page.

    Description:
    This function retrieves all contacts associated with the logged-in user,
    paginates them (10 contacts per page), and renders the contact list template
    with the contacts for the specified page.
    """
    contacts = Contact.objects.filter(user=request.user)
    per_page = 10
    paginator = Paginator(list(contacts), per_page=per_page)
    contacts_on_page = paginator.page(page)
    return render(request, 'contact_list.html', {"contacts" : contacts_on_page})


@login_required
def add_contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect('contacts:contact_list')
        else:
            return render(request, 'add_contact.html', {'form': form})

    return render(request, 'add_contact.html', {'form': ContactForm()})


@login_required
def update_contact_view(request, contact_id):
    """
    Handles the creation of a new contact.

    This view function manages both GET and POST requests for adding a new contact.
    It requires the user to be logged in.

    Args:
    request (HttpRequest): The request object containing metadata about the request.

    Returns:
    HttpResponse: Either a redirect to the contact list upon successful contact creation,
                  or the rendered 'add_contact.html' template with a form.
    """
    contact = get_object_or_404(Contact, id=contact_id, user=request.user)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect('contacts:contact_list')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'update_contact.html', {'form': form})


@login_required
def delete_contact_view(request, contact_id):
    """
    Handles the deletion of a specific contact.

    This view function manages both GET and POST requests for deleting a contact.
    It requires the user to be logged in and ensures that the contact belongs to the current user.

    Args:
    request (HttpRequest): The request object containing metadata about the request.
    contact_id (int): The ID of the contact to be deleted.

    Returns:
    HttpResponse: Either a redirect to the contact list upon successful deletion,
                  or the rendered 'delete_contact.html' template for confirmation.
    """
    contact = get_object_or_404(Contact, id=contact_id, user=request.user)
    if request.method == 'POST':
        contact.delete()
        return redirect('contacts:contact_list')
    return render(request, 'delete_contact.html', {'contact': contact})


@login_required
def fulldata_contact_view(request, contact_id):
    """
    Displays full details of a specific contact.

    This view function retrieves and displays all available data for a given contact.
    It requires the user to be logged in and ensures that the contact belongs to the current user.

    Args:
    request (HttpRequest): The request object containing metadata about the request.
    contact_id (int): The ID of the contact whose full details are to be displayed.

    Returns:
    HttpResponse: The rendered 'fulldata_contact.html' template with the contact's full details.
    """
    contact = get_object_or_404(Contact, id=contact_id, user=request.user)
    return render(request, 'fulldata_contact.html', {"contact" : contact})


@login_required
def search_contacts(request):
    """
    Searches and filters contacts based on user input and upcoming birthdays.

    This view function handles the search and filtering of contacts for the logged-in user.
    It considers both the search query and the number of days until the next birthday.

    Args:
    request (HttpRequest): The request object containing search parameters.

    Returns:
    HttpResponse: The rendered 'contact_list.html' template with filtered contacts.
    """
    query = request.GET.get('query')
    days = int(request.GET.get('birthday_filter'))

    today = date.today()
    end_date = today + timedelta(days=days)
    print(end_date)

    upcoming_contacts = []

    if query:
        contacts = Contact.objects.filter(
            Q(user=request.user) &
            (Q(name__icontains=query) | 
             Q(phone_number__icontains=query))
        )
    else:
        contacts = Contact.objects.filter(user=request.user)

    for contact in contacts:
        birthday_this_year = contact.birthday.replace(year=today.year)

        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)

        if birthday_this_year == end_date:
                upcoming_contacts.append(contact)

    return render(request, 'contact_list.html', {"contacts" : upcoming_contacts,  "query": query, "birthday_filter": days})