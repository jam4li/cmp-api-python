from apps.users.models import User
from apps.referral.models import Referral

user_list = User.objects.all()

referral_not_found = 0
parent_not_found = 0

binary_place_not_integer = 0
parent_binary_not_integer = 0

for user in user_list:
    try:
        referral_obj = Referral.objects.get(user=user)
    except Referral.DoesNotExist:
        referral_not_found += 1

        print("Referral Not Found:", end=' ')
        print(referral_not_found)

        print("Parent Referral Not Found:", end=' ')
        print(parent_not_found)

        continue

    try:
        binary_place = int(referral_obj.binary_place)
    except:
        print('Binary Place is not integer')
        print(binary_place)
        binary_place_not_integer += 1
        continue

    if binary_place % 2 != 0:
        binary_place -= 1

    try:
        parent_binary_place = str(binary_place // 2)
    except:
        print('Parent binary place is not integer')
        print(parent_binary_place)
        parent_binary_not_integer += 1
        continue

    try:
        parent_referral_obj = Referral.objects.get(
            binary_place=parent_binary_place,
        )
    except Referral.DoesNotExist:
        parent_not_found += 1

        print(referral_obj.user.email)

        print("Referral Not Found:", end=' ')
        print(referral_not_found)

        print("Parent Referral Not Found:", end=' ')
        print(parent_not_found)

        continue

    print("Referral Not Found:", end=' ')
    print(referral_not_found)

    print("Parent Referral Not Found:", end=' ')
    print(parent_not_found)

print(binary_place_not_integer)
print(parent_binary_not_integer)
