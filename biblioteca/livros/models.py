from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True, null=True)
    available = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title

class Borrow(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrows')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrows')
    borrowed_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField()
    return_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.book.title} emprestado por {self.user.username}"


class Livro(models.Model):
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo

class Emprestimo(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_emprestimo = models.DateField(auto_now_add=True)
    data_devolucao = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.livro.titulo} - {self.usuario.username}"