from django.contrib.auth.hashers import check_password
from django.db import models

class User(models.Model):
    ROLES = (
        ('A', 'Admin'),
        ('M', 'Moderator'),
        ('C', 'Customer')
    )
    role = models.CharField(max_length=1, choices=ROLES, default='C')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    logged_in = models.BooleanField(default=False)

    @classmethod
    def authenticate(cls, email, password):
        users = cls.objects.filter(email=email)
        if user := users.first():
            if check_password(password, user.password):
                return user

    def login(self, request):
        request.session['user'] = {'pk': self.pk, 'email': self.email, 'role': self.role}
        self.logged_in = True
        self.save()

    def logout(self,request):
        request.session['user'] = None
        self.logged_in = False
        self.save()


    def __str__(self):
        return self.email
