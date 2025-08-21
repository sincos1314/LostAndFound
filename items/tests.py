from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Profile
from items.models import Item, Comment
from django.utils import timezone

class ItemsFlowTests(TestCase):
    def setUp(self):
        self.u = User.objects.create_user(username='bob', password='StrongPass123')
        Profile.objects.create(user=self.u, student_id='20230002', college='计科', class_name='2302', gender='M')
        self.client.post('/accounts/login/', {'method':'username','identifier':'bob','password':'StrongPass123'})

    def test_create_item_and_comment(self):
        r = self.client.post('/items/create/', {
            'title':'丢失校园卡',
            'description':'在图书馆附近丢失蓝色校园卡',
            'category':'lost',
            'location':'图书馆',
            'occurred_at': timezone.now().strftime('%Y-%m-%dT%H:%M'),
            'status':'open',
        })
        self.assertEqual(r.status_code, 302)
        it = Item.objects.first()
        self.assertIsNotNone(it)
        d = self.client.post(f'/items/{it.id}/', {'comment_submit':'1', 'content':'我好像看到了，私信你'})
        self.assertEqual(d.status_code, 302)
        self.assertEqual(Comment.objects.count(), 1)