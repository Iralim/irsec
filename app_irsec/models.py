from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories'
    )
    tree = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    picture = models.ImageField(upload_to='pictures', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Topic(models.Model):
    name = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    tree = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='topics')
    content = models.TextField()
    picture = models.ImageField(upload_to='pictures', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'
