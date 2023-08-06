from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin




# class UserManger(BaseUserManager):
#     use_in_migrations = True

#     def create_user(self, userID, password):

#         user = self.model(
#             userID = userID
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
    
#     def create_superuser(self, userID, password):
#         superuser = self.create_user(userID = userID, password = password)
#         superuser.is_staff = True
#         superuser.is_superuser = True
#         superuser.is_active = True
#         superuser.save(using=self._db)
        
#         return superuser


# class Region(models.Model):
#     name= models.CharField(verbose_name='지역',max_length=50)
#     def __str__(self):
#         return self.name

class UserManger(BaseUserManager):
    use_in_migrations = True

    def create_user(self, userID, user_type, user_name, user_phonenum, user_address, user_gender, password):
        user = self.model(
            userID = userID,
            user_type = user_type,
            user_name = user_name,
            user_phonenum = user_phonenum,
            user_address = user_address,
            user_gender = user_gender,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, userID, user_type, user_name, user_phonenum, user_address, user_gender, password):
        superuser = self.create_user(userID1 = userID, user_type1 = user_type,
            user_name1 = user_name,
            user_phonenum1 = user_phonenum,
            user_address1 = user_address,
            user_gender1 = user_gender,
            password1 = password)
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        superuser.save(using=self._db)
        
        return superuser
    

    
class User(AbstractBaseUser, PermissionsMixin):
    userID = models.CharField(max_length=50, unique = True,null=True)# 이메일(아이디)
    user_type=models.IntegerField(verbose_name='회원종류',default=0)# 기업회원의 타입 (의류,음식,예술)
    user_name = models.CharField(verbose_name='이름',max_length=50, null=True,default=0)
    user_phonenum = models.CharField(verbose_name='전화번호',max_length=50, null=True,default=0)
    
    user_address = models.CharField(verbose_name='주소',max_length=50, null=True,default=0)# 주소(시)
    #user_address = models.ForeignKey(Region, on_delete=models.CASCADE, null=True)

    user_gender = models.IntegerField(verbose_name='성별', null=True,default=0)


    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    def is_staff(self):
        return self.is_admin
    
    objects = UserManger()

    USERNAME_FIELD = 'userID'

    class Meta:
        db_table = 'user'