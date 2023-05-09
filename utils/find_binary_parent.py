from apps.users.models import User
from apps.referral.models import Referral

user_list = User.objects.all()

referral_not_found_counter = 0


def convert_old_to_new_binary_place(old_binary_place):
    new_binary_place = ''
    while old_binary_place > 1:
        new_binary_place = str(old_binary_place % 2) + new_binary_place
        old_binary_place //= 2
    return new_binary_place


for user in user_list:
    try:
        referral_obj = Referral.objects.get(user=user)
    except Referral.DoesNotExist:
        referral_not_found_counter += 1

        continue

    try:
        binary_place = int(referral_obj.binary_place)
        new_binary_place = convert_old_to_new_binary_place(binary_place)
        print('-------')
        print(binary_place)
        print(new_binary_place)
        print('-------')
        referral_obj.binary_place = new_binary_place
        referral_obj.save()
    except:
        continue

    if binary_place % 2 != 0:
        binary_place -= 1

    try:
        parent_binary_place = str(binary_place // 2)
    except:
        continue

    try:
        parent_referral_obj = Referral.objects.get(
            binary_place=parent_binary_place,
        )
    except Referral.DoesNotExist:
        continue

print('Referral Not Found')
print(referral_not_found_counter)
