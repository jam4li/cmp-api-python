# This script is designed to convert the old binary place values of users to a new format.
# The conversion involves changing the representation from a power-of-2-based system to a binary system.
# Additionally, the script handles updating related objects in the Referral model.

# The old calculation method involves representing binary places using a power-of-2-based system.
# Specifically, if a user's binary place is given as n,
# the calculation for determining the positions of their left and right children is as follows:
# Left Child: 2 ^ n
# Right Child: (2 ^ n) + 1

# The new calculation method involves representing binary places using a binary system based on 0 and 1.
# The conversion from the old to the new binary place involves breaking down
# the old binary place value into its binary representation.
# The steps for conversion are as follows:
# 1. Initialize an empty string for the new binary place.
# 2. While the old binary place is greater than 1:
#   . Append the remainder of the old binary place divided by 2 to the beginning of the new binary place string.
#   . Update the old binary place to the result of the floor division of the old binary place by 2.
# 3. The resulting string is the new binary place value.

# NOTE: Referral model has been merged with Network model

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
