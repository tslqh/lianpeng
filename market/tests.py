import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from market.models import Order, UserApp, App, AppPlan,\
        OrderLock

class MarketTest(TestCase):

    fixtures = ('app', 'plan', 'users')

    def setUp(self):
        self.app = App.objects.get(key='snapshot')
        self.plans = AppPlan.objects.all()
        self.plan1 = self.plans[0]
        self.user = User.objects.get(id=1)

    def test_order(self):
        plan = self.plan1
        app = self.app
        price = plan.price
        amount = 2
        order = Order(price=price, amount=amount, period=plan.period, user=self.user, app=app, plan=plan)
        order.save()
        self.assertTrue(order.state == 0)
        now = timezone.now()
        order.finish()
        userapp = UserApp.objects.get(user=self.user, app=app)

        self.assertTrue(userapp.plan == plan)
        self.assertTrue((userapp.expired_time - now).days == 60)
        self.assertTrue(order.state == 1)
        self.assertTrue(OrderLock.objects.get(order=order))

    def test_order_finish_twice(self):
        plan = self.plan1
        app = self.app
        price = plan.price
        amount = 2
        order = Order(price=price, amount=amount, period=plan.period, user=self.user, app=app, plan=plan)
        order.save()
        self.assertTrue(order.state == 0)
        now = timezone.now()
        order.finish()
        userapp = UserApp.objects.get(user=self.user, app=app)

        self.assertTrue(userapp.plan == plan)
        self.assertTrue((userapp.expired_time - now).days == 60)
        self.assertTrue(order.state == 1)
        self.assertTrue(OrderLock.objects.get(order=order))
        self.assertTrue(UserApp.objects.is_active(self.user, app.key))

        #: finish order again
        order.finish()
        userapp = UserApp.objects.get(user=self.user, app=app)

        self.assertTrue(userapp.plan == plan)
        self.assertTrue((userapp.expired_time - now).days == 60)
        self.assertTrue(order.state == 1)
        self.assertTrue(OrderLock.objects.get(order=order))

    def test_order_twice(self):
        plan = self.plan1
        app = self.app
        price = plan.price
        amount = 2
        order = Order(price=price, amount=amount, period=plan.period, user=self.user, app=app, plan=plan)
        order.save()
        self.assertTrue(order.state == 0)
        now = timezone.now()
        order.finish()
        userapp = UserApp.objects.get(user=self.user, app=app)

        self.assertTrue(userapp.plan == plan)
        self.assertTrue((userapp.expired_time - now).days == 60)
        self.assertTrue(order.state == 1)
        self.assertTrue(OrderLock.objects.get(order=order))


        #: order again
        order = Order(price=price, amount=amount, period=plan.period, user=self.user, app=app, plan=plan)
        order.save()
        self.assertTrue(order.state == 0)
        order.finish()

        userapp = UserApp.objects.get(user=self.user, app=app)

        self.assertTrue(userapp.plan == plan)
        self.assertTrue((userapp.expired_time - now).days == 120)
        self.assertTrue(order.state == 1)
        self.assertTrue(OrderLock.objects.get(order=order))

    def test_expired(self):
        plan = self.plan1
        app = self.app
        price = plan.price
        amount = 2
        order = Order(price=price, amount=amount, period=plan.period, user=self.user, app=app, plan=plan)
        order.save()
        self.assertTrue(order.state == 0)
        now = timezone.now()
        order.finish()
        userapp = UserApp.objects.get(user=self.user, app=app)

        self.assertTrue(userapp.plan == plan)
        self.assertTrue((userapp.expired_time - now).days == 60)
        self.assertTrue(order.state == 1)
        self.assertTrue(OrderLock.objects.get(order=order))


        userapp.expired_time = now
        userapp.save()

        self.assertFalse(UserApp.objects.is_active(self.user, app.key))


