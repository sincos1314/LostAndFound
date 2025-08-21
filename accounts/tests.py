from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Profile

class AccountsFlowTests(TestCase):
    def setUp(self):
        self.u = User.objects.create_user(username='alice', password='StrongPass123', email='alice@example.com')
        Profile.objects.create(user=self.u, student_id='20230001', college='计科', class_name='2301', gender='F', phone='13800000000')

    def test_login_username(self):
        ok = self.client.post('/accounts/login/', {'method':'username','identifier':'alice','password':'StrongPass123'})
        self.assertEqual(ok.status_code, 302)

    def test_login_student_id(self):
        ok = self.client.post('/accounts/login/', {'method':'student_id','identifier':'20230001','password':'StrongPass123'})
        self.assertEqual(ok.status_code, 302)

    def test_login_email(self):
        ok = self.client.post('/accounts/login/', {'method':'email','identifier':'alice@example.com','password':'StrongPass123'})
        self.assertEqual(ok.status_code, 302)

    def test_login_phone(self):
        ok = self.client.post('/accounts/login/', {'method':'phone','identifier':'13800000000','password':'StrongPass123'})
        self.assertEqual(ok.status_code, 302)