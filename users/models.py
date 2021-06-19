from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F, Q

User = get_user_model()


class Follow(models.Model):
    author = models.ForeignKey(User,
                               verbose_name='Автор',
                               related_name='followings',
                               on_delete=models.CASCADE)
    follower = models.ForeignKey(User,
                                 verbose_name='Подписчик',
                                 on_delete=models.CASCADE,
                                 related_name='followers')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'follower'],
                                    name='unique_follow'),
            models.CheckConstraint(check=~Q(follower=F('author')),
                                   name='dont_follow_yourself')
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['author']
