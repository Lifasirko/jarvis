from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import date, timedelta
from django.db.models import Q

from .models import Contact
from .forms import ContactForm


@login_required
def contact_list_view(request, page=1):
    query = request.GET.get('query')
    today = date.today()
    next_week = today + timedelta(days=7)

    # Отримати всі контакти користувача
    contacts = Contact.objects.filter(user=request.user).order_by('name')

    # Контакти з днями народження протягом найближчого тижня
    upcoming_birthdays = []
    for contact in contacts:
        if contact.birthday:
            birthday_this_year = contact.birthday.replace(year=today.year)
            if today <= birthday_this_year <= next_week:
                upcoming_birthdays.append(contact)

    # Додамо відлагоджувальні повідомлення
    print(f"Upcoming birthdays: {upcoming_birthdays}")
    print(f"Today's date: {today}")
    print(f"Next week's date: {next_week}")

    # Фільтрація контактів за запитом
    if query:
        contacts = contacts.filter(Q(name__icontains=query) | Q(phone_number__icontains=query))

    # Сортування контактів перед пагінацією
    contacts = contacts.order_by('name')

    per_page = 10
    paginator = Paginator(contacts, per_page)
    contacts_on_page = paginator.page(page)

    context = {
        'upcoming_birthdays': upcoming_birthdays,
        'contacts': contacts_on_page,
        'query': query
    }

    if request.path == '/':
        return render(request, 'core/home.html', context)
    else:
        return render(request, 'contact_list.html', context)


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
        form = ContactForm()
    return render(request, 'add_contact.html', {'form': form})


@login_required
def update_contact_view(request, contact_id):
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
    return render(request, 'fulldata_contact.html', {"contact": contact})


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

    return render(request, 'contact_list.html',
                  {"contacts": upcoming_contacts, "query": query, "birthday_filter": days})
