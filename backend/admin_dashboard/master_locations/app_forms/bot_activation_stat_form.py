from .base_form import ChoicesModelForm
from ..models import BotActivationStat, ConstantsBotActivationStat


class BotActivationStatForm(ChoicesModelForm):
    class Meta:
        model = BotActivationStat
        fields = ConstantsBotActivationStat.get_fields(exclude=['views_count', 'id'])

