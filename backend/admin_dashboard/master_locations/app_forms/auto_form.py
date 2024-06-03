
from .base_form import ChoicesModelForm
from ..models import Auto, ConstantsAuto


class AutoForm(ChoicesModelForm):
    class Meta:
        model = Auto
        fields = ConstantsAuto.get_fields(exclude=['id'])
