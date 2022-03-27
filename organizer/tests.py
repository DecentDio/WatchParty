from django.test import TestCase
from .models import Watchparty, AvailabilityRange
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

class AvailabilityRangeModelTests(TestCase):
    def test_valid_time_range(self):
        my_user = User.objects.create(username='Testuser')
        test_watchparty = Watchparty(account=my_user,title_text='test watch party', start_date='2022-02-22', end_date='2022-02-23')
        test_range = AvailabilityRange(account=my_user,watchparty=test_watchparty, start_time='2022-02-22 10:00:00', end_time='2022-02-22 12:00:00')
        self.assertIs(test_range.valid_time_range(), True)
    def test_invalid_time_range(self):
        my_user = User.objects.create(username='Testuser')
        test_watchparty = Watchparty(account=my_user,title_text='test watch party', start_date='2022-02-22', end_date='2022-02-23')
        test_range = AvailabilityRange(account=my_user,watchparty=test_watchparty, start_time='2022-02-22 10:00:00', end_time='2022-02-22 09:00:00')
        self.assertIs(test_range.valid_time_range(), False)
    def test_before_start_range(self):
        my_user = User.objects.create(username='Testuser')
        test_watchparty = Watchparty(account=my_user,title_text='test watch party', start_date='2022-02-22', end_date='2022-02-23')
        test_range = AvailabilityRange(account=my_user,watchparty=test_watchparty, start_time='2022-02-22 23:59:00', end_time='2022-02-22 09:00:00')
        self.assertIs(test_range.valid_time_range(), False)
    def test_after_end_range(self):
        my_user = User.objects.create(username='Testuser')
        test_watchparty = Watchparty(account=my_user,title_text='test watch party', start_date='2022-02-22', end_date='2022-02-23')
        test_range = AvailabilityRange(account=my_user,watchparty=test_watchparty, start_time='2022-02-22 00:00:00', end_time='2022-02-23 00:00:00')
        self.assertIs(test_range.valid_time_range(), False)



