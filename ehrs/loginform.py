from django import forms

class loginform(forms.Form):
    user = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
    organization = forms.CharField(max_length=100)

class newehr(forms.Form):
    ehruid = forms.CharField(max_length=999, required=False)
    subuid = forms.CharField(max_length=999)


class templateselect(forms.Form):
    CHOICES = (
        ('Vital Signs', 'Vital Signs'),
        ('Cancer Signs', 'Cancer Signs'),
    )
    template = forms.ChoiceField(widget=forms.Select, choices=CHOICES)

class vitalcomp(forms.Form):

    age = forms.CharField(max_length=999)
    sex = forms.CharField(max_length=999)
    cpt = forms.CharField(max_length=999)
    rbp = forms.CharField(max_length=999)
    chol = forms.CharField(max_length=999)
    fbsugar = forms.CharField(max_length=999)
    regc = forms.CharField(max_length=999)
    maxhr = forms.CharField(max_length=999)
    exang = forms.CharField(max_length=999)
    std = forms.CharField(max_length=999)
    slope = forms.CharField(max_length=999)
    ves = forms.CharField(max_length=999)
    thal = forms.CharField(max_length=999)

class cancercomp (forms.Form):
    clump = forms.CharField(max_length=999)
    cellsize = forms.CharField(max_length=999)
    cellshape = forms.CharField(max_length=999)
    marg = forms.CharField(max_length=999)
    epicell = forms.CharField(max_length=999)
    bare = forms.CharField(max_length=999)
    bland = forms.CharField(max_length=999)
    nucleoli = forms.CharField(max_length=999)
    mitoses = forms.CharField(max_length=999)