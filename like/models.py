from django.db import models

from comment.models import Comment
from users.models import CustomUser

class Like(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, verbose_name='Комментарий', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
        unique_together = ('user', 'comment')

    def __str__(self):
        return f"{self.user} {self.comment}"
