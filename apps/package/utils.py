from apps.users.models import User
from apps.package.models import Package
from apps.wallet.models import Wallet
from apps.config.models import Config


def validate_deposit_and_voucher_amount(username, package_id, voucher_amount):
    user = User.objects.get(username=username)
    package = Package.objects.get(id=package_id)

    # Get user's wallets
    deposit_wallet = Wallet.objects.get(
        user=user, access_type='user', type='deposit')

    if voucher_amount != 0:
        voucher_wallet = Wallet.objects.get(
            user=user, access_type='user', type='voucher')

        # Check if user has enough voucher in wallet
        if voucher_wallet.balance < voucher_amount:
            return '404'

        # Calculate the amount of voucher the user can pay in general
        max_payable_voucher_percent = Config.objects.get(
            key='package_max_payable_voucher_percent',
        )
        payable_voucher_amount = (
            max_payable_voucher_percent * package.price) / 100

        # The user can't pay more voucher than payable_voucher_amount
        if voucher_amount > payable_voucher_amount:
            return '404'

        # Check if the user has enough "USDT + Voucher" to buy a package
        if deposit_wallet.balance + voucher_amount < package.price + package.fee:
            return '472'
