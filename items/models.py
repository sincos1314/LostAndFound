from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = (
    ('lost', '寻物'),
    ('found', '招领'),
)

STATUS_CHOICES = (
    ('open', '未解决'),
    ('resolved', '已归还/已找到'),
)

def item_image_path(instance, filename):
    return f'item_images/{instance.owner_id}/{filename}'

class Item(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('标题', max_length=100)
    description = models.TextField('描述')
    category = models.CharField('类型', max_length=10, choices=CATEGORY_CHOICES, default='lost')
    location = models.CharField('地点', max_length=120)
    occurred_at = models.DateTimeField('发生时间')
    image = models.ImageField('图片', upload_to=item_image_path, null=True, blank=True)
    status = models.CharField('状态', max_length=10, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.get_category_display()} - {self.title}'

class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField('留言内容', max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.item_id}'