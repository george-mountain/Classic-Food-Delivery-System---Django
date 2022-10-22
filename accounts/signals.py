from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import User, UserProfile



# @receiver(post_save,sender=User)    
# def post_save_create_profile_receiver(sender,instance,created,**kwargs):
#     print(created)
#     if created:
#         UserProfile.objects.create(user=instance)
#         # print('The user proifle has been created')
#     else:
#         try:
#             profile = UserProfile.objects.get(user=instance)
#             profile.save()
#         except:
#             #create the userprofile if it does not exist before
#             UserProfile.objects.create(user=instance)
#         #     print('Profile did not exist but new one created now')
#         # print('user is updated')

@receiver(pre_save,sender=User)
def pre_save_profile_receiver(sender,instance,**kwargs):
    pass
    # print(instance.username,'this user is being added')

# post_save.connect(post_save_create_profile_receiver,sender=User)