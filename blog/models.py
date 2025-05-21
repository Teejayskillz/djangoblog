from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User  # Assuming the author is a User
from django.utils.text import slugify
import os
from django.utils.timezone import now
from django.utils import timezone
from PIL import Image
from django.core.exceptions import ValidationError

def upload_thumbnail_to(instance, filename):
    now = timezone.now()
    base, ext = os.path.splitext(filename.lower())
    return f'posts/{now:%Y/%m/%d}/thumbnails/{slugify(instance.title)}_thumb{ext}'


def validate_image_size(value):
    limit = 2 * 1024 * 1024  # 2MB
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 2MB.')

#image upload function 
def upload_to(instance, filename):
    """Generate path using current date if created_at doesn't exist"""
    date_path = now().strftime('%Y/%m/%d') if not instance.id else instance.created_at.strftime('%Y/%m/%d')
    return os.path.join('posts', date_path, filename)

#tag
class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)


    def __str__(self):
        return self.name
    
# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# Post Model
class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField()
    image = models.ImageField( upload_to=upload_to,
        validators=[validate_image_size],
        blank=True,
        null=True)
    thumbnail = models.ImageField(upload_to=upload_thumbnail_to, null=True, blank=True, max_length=1000) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
  # Assuming you will define a Tag model
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)  # Fixed typo here
    dislikes = models.IntegerField(default=0)
    #comments = models.IntegerField(default=0)
    published_at = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming the author is a User model


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.slug)])

    def get_comments(self):
        return self.comment_set.all()

    def get_tags(self):
        return self.tags.all()

    def get_category(self):
        return self.category.name

    def get_author(self):
        return self.author.username
    
    def save(self, *args, **kwargs):
        
        if not self.slug:  # Only generate slug if empty
            self.slug = slugify(self.title)
            # Handle potential duplicates
            original_slug = self.slug
            counter = 1
            while Post.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            size = (300, 200)  # Define your thumbnail size
            img.thumbnail(size)
            thumb_filename = os.path.basename(self.image.name)
            thumb_name, thumb_ext = os.path.splitext(thumb_filename)
            thumb_name = f"{thumb_name}_thumb{thumb_ext}"
            thumb_path = os.path.join(os.path.dirname(self.image.path), 'thumbnails', thumb_name)
            if not os.path.exists(os.path.dirname(thumb_path)):
                os.makedirs(os.path.dirname(thumb_path))
            img.save(thumb_path)
            self.thumbnail = os.path.join(os.path.relpath(os.path.dirname(self.image.name), os.path.dirname(thumb_path)), thumb_name)
            print(f"Generated thumbnail path: {self.thumbnail}") 
            super().save() # Save the thumbnail path to the model
# Comment Model
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    text = models.TextField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"



   