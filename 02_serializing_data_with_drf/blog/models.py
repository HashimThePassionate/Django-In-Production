from django.db import models


class BaseTimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Blog(BaseTimeStampModel):
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    author = models.ForeignKey('author.Author', related_name='author_blogs', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tags', related_name='blog_tags')
    blog_cover_image = models.OneToOneField('CoverImage', related_name='blog', on_delete=models.PROTECT)

    def __str__(self):
        return self.title


class CoverImage(BaseTimeStampModel):
    image_link = models.URLField()


class Tags(BaseTimeStampModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name