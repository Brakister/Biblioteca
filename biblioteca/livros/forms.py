from django import forms
from .models import Book, Borrow, Tag
from django import forms
from .models import Emprestimo


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

class ReturnForm(forms.ModelForm):
    return_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Data de Devolução"
    )
    class Meta:
        model = Borrow
        fields = ['return_date']

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']




class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['livro', 'usuario', 'data_devolucao']
