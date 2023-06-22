from django.db import models
import uuid

userrole={
    ('admin','admin'),
    ('user','user'),
}

loanstatus={
    ('approved','approved'),
    ('pending','pending'),
    ('reject','reject'),

}

class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    updated_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    class Meta:
        abstract = True

# Create your models here.
class Account(BaseModel):
    firstname = models.CharField(max_length=255, default='')
    lastname = models.CharField(max_length=255, default='')
    email = models.EmailField(max_length=255, default='')
    password = models.CharField(max_length=255, default='')
    contact = models.CharField(max_length=255, default='')
    role=models.CharField(choices=userrole,max_length=20,default="user")


    def __str__(self):
        return self.email

class loan(models.Model):
    amount = models.IntegerField()
    date = models.DateTimeField()
    comment = models.TextField()
    loanstatus=models.CharField(choices=loanstatus,max_length=20,default="pending")
    userdetails = models.ForeignKey(Account, blank = True, null = True, on_delete = models.CASCADE)

    # Add any other fields yosu require for the loan model
