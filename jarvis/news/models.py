from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique = True)

    def __str__(self):
        return self.name
    

class News(models.Model):
    """
    Model to store news articles.

    Attributes:
        source (CharField): The source of the news article. Maximum length of 255 characters.
        title (CharField): The title of the news article. Maximum length of 255 characters.
        content (TextField): The content of the news article.
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