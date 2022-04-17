from django.test import TestCase
from .models import Watchparty, AvailabilityRange
from django.contrib.auth.models import User
import datetime

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
        test_watchparty = Watchparty(account=my_user,title_text='test watch party', start_date= datetime.datetime.strptime('2022-02-22', '%Y-%m-%d'), end_date=datetime.datetime.strptime('2022-02-23', '%Y-%m-%d'))
        test_range = AvailabilityRange(account=my_user,watchparty=test_watchparty, start_time=datetime.datetime.strptime('2022-02-22 10:00', '%Y-%m-%d %H:%M'), end_time=datetime.datetime.strptime('2022-02-22 12:00', '%Y-%m-%d %H:%M'))
        self.assertIs(test_range.valid_time_range(), True)
    def test_invalid_time_range(self):
        my_user = User.objects.create(username='Testuser')
        test_watchparty = Watchparty(account=my_user,title_text='test watch party', start_date= datetime.datetime.strptime('2022-02-22', '%Y-%m-%d'), end_date=datetime.datetime.strptime('2022-02-23', '%Y-%m-%d'))
        test_range = AvailabilityRange(account=my_user,watchparty=test_watchparty, start_time=datetime.datetime.strptime('2022-02-22 10:00', '%Y-%m-%d %H:%M'), end_time=datetime.datetime.strptime('2022-02-22 09:00', '%Y-%m-%d %H:%M'))
        self.assertIs(test_range.valid_time_range(), False)
    def test_before_start_range(self):
        my_user = User.objects.create(username='Testuser')
        test_watchparty = Watchparty(account=my_user,title_text='test watch party', start_date= datetime.datetime.strptime('2022-02-22', '%Y-%m-%d'), end_date=datetime.datetime.strptime('2022-02-23', '%Y-%m-%d'))
        test_range = AvailabilityRange(account=my_user,watchparty=test_watchparty, start_time=datetime.datetime.strptime('2022-02-21 23:59', '%Y-%m-%d %H:%M') , end_time=datetime.datetime.strptime('2022-02-22 09:00', '%Y-%m-%d %H:%M'))
        self.assertIs(test_range.valid_time_range(), False)
    def test_after_end_range(self):
        my_user = User.objects.create(username='Testuser')
        test_watchparty = Watchparty(account=my_user,title_text='test watch party', start_date= datetime.datetime.strptime('2022-02-22', '%Y-%m-%d'), end_date=datetime.datetime.strptime('2022-02-23', '%Y-%m-%d'))
        test_range = AvailabilityRange(account=my_user,watchparty=test_watchparty, start_time=datetime.datetime.strptime('2022-02-22 00:00','%Y-%m-%d %H:%M'), end_time=datetime.datetime.strptime('2022-02-24 00:00','%Y-%m-%d %H:%M'))
        self.assertIs(test_range.valid_time_range(), False)



