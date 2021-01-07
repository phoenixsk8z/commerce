from django.forms import ModelForm
from .models import Watchlist

class WatchListForm(ModelForm):
    class Meta:
        model = Watchlist
        fields = ["listing", "user"]
