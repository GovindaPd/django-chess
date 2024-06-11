from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class TokenSenderTable(models.Model):
	token_id = models.CharField(max_length=10, primary_key=True, blank=False, null=False)
	token_busy = models.IntegerField(default=1)
	token_sender_id = models.CharField(max_length=30, blank=True)
	token_receiver_id = models.CharField(max_length=30, blank=True)
	#token_sender_name = models.CharField(max_length=30, blank=True)
	#token_receiver_name = models.CharField(max_length=30, blank=True)
	token_color = models.CharField(max_length=2)
	token_time = models.PositiveSmallIntegerField(default=2, validators=[MinValueValidator(1), MaxValueValidator(5)])
	token_turn = models.CharField(max_length=2, blank=False, null=False)
	token_last_joiner = models.CharField(blank=True, max_length=50)
	chessboard = models.TextField()
	castle = models.TextField()
	dead_list = models.TextField(default="[]")
	game_over = models.BooleanField(default=False)
	# token_date = 
	
	def __str__(self):
		return self.token_id


class WithComputerToken(models.Model):
	token_id = models.CharField(max_length=10, primary_key=True, blank=False, null= False)
	token_busy = models.IntegerField(default=0)
	token_color = models.CharField(max_length=2)
	token_turn = models.CharField(max_length=2, blank=False, null=False)
	token_level = models.IntegerField(default=2)	#2 or 3
	chessboard = models.TextField()
	castle = models.TextField()
	dead_list = models.TextField(default="[]")
	game_over = models.BooleanField(default=False)

	def __str__(self):
		return self.token_id