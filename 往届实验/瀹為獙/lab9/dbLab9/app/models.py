from django.db import models

# Create your models here.


class User(models.Model):
    uid = models.AutoField(primary_key=True)
    uname = models.CharField(max_length=50)
    age = models.IntegerField(default=0, blank=True, null=True)
    phone = models.CharField(max_length=11)
    city = models.CharField(max_length=50)

    class Meta:
        app_label = 'app'

    def to_dic(self):
        return {
            'uid': self.uid,
            'uname': self.uname,
            'age': self.age,
            'phone': self.phone,
            'city': self.city
        }


class Role(models.Model):
    rid = models.AutoField(primary_key=True)
    rname = models.CharField(max_length=50)

    class Meta:
        app_label = 'app'


class Perm(models.Model):
    pid = models.AutoField(primary_key=True)
    pname = models.CharField(max_length=50)

    class Meta:
        app_label = 'app'


class Ur(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey('app.User', on_delete=models.CASCADE)
    rid = models.ForeignKey('app.Role', on_delete=models.CASCADE)

    class Meta:
        app_label = 'app'


class Pr(models.Model):
    id = models.AutoField(primary_key=True)
    rid = models.ForeignKey('app.Role', on_delete=models.CASCADE)
    pid = models.ForeignKey('app.Perm', on_delete=models.CASCADE)

    class Meta:
        app_label = 'app'
