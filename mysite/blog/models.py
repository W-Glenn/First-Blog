from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse

#custom manager to retrieve all "published" status posts
class PublishedManager(models.Manager):
    def get_queryset(self):
        return(
            super().get_queryset().filter(status=Post.Status.PUBLISHED)
        )
    

class Post(models.Model):
    class Status(models.TextChoices): #gives 2 status option
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250) #sets title to a character field of 205
    slug = models.SlugField( #slug=url in browser.
        max_length=250,
        unique_for_date="publish" #requires a unique publish date for the url
        ) 
    author = models.ForeignKey( #foreign key links models together ie. all blog posts belong to this user, if deleted, delete all posts.
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, #cascade = everything associated with will be deleted
        related_name="blog_posts"
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField( #creates the status drop down in the admin window.)
        max_length=2, #Says there will only be a max of 2 options
        choices=Status, #the choices are from the Status Class ^^^
        default=Status.DRAFT #default option displayed
    )

    objects = models.Manager() #default model manager (must be added if using custom manager: says - hey use this, unless its published then use that)
    published = PublishedManager() #custom model manager for "published" posts

    class Meta: #sets the default ordering for query results.
        ordering = ['-publish'] #means descending order by publish date.
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self): 
        return self.title

    def get_absolute_url(self): #defines the canonical URL for each Post object... "best practice"
        return reverse(
            "blog:post_detail",
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug
            ]
        )
    
class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["created"]
        indexes = [
            models.Index(fields=['created']),
        ] 
    
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'