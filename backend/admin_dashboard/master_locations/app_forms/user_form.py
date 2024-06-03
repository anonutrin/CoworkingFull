from .base_form import ChoicesModelForm
from ..models import TelegramUsers, ConstantsTelegramUser


class TelegramUserForm(ChoicesModelForm):
    class Meta:
        model = TelegramUsers
        fields = ConstantsTelegramUser.get_fields(exclude=['created_at', 'updated_at', 'bot_activation_count'])

