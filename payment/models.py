from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse


class Payment(models.Model):
    order_id = models.CharField(max_length=255, unique=True)
    reference_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3)
    status = models.CharField(max_length=20)

    linked_object_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    linked_object_id = models.PositiveIntegerField(null=True, blank=True)
    linked_object = GenericForeignKey('linked_object_type', 'linked_object_id')

    # meta data
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.created_at} - {self.order_id} - {self.reference_id} - {self.amount} - {self.currency} - {self.status}"

    def get_order_id(self):
        return self.order_id

    def get_reference_id(self):
        return self.reference_id

    def get_amount(self):
        return self.amount

    def get_currency(self):
        if self.currency == "EUR":
            return "€"
        elif self.currency == "USD":
            return "$"
        else:
            return self.currency

    def get_status(self):
        return self.status

    def get_linked_object(self):
        return self.linked_object

    def get_created_at(self):
        return self.created_at

    def get_updated_at(self):
        return self.updated_at

    def get_total_amount(self):
        return self.amount + self.fee

    def get_fee(self):
        return self.fee

    def get_absolute_url(self):
        return reverse("payment:payment_details",
                       kwargs={"reference_id": self.reference_id, "object_id": self.linked_object_id,
                               "order_id": self.order_id})

    def get_payment_status_css_status(self):
        if self.status == "COMPLETED":
            return "success"
        elif self.status == "APPROVED":
            return "success"
        elif self.status == "CREATED":
            return "warning"
        elif self.status == "SAVED":
            return "warning"
        elif self.status == "PENDING":
            return "warning"
        elif self.status == "REJECTED":
            return "danger"
        elif self.status == "ERROR":
            return "danger"
        elif self.status == "EXPIRED":
            return "danger"
        elif self.status == "CANCELLED":
            return "danger"
        else:
            return "danger"
