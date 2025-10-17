from django.db import models
from django.contrib.auth.models import User


class LostItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    date_lost = models.DateField()
    photo = models.ImageField(upload_to='lost_items/', blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lost: {self.item_name} by {self.user.username}"


class FoundItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    date_found = models.DateField()
    photo = models.ImageField(upload_to='found_items/', blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Found: {self.item_name} by {self.user.username}"


class VerificationQuestion(models.Model):
    found_item = models.ForeignKey(FoundItem, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text


class ClaimAttempt(models.Model):
    found_item = models.ForeignKey(FoundItem, on_delete=models.CASCADE)
    claimant = models.ForeignKey(User, on_delete=models.CASCADE)
    answer1 = models.CharField(max_length=255, blank=True, null=True)
    answer2 = models.CharField(max_length=255, blank=True, null=True)
    answer3 = models.CharField(max_length=255, blank=True, null=True)
    correct_count = models.IntegerField(default=0)
    approved = models.BooleanField(default=False)
    date_attempted = models.DateTimeField(auto_now_add=True)

    def check_answers(self):
        """Compare claimant's answers to the correct ones."""
        correct = 0
        questions = list(self.found_item.questions.all())

        if len(questions) >= 1 and self.answer1:
            if self.answer1.lower().strip() == questions[0].answer.lower().strip():
                correct += 1
        if len(questions) >= 2 and self.answer2:
            if self.answer2.lower().strip() == questions[1].answer.lower().strip():
                correct += 1
        if len(questions) >= 3 and self.answer3:
            if self.answer3.lower().strip() == questions[2].answer.lower().strip():
                correct += 1

        self.correct_count = correct
        self.approved = correct >= 2  # at least 2/3 correct
        self.save()

    def __str__(self):
        return f"Claim by {self.claimant.username} for {self.found_item.item_name}"
