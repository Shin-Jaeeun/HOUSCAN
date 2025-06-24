from django.db import models
from django.conf import settings

class CommunityPost(models.Model):
    CATEGORY_CHOICES = [
        ('아파트', '아파트'),
        ('임의공급', '임의공급'),
        ('주택', '주택'),
        ('토지', '토지'),
        ('상가', '상가'),
        ('예적금', '예적금'),
        ('자유게시판', '자유게시판'),
    ]

    title = models.CharField(max_length=100)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES,default='자유게시판')  # ✅ 추가
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'user')  # 한 게시글에 한 번만 좋아요 가능
