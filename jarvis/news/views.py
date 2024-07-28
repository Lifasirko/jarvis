from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.core.management import call_command

from .models import News, Category


def news_list(request, page=1):
    """
    Handles the news list display with pagination and category filtering.
    
    Args:
    request (HttpRequest): The request object used to generate this response.
    page (int): The page number to display, defaults to 1.
    
    Returns:
    HttpResponse: The rendered news list page with list of news articles and their categories.
    """
    news = News.objects.all().order_by('-published_time')
    categories = Category.objects.all()

    category = request.GET.get('category')
    if category:
        news = news.filter(category__id=category)

    per_page = 10
    paginator = Paginator(list(news), per_page=per_page)
    contacts_on_page = paginator.page(page)

    return render(request, 'news_list.html', {"all_news": contacts_on_page,
                                              "categories": categories,
                                              "selected_category": category,})


def news_detail(request, title):
    """
    Handles the display of a single news article.
    
    Args:
    request (HttpRequest): The request object used to generate this response.
    title (str): The title of the news article to display.
    
    Returns:
    HttpResponse: Renders the news detail template with the specified article.
    """
    news = News.objects.get(title=title)
    return render(request, 'news_detail.html', {'news': news})


def news_update(request):
    """
    Handles the update of news articles by calling a management command.
    
    Args:
    request (HttpRequest): The request object used to generate this response.
    
    Returns:
    HttpResponseRedirect: Redirects to the news list page after updating.
    """
    call_command('update_news')
    return redirect('news:news_list')
