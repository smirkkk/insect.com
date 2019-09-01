from django import forms
from .models import Champion


class ChampionForm(forms.ModelForm):
    grade1 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 4점 이상', 'maxlength': 200, 'style': 'width:750px;'}), required=False)
    grade2 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 3점대', 'maxlength': 200, 'style': 'width:750px;'}), required=False)
    grade3 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 2점대', 'maxlength': 200, 'style': 'width:750px;'}), required=False)
    grade4 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 1점대', 'maxlength': 200, 'style': 'width:750px;'}), required=False)
    grade5 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 1점 미만', 'maxlength': 200, 'style': 'width:750px;'}), required=False)

    grade6 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 4점 이상', 'maxlength': 200, 'style': 'width:750px;'}), required=False)
    grade7 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 3점대', 'maxlength': 200, 'style': 'width:750px;'}), required=False)
    grade8 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 2점대', 'maxlength': 200, 'style': 'width:750px;'}), required=False)
    grade9 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 1점대', 'maxlength': 200, 'style': 'width:750px;'}), required=False)
    grade10 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 1점 미만', 'maxlength': 200, 'style': 'width:750px;'}), required=False)

    grade11 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 4점 이상', 'maxlength': 200, 'style': 'width:750px;'}), required=False)
    grade12 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 3점대', 'maxlength': 200, 'style': 'width:750px;'}), required=False)
    grade13 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 2점대', 'maxlength': 200, 'style': 'width:750px;'}), required=False)
    grade14 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 1점대', 'maxlength': 200, 'style': 'width:750px;'}), required=False)
    grade15 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 1점 미만', 'maxlength': 200, 'style': 'width:750px;'}), required=False)

    grade16 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 4점 이상', 'maxlength': 200, 'style': 'width:750px;'}), required=False)
    grade17 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 3점대', 'maxlength': 200, 'style': 'width:750px;'}), required=False)
    grade18 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 2점대', 'maxlength': 200, 'style': 'width:750px;'}), required=False)
    grade19 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 1점대', 'maxlength': 200, 'style': 'width:750px;'}), required=False)
    grade20 = forms.CharField(widget=forms.TextInput({'placeholder':'평점 1점 미만', 'maxlength': 200, 'style': 'width:750px;'}), required=False)

    class Meta:
        model = Champion
        fields = '__all__'
