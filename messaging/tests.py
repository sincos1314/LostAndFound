from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Profile
from items.models import Item
from django.utils import timezone

class MessagingFlowTests(TestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(username='u1', password='StrongPass123')
        Profile.objects.create(user=self.u1, student_id='20230003', college='计科', class_name='2303', gender='M')
        self.u2 = User.objects.create_user(username='u2', password='StrongPass123')
        Profile.objects.create(user=self.u2, student_id='20230004', college='计科', class_name='2304', gender='F')

        self.item = Item.objects.create(
            owner=self.u2, title='拾到校园卡', description='在食堂捡到校园卡',
            category='found', location='一食堂', occurred_at=timezone.now()
        )

    def test_private_message(self):
        self.client.post('/accounts/login/', {'method':'username','identifier':'u1','password':'StrongPass123'})
        r = self.client.get(f'/msg/start/{self.item.id}/')
        self.assertEqual(r.status_code, 302)
        # room
        room_url = r['Location']
        send = self.client.post(room_url, {'content':'你好，我是失主'}, follow=True)
        self.assertEqual(send.status_code, 200)
        self.assertContains(send, '你好，我是失主')