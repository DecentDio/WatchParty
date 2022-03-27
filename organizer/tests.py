from django.test import TestCase
from .models import Watchparty
from django.contrib.auth.models import User

class WatchpartyModelTests(TestCase):
    def test_valid_date_range(self):
        my_user = User.objects.create(username='Testuser')
        test_watchparty = Watchparty(account=my_user,title_text='test watch party', start_date='2022-02-22', end_date='2022-02-23')
        self.assertIs(test_watchparty.valid_date_range(), True)

    def test_invalid_date_range(self):
        my_user = User.objects.create(username='Testuser')
        test_watchparty = Watchparty(account=my_user,title_text='test watch party', start_date='2022-02-23', end_date='2022-02-22')
        self.assertIs(test_watchparty.valid_date_range(), False)

    def test_same_day(self):
        my_user = User.objects.create(username='Testuser')
        test_watchparty = Watchparty(account=my_user,title_text='test watch party', start_date='2022-02-22', end_date='2022-02-22')
        self.assertIs(test_watchparty.valid_date_range(), True)


