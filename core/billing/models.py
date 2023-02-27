from django.db import models
from uuid import uuid4 as uuid

# Create your models here.


class Order(models.Model):
    ORDER_STATUS_CHOICE = [
        ('Waiting', 'Waiting'),
        ('Delivered', 'Delivered'),
        ('Paid', 'Paid'),
    ]
    ordered_on = models.DateTimeField(auto_now_add=True)
    paid_online = models.BooleanField(default=False)
    order_status = models.CharField(choices=ORDER_STATUS_CHOICE,
                                    max_length=10,
                                    default=ORDER_STATUS_CHOICE[0][0])
    #  is_new returns True if the order is recently created
    #  and has no items in it
    #  but if set to False
    #  all the items are set and it is finally saved as a model.
    is_new = models.BooleanField(default=True)
    items = models.ManyToManyField('Item', through="OrderItem")

    def get_id(self):
        """
        Returns the id of the order
        """
        return self.pk

    def get_total_price(self):
        """
        Returns the total price of the order.
        This includes the sum of the toal prices of the items that 
        are ordered.
        """
        return sum([item.price for item in self.items.all()])

    def __str__(self):
        return f"OrderId: {self.pk}"


class Item(models.Model):
    name = models.CharField(max_length=120)
    price = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id}. {self.name} - Rs. {self.price}"


class OrderItem(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    item = models.ForeignKey("Item", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
