from django.db import models


class Tweet(models.Model):
    text = models.TextField()
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    photo = models.URLField(max_length=200, blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'[{self.author.username}] {self.text}'


class Follow(models.Model):
    # User(username=Саша, follows=[Саша->Миша], followers=[])
    follower = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='follows')
    # User(username=Миша, follows=[], followers=[Саша->Миша])
    follows = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='followers')
    followed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower.username} -> {self.follows.username}'
