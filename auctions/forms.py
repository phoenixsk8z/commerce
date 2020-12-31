from django import forms

class WatchlistForm(forms.Form):
    def __init__(self, *args, **kwargs):
        print(kwargs.keys())

        listing_id = kwargs.pop('listing_id')
        super().__init__(*args, **kwargs)

        self.fields["listing_id"] = forms.IntegerField(
            required = False,
            widget = forms.HiddenInput()
        )