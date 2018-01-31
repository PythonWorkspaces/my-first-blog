from django.db import models
from django.utils import timezone
from django.urls import reverse_lazy

class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE,)
    title = models.CharField(max_length=200)
    text = models.TextField()
    photo = models.ImageField(upload_to='%Y/%m/%d/orig', blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def delete(self, *args, **kwargs):
        self.photo.delete()
        super(Post, self).delete(*args, **kwargs)

    def get_absolute_url(self):
        url = reverse_lazy('', kwargs={'pk': self.pk})
        return url

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments', on_delete=models.CASCADE,)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
