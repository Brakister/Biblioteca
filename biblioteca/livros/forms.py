from django import forms
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from .models import Book, Borrow, Tag

class BookForm(forms.ModelForm):
    # Campo para entrada de tags separadas por vírgula
    tags = forms.CharField(required=False, help_text="Informe as tags separadas por vírgula.")

    class Meta:
        model = Book
        fields = ['title', 'author', 'available', 'tags']

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['tags'].initial = ", ".join([tag.name for tag in self.instance.tags.all()])

    def clean_tags(self):
        tags_str = self.cleaned_data.get('tags', '')
        tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]
        if not all(tag.isalnum() or ' ' in tag for tag in tag_names):
            raise forms.ValidationError("As tags só podem conter letras, números ou espaços.")
        return tags_str

    def save(self, commit=True):
        instance = super(BookForm, self).save(commit=False)
        if commit:
            instance.save()
        tags_str = self.cleaned_data.get('tags', '')
        tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]
        instance.tags.clear()
        for name in tag_names:
            tag, created = Tag.objects.get_or_create(name=name)
            instance.tags.add(tag)
        return instance


class BorrowForm(forms.ModelForm):
    expiration_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Data de Expiração"
    )

    class Meta:
        model = Borrow
        fields = ['expiration_date']

    def clean_expiration_date(self):
        expiration_date = self.cleaned_data.get('expiration_date')
        if expiration_date and expiration_date <= now():
            raise ValidationError("A data de expiração deve ser posterior à data atual.")
        return expiration_date


class ReturnForm(forms.ModelForm):
    return_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Data de Devolução"
    )

    class Meta:
        model = Borrow
        fields = ['return_date']

    def clean_return_date(self):
        return_date = self.cleaned_data.get('return_date')
        borrowed_date = self.instance.borrowed_date
        if return_date and return_date <= borrowed_date:
            raise ValidationError("A data de devolução deve ser posterior à data de empréstimo.")
        return return_date


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']