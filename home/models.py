from django.db import models
from django.contrib.auth.models import User
# Create your models here.
import uuid
from django_prometheus.models import ExportModelOperationsMixin


class Policys(ExportModelOperationsMixin('policys'),models.Model):
    POLICY_TYPES = [
        ('health', 'Health Insurance'),
        ('life', 'Life Insurance'),
        ('auto', 'Auto Insurance'),
    ]


    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False)
    holder_name = models.CharField(max_length=60, null=False, blank=False)
    policy_number = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    start_date = models.DateField( null = False, blank =False)
    end_date = models.DateField( null = False, blank =False)
    premuim = models.IntegerField(null =False)
    coverage = models.IntegerField(null =False)
    policy_type = models.CharField(max_length=20, choices=POLICY_TYPES)
    def __str__(self):
        return f"Username: {self.user}, Policy_Number is: {self.policy_number}, Start_Date: {self.start_date}, End_Date: {self.end_date}, Premium: RS. {self.premuim}"
    class Meta:
        verbose_name_plural = "Policys"


class Claims(ExportModelOperationsMixin('claims'),models.Model):
    STATUS_CHOICES = [
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Initiated', 'Initiated'),
    ]
    claim_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False) 
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False)
    policy_number = models.UUIDField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='I')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    res_amt = models.IntegerField(null =False)
    amt = models.IntegerField(null =False)

    reason = models.TextField(default="----------")
    def __str__(self):
        return f"Username: {self.user}, Claim_ID: {self.claim_id}, Status: {self.status}, Claim amount: RS. {self.amt}, Residual amount: RS. {self.res_amt}"
    class Meta:
        verbose_name_plural = "Claims"
