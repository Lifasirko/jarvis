from django.db import models


# Create your models here.

class Category(models.Model):
    """
    Model to store categories of the articles.
    
    Attributes:
    name (CharField): The name of the category. Maximum length of 100 characters, must be unique.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class News(models.Model):
    """
    Model to store news articles.
    
    Attributes:
    source (URLField): The URL source of the news article. Maximum length of 255 characters, must be unique.
    title (TextField): The title of the news article. Must be unique.
    caption (TextField): A brief description or summary of the article. Can be null.
    category (ForeignKey): Relates to the Category model, establishing a many-to-one relationship.
    content (TextField): The full content of the news article.
    author (CharField): The name of the article's author. Maximum length of 255 characters.
    image (URLField): The URL of an associated image. Maximum length of 255 characters, can be null.
    image_caption (TextField): A caption for the associated image. Can be null.
    published_time (DateTimeField): The date and time when the article was published. Can be null.
    """
    source = models.URLField(max_length=255, unique=True)
    title = models.TextField(unique=True)
    caption = models.TextField(null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.CharField(max_length=255)
    image = models.URLField(max_length=255, null=True)
    image_caption = models.TextField(null=True)
    published_time = models.DateTimeField(null=True)
