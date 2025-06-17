from aiogram.filters.callback_data import CallbackData


class SetAdminCallback(CallbackData, prefix="set_admin"):
    pass


class RemoveAdminCallback(CallbackData, prefix="remove_admin"):
    pass


class CreateSubscriptionCallback(CallbackData, prefix="create_subscription_plan"):
    pass


class SubscriptionStatsCallback(CallbackData, prefix="subscription_stats"):
    pass


class ActivateUserCallback(CallbackData, prefix="activate_user"):
    pass


class DeactivateUserCallback(CallbackData, prefix="deactivate_user"):
    pass


class CheckUserTestCallback(CallbackData, prefix="check_user_test"):
    pass


class DeactivateSubscriptionCallback(CallbackData, prefix="deactivate_subscription"):
    pass


class GiveSubscriptionCallback(CallbackData, prefix="give_subscription"):
    pass


class SetPremiumSubscriptionCallback(CallbackData, prefix="set_premium_subscription"):
    pass


class RemovePremiumSubscriptionCallback(
    CallbackData, prefix="remove_premium_subscription"
):
    pass

class CreatePraxiCallback(CallbackData, prefix="create_praxi"):
    pass

class UploadSubscriptionFiles(CallbackData, prefix="upload_files"):
    pass

class DeleteSubscriptionFiles(CallbackData, prefix="delete_files"):
    pass

class AllSubscriptionFiles(CallbackData, prefix="all_files"):
    pass