from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name= models.CharField(max_length=255)

    class Meta:
        ordering = ('name',) #permite ordenar os items na BD
        verbose_name_plural = 'Categories'  #define que oo nome em plural é Categories e nao categorys como django metia automaticametne

    def __str__(self):     # define que o nome de cada categoria é o nome que lhe foi atribuido na pagina do administrador
        return self.name


class Article(models.Model):
    categories = models.ManyToManyField(Category, related_name='articles')
    title= models.CharField(max_length=355)
    description= models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='articles_images', blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='articles', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.URLField(max_length = 200, blank=True, null=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title
    

class ArticleView(models.Model): #CONFIGURAR MAIS TARDE
    article = models.ForeignKey(Article, related_name='views', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='viewed_articles', on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)
    was_viewed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('article', 'user')  # Prevent duplicate views by the same user

        
    

        