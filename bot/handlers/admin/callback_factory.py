from aiogram.filters.callback_data import CallbackData


class SetAdminCallback(CallbackData, prefix='set_admin'):
    pass

class RemoveAdminCallback(CallbackData, prefix='remove_admin'):
    pass

class CreateSubscriptionPlanCallback(CallbackData, prefix='create_subscription_plan'):
    pass

class DeleteSubscriptionPlanCallback(CallbackData, prefix='delete_subscription_plan'):
    pass

class StatsSubscriptionCallback(CallbackData, prefix='stats_subscription'):
    pass

class ActivateUserCallback(CallbackData, prefix='activate_user'):
    pass

class DeactivateUserCallback(CallbackData, prefix='deactivate_user'):
    pass