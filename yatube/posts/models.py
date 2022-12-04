from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название группы')
    slug = models.SlugField(unique=True, verbose_name='Ссылка сайта после group/...')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='posts')
    group = models.ForeignKey(Group,
                              on_delete=models.CASCADE,
                              null=True,
                              blank=True)
    
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
