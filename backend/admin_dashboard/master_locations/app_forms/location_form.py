from .base_form import ChoicesModelForm
from ..models import Location, ConstantsLocation


class LocationForm(ChoicesModelForm):
    class Meta:
        model = Location
        fields = ConstantsLocation.get_fields(exclude=['id'])

