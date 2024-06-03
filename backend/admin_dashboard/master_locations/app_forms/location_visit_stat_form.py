from .base_form import ChoicesModelForm
from ..models import LocationVisitStats, ConstantsLocationVisitStats


class LocationVisitStatForm(ChoicesModelForm):
    class Meta:
        model = LocationVisitStats
        fields = ConstantsLocationVisitStats.get_fields(exclude=['updated_at', 'created_at'])

