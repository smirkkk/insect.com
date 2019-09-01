from django import forms
from .models import Champion


class ChampionForm(forms.ModelForm):
    grade1 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 4점 이상', 'maxlength': 200, 'style': 'width:750px;'}))
    grade2 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 3점대', 'maxlength': 200, 'style': 'width:750px;'}))
    grade3 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 2점대', 'maxlength': 200, 'style': 'width:750px;'}))
    grade4 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 1점대', 'maxlength': 200, 'style': 'width:750px;'}))
    grade5 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 1점 미만', 'maxlength': 200, 'style': 'width:750px;'}))

    grade6 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 4점 이상', 'maxlength': 200, 'style': 'width:750px;'}))
    grade7 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 3점대', 'maxlength': 200, 'style': 'width:750px;'}))
    grade8 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 2점대', 'maxlength': 200, 'style': 'width:750px;'}))
    grade9 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 1점대', 'maxlength': 200, 'style': 'width:750px;'}))
    grade10 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 1점 미만', 'maxlength': 200, 'style': 'width:750px;'}))

    grade11 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 4점 이상', 'maxlength': 200, 'style': 'width:750px;'}))
    grade12 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 3점대', 'maxlength': 200, 'style': 'width:750px;'}))
    grade13 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 2점대', 'maxlength': 200, 'style': 'width:750px;'}))
    grade14 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 1점대', 'maxlength': 200, 'style': 'width:750px;'}))
    grade15 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 1점 미만', 'maxlength': 200, 'style': 'width:750px;'}))

    grade16 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 4점 이상', 'maxlength': 200, 'style': 'width:750px;'}))
    grade17 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 3점대', 'maxlength': 200, 'style': 'width:750px;'}))
    grade18 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 2점대', 'maxlength': 200, 'style': 'width:750px;'}))
    grade19 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 1점대', 'maxlength': 200, 'style': 'width:750px;'}))
    grade20 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 1점 미만', 'maxlength': 200, 'style': 'width:750px;'}))

    class Meta:
        model = Champion
        fields = '__all__'
