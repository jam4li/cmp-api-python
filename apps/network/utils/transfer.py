from apps.users.models import User
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


def transfer(origin_user_email, end_point_user_email, side):
    origin_user = User.objects.get(email=origin_user_email)
    end_point_user = User.objects.get(email=end_point_user_email)

    origin_network = Network.objects.get(user=origin_user)
    end_point_network = Network.objects.get(user=end_point_user)

    origin_binary_place = origin_network.binary_place
    end_point_binary_place = end_point_network.binary_place

    print('Origin Binary Place:', end=' ')
    print(origin_binary_place)
    print('Endpoint Binary Place:', end=' ')
    print(end_point_binary_place)

    origin_network_sub = Network.objects.filter(
        binary_place__istartswith=origin_binary_place,
    )

    origin_binary_place_len = len(origin_binary_place)

    origin_binary_place_parent = origin_binary_place

    # Calculate new binary place for origin_user based on the endpoint_user
    origin_binary_place_new = end_point_binary_place
    if side == 'left':
        while True:
            origin_binary_place_new = origin_binary_place_new + '0'

            try:
                network_new = Network.objects.get(
                    binary_place=origin_binary_place_new
                )
            except Network.DoesNotExist:
                break

    elif side == 'right':
        while True:
            origin_binary_place_new = origin_binary_place_new + '1'

            try:
                network_new = Network.objects.get(
                    binary_place=origin_binary_place_new
                )
            except Network.DoesNotExist:
                break

    print('New Origin Binary Place:', end=' ')
    print(origin_binary_place_new)

    # Minus origin_network.left_amount and right_amount from the above nodes
    while True:
        if origin_binary_place_parent == '':
            break

        origin_last_character = find_last_character(
            origin_binary_place_parent,
        )

        origin_binary_place_parent = remove_last_character(
            origin_binary_place_parent,
        )

        try:
            origin_network_parent = Network.objects.get(
                binary_place=origin_binary_place_parent,
            )
        except Network.DoesNotExist:
            continue

        if origin_last_character == '0':
            origin_network_parent.left_count -= origin_network.left_count
            origin_network_parent.left_amount -= origin_network.left_amount

        elif origin_last_character == '1':
            origin_network_parent.right_count -= origin_network.right_count
            origin_network_parent.right_amount -= origin_network.right_amount

        print('Origin network parent:', end=' ')
        print(origin_network_parent.binary_place)
        origin_network_parent.save()

    # Update binary place for the origin sub users
    for network in origin_network_sub:
        binary_place_remain = network.binary_place[origin_binary_place_len:]
        binary_place_new = origin_binary_place_new + binary_place_remain

        network.binary_place = binary_place_new

        print('New binary place for sub user:', end=' ')
        print(network.binary_place)
        network.save()

        # Plus origin_network.left_amount and right_amount to the new above nodes
    while True:
        if origin_binary_place_new == '':
            break

        origin_last_character_new = find_last_character(
            origin_binary_place_new,
        )

        origin_binary_place_new = remove_last_character(
            origin_binary_place_new,
        )

        try:
            origin_network_parent_new = Network.objects.get(
                binary_place=origin_binary_place_new,
            )
        except Network.DoesNotExist:
            continue

        if origin_last_character_new == '0':
            origin_network_parent_new.left_count += origin_network.left_count
            origin_network_parent_new.left_amount += origin_network.left_amount

        elif origin_last_character_new == '1':
            origin_network_parent_new.right_count += origin_network.right_count
            origin_network_parent_new.right_amount += origin_network.right_amount

        print('Origin network parent new:', end=' ')
        print(origin_network_parent_new.binary_place)
        origin_network_parent_new.save()
