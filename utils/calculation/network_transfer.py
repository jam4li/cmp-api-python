from decimal import Decimal
from apps.network.models import Network


def remove_last_character(string):
    if len(string) > 0:
        modified_string = string[:-1]
        return modified_string
    else:
        return string


def find_last_character(string):
    if len(string) > 0:
        last_character = string[-1]
        return last_character
    else:
        return None


def transfer(old_binary_place, new_binary_place, amount):
    amount = Decimal(amount)

    while True:
        if old_binary_place == '':
            break

        old_last_character = find_last_character(
            old_binary_place,
        )

        old_binary_place = remove_last_character(
            old_binary_place,
        )

        try:
            old_parent_network = Network.objects.get(
                binary_place=old_binary_place,
            )
        except Network.DoesNotExist:
            continue

        print('Old network parent:', end=' ')
        print(old_parent_network.binary_place)

        if old_last_character == '0':
            old_parent_network.left_count -= 1
            old_parent_network.left_amount -= amount
            print(old_parent_network.left_amount)

        elif old_last_character == '1':
            old_parent_network.right_count -= 1
            old_parent_network.right_amount -= amount
            print(old_parent_network.right_amount)

        print('******************************')

        old_parent_network.save()

    while True:
        if new_binary_place == '':
            break

        new_last_character = find_last_character(
            new_binary_place,
        )

        new_binary_place = remove_last_character(
            new_binary_place,
        )

        try:
            new_parent_network = Network.objects.get(
                binary_place=new_binary_place,
            )
        except Network.DoesNotExist:
            continue

        print('New network parent:', end=' ')
        print(new_parent_network.binary_place)

        if new_last_character == '0':
            new_parent_network.left_count += 1
            new_parent_network.left_amount += amount
            print(new_parent_network.left_amount)

        elif new_last_character == '1':
            new_parent_network.right_count += 1
            new_parent_network.right_amount += amount
            print(new_parent_network.right_amount)

        print('******************************')

        new_parent_network.save()
