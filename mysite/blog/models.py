from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                     self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=250)  # CharField translates to a VARCHAR column in SQL
    slug = models.SlugField(max_length=250,  # Field intended to be used in a url.
                            unique_for_date='publish')
    author = models.ForeignKey(User,  # This field defines a many-to-one relationship.
                               on_delete=models.CASCADE,  # If the user is deleted, Django will delete all related
                               # posts.
                               related_name='blog_posts')  # Allows access to related objects easily.

    body = models.TextField()  # Body of the post.Translates to a TEXT column in SQL.
    publish = models.DateTimeField(default=timezone.now)  # DatetimeField indicates when the post as published.
    created = models.DateTimeField(auto_now_add=True)  # DatetimeField indicates when the post as created.
    # Auto_now_add=True saves the date automatically when creating an object.

    updated = models.DateTimeField(auto_now=True)  # Saves the date the for last update. Auto_now, saves the
    # date when saving the object

    status = models.CharField(max_length=10,  # Shows the status of the post.
                              choices=STATUS_CHOICES,
                              default='draft')

    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])

    class Meta:  # Contains metadata. Tells Django to sort result by the publish field in descending
        # order(-).
        ordering = ('-publish',)

    def __str__(self):  # Human-readable representation of the object.
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created', )

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'




