# import aioredis
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer, WebsocketConsumer
from asgiref.sync import sync_to_async	#for group chat or async_to_sync
from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import TokenSenderTable, WithComputerToken
from .chess import Chess
import json
from copy import deepcopy


class OnlineWithFriendConsumer(AsyncJsonWebsocketConsumer):

	async def connect(self):
		#accept connection
		await self.accept()

		self.room_name = self.scope['url_route']['kwargs']['teamname']
		# print(self.scope, self.scope['url_route'], self.channel_name, self.room_name)
		
		try:
			userdata =  await database_sync_to_async(get_object_or_404)(TokenSenderTable, token_id=self.room_name)

			self.username = userdata.token_last_joiner
			self.players = userdata.token_busy
			self.time = userdata.token_time
			#retunr whois color
			self.color = userdata.token_color if userdata.token_last_joiner == 'sender' else 'W' if userdata.token_color == 'B' else 'B'
			self.turn = userdata.token_turn
			self.chessboard = json.loads(userdata.chessboard)
			self.castle = json.loads(userdata.castle)
			self.dead_list = json.loads(userdata.dead_list)

			#create new group if not exist else add in present group
			await self.channel_layer.group_add(
				self.room_name,
				self.channel_name,
			)

			await self.channel_layer.group_send(
				self.room_name,
				{
					'type':'game_join',
					'username':self.username,
					'players':self.players,
					'message':"Joind Group",
					'time': self.time
				})
		except Http404:
			self.close()
			pass

	async def disconnect(self, close_code):
		try:
			tb_read =  await database_sync_to_async(get_object_or_404)(TokenSenderTable, token_id=self.room_name)
			
			avail_users = tb_read.token_busy - 1	#decreas join users after leave
			await sync_to_async(on_leave, thread_sensitive=True)(self.username, tb_read)

			if avail_users !=0 :
				await self.channel_layer.group_send(
					self.room_name,
					{
						'type': 'game_leave',
						'username': self.username,
						'message': self.username + " leave"
					})	
			else:	
				await self.channel_layer.group_discard(
					self.room_name,
					self.channel_name
				)
		except Http404:
			pass
		finally:
			self.close()

	async def receive_json(self, content):
		typ = content.get("type")
		if typ == "message":
			await self.channel_layer.group_send(
				self.room_name,
				{
					"type": "chat_message",
					"username": self.username,
					"message": content["message"]
				})

		elif typ == "time_over":
			await self.channel_layer.group_send(
				self.room_name,
				{
					"type":"time_over",
					"username": self.username,
					"turn": self.color
				})
			
		elif typ == "store":
			try:
				tb_read = await database_sync_to_async(get_object_or_404)(TokenSenderTable, token_id=self.room_name)
				await sync_to_async(store_data, thread_sensitive=True)(content, tb_read)
			except Http404:
				pass

		#get legal moves
		elif typ == "get_moves":
			self.chessboard = content['chessboard']
			self.castle = content['castle']
			self.dead_list = content['dead_list']

			legal_moves = Chess.get_both_data(self.color, self.chessboard, self.castle)[0]
			if legal_moves!=None:
				legal_moves = legal_moves['legal_moves']
			else:
				legal_moves = {}

			await self.channel_layer.group_send(
				self.room_name,
				{
					'type':'get_moves',
					'username': self.username,
					'legal_moves': legal_moves
				})


		# make moves on board
		elif typ == 'make_moves':
			if self.color == content.get('color'):
				context = {}

				if self.chessboard[content['to_']] != '':
					context['dead_man'] = self.chessboard[content['to_']]
					self.dead_list.append(self.chessboard[content['to_']])

				Chess.push(self.turn, self.chessboard, self.castle, content['from_'], content['to_'], self.chessboard[content['from_']])
				temp = Chess.get_both_data(self.color, self.chessboard, self.castle)

				# context['legal_moves'] = temp[1]['legal_moves']
				context['chessboard'] = self.chessboard
				context['castle'] = self.castle
				context['dead_list'] = self.dead_list
				context['htt'] = [content['from_'], content['to_']]
				context['whois'] = self.username
				context['turn'] = 'B' if self.color == 'W' else 'W'
				context['sec'] = self.time

				#check opponent king got check
				if temp[1]['kp'] in temp[0]['all_moves']:
					context['check'] = True
					context['kp'] = temp[1]['kp']

				if len(temp[1]['legal_moves'])==0:
					if Chess.checkmate(temp[1]['kp'], temp[1]['legal_moves'], temp[0]['all_moves']):
						context['win'] = True

					elif Chess.stalemate(temp[1]['kp'],temp[1]['legal_moves'],temp[0]['all_moves']):
						context['stalemate_win'] = True

				if Chess.insufficient_piece(self.chessboard):
					context['insufficient_piece'] = True

				await self.channel_layer.group_send(
					self.room_name,
					{
						"type": "make_moves",
						"username": self.username,
						"context": context,
					})
		else:
			pass
			#context['move_data'] = json.dumps(Chess.get_both_data(turn, chessboard, castle))
			#possible_moves = self.move_data[0]['legal_moves'].get(moving_man,[])
	
	async def make_moves(self,event):
		await self.send_json(event)

	async def get_moves(self, event):
		await self.send_json(event)

	async def chat_message(self, event):
		await self.send_json(event)
	
	async def time_over(self,event):
		await self.send_json(event)
	
	async def game_join(self, event):
		await self.send_json(event)

	async def game_leave(self, event):
		await self.send_json(event)

# store user data
def store_data(content, tb_read):
	tb_read.token_turn = content.get('turn')
	#tb_read.token_time = content.get('time')
	tb_read.chessboard = json.dumps(content.get('chessboard'))
	tb_read.castle = json.dumps(content.get('castle'))
	tb_read.dead_list = json.dumps(content.get('dead_list'))
	
	if content.get('gameover') == True:
		tb_read.game_over = content.get('gameover')
	tb_read.save()

#handle user leave in database
def on_leave(username, tb_read):
	if tb_read.token_busy == 2:
		tb_read.token_busy = 1
		if username == tb_read.token_sender_id:
			tb_read.token_sender_id = ''
		elif username == tb_read.token_receiver_id:
			tb_read.token_receiver_id = ''
		tb_read.save()
	else:
		tb_read.delete()



class WithComputerConsumer(AsyncJsonWebsocketConsumer):
	async def connect(self):
		await self.accept()
		self.room_name = self.scope['url_route']['kwargs']['token_id']

		try:
			userdata = await database_sync_to_async(get_object_or_404)(WithComputerToken, token_id=self.room_name)
			self.players = userdata.token_busy
			self.color = userdata.token_color
			self.turn = userdata.token_turn
			self.depth = userdata.token_level
			self.chessboard = json.loads(userdata.chessboard)
			self.castle = json.loads(userdata.castle)
			self.dead_list = json.loads(userdata.dead_list)

			await self.send_json({
				'type':'game_join',
				'message':"Joind Group",
			})
		except Http404:
			await self.close()
			
		
	async def disconnect(self, close_code):
		try:
			tb_read = await database_sync_to_async(get_object_or_404)(WithComputerToken, token_id = self.room_name)
			await sync_to_async(delete_record)(tb_read)
		except Http404:
			pass
		finally:
			# print("disconnect...")
			self.close()

	async def receive_json(self, content):
		typ = content.get("type")
		#get legal moves
		if typ == "get_moves":
			legal_moves = Chess.get_both_data(self.color, self.chessboard, self.castle)[0]
			legal_moves = legal_moves['legal_moves'] if legal_moves!=None else {}

			await self.send_json({
				'type':'get_moves',
				'legal_moves': legal_moves
			})

		# make moves on board
		elif typ == 'make_moves':
			# for computer
			if self.color != self.turn:
				data,points = Chess.play(self.chessboard.copy(), deepcopy(self.castle), self.turn, self.depth)
				chessman_name, from_, to_ = data if data != None else (None, None, None)

        	# for user
			elif self.color == self.turn:
				from_ = content.get('from_')
				to_ = content.get('to_')
				chessman_name = self.chessboard.get(from_)
			
			if from_ != None and to_ != None and chessman_name != None:
				context = {}
				if self.chessboard[to_] != '':
					context['dead_man'] = self.chessboard[to_]
					self.dead_list.append(self.chessboard[to_])

				Chess.push(self.turn, self.chessboard, self.castle, from_, to_, chessman_name)
				temp = Chess.get_both_data(self.turn, self.chessboard, self.castle)

				#check opponent king got check
				if temp[1]['kp'] in temp[0]['all_moves']:
					context['check'] = True
					context['kp'] = temp[1]['kp']

				# opponent does not have legal moves
				if len(temp[1]['legal_moves'])==0:
					if Chess.checkmate(temp[1]['kp'], temp[1]['legal_moves'], temp[0]['all_moves']):
						context['win'] = True

					elif Chess.stalemate(temp[1]['kp'],temp[1]['legal_moves'],temp[0]['all_moves']):
						context['stalemate_win'] = True

				if Chess.insufficient_piece(self.chessboard):
					context['insufficient_piece'] = True

				context['chessboard'] = self.chessboard
				context['castle'] = self.castle
				context['dead_list'] = self.dead_list
				context['htt'] = [from_, to_]
				context['color'] = self.color

				context['turn'] = self.turn = 'B' if self.turn == 'W' else 'W'
				context['legal_moves'] = temp[1]['legal_moves'] if self.color == self.turn else {}

				await self.send_json({
					"type": "make_moves",
					"context": context,
				})


	async def make_moves(self,event):
		await self.send_json(event)

	async def get_moves(self, event):
		await self.send_json(event)

	async def game_join(self, event):
		await self.send_json(event)

def delete_record(tb):
	tb.delete()

"""
#practice
class withcomputer(WebsocketConsumer):
	def connect(self):
		self.accept()
		self.send(text_data=json.dumps({
			'type':'websocket.accept',
			'message':'You are now connected'
			}))
	
	def receive(self, text_data):
		text_data_json = json.loads(text_data)
		box_id = text_data_json['box_id']
		color = text_data_json['color']
		move(box_id,color)
		print('message: ',text_data_json)

		self.send(text_data = json.dumps({
			'type':'chat',
			'message':box_id,
			'color':color
		}))
	# def disconnect(self,close_code):
	# 	self.close()

class WithComputer(AsyncJsonWebsocketConsumer):
	async def connect(self):
		self.room_name = self.scope['url_route']['kwargs']['teamname']
		self.room_group_name = self.room_name
		
		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name)
		await self.accept()

		self.chessobj = ChessmanMove(self.userdata.token_chessboard, int(self.userdata.token_time))
		self.chessobj.handle()

		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type':'chat_join',
				'message':'joind group'
			}
		)

	async def disconnect(self, close_code):
		print("disconnect....")
		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type':'chat_leave',
				# 'username':self.username,
				'message':"user leave"
			}
		)
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)

	async def receive_json(self, content):
		print("data received.....")

		await self.channel_layer.group_send(
			self.room_group_name,
			{
				"type": "chat_message",
				# "username": self.username,
				"message": content["message"],
			}
		)

	async def chat_message(self, event):
		await self.send_json(event)
	async def chat_join(self, event):
		await self.send_json(event)
	async def chat_leave(self, event):
		await self.send_json(event)
"""

# class onlinechesswithfriendsConsumer(WebsocketConsumer):
# 	def connect(self):
# 		# print('you current url is : ',self.scope['url_route'])
# 		self.room_name = self.scope['url_route']['kwargs']['teamname']
# 		self.room_group_name = self.room_name
		
# 		# print(self.room_group_name)
# 		async_to_sync(self.channel_layer.group_add)(
# 			self.room_group_name,
# 			self.channel_name
# 		)
# 		self.accept()

# 		self.userdata = TokenTable.objects.get(token_id=self.room_name)
# 		if self.userdata.token_busy:
# 			print("your friend has joind the game.")
# 			self.username = 'receiver'
# 		else:
# 			print("Wait for friend to join...")
# 			self.username = 'creator'

# 		self.send(text_data=json.dumps({
# 			'type':'websocket.accept',
# 			'message':'connection establishing...'
# 			}))
		
# 	# def disconnect(self,close_code):
# 	# 	self.close()

# 	def receive(self,text_data):
# 		text_data_json = json.loads(text_data)
# 		message = text_data_json['message']

# 		async_to_sync(self.channel_layer.group_send)(
# 			self.room_group_name,
# 			{
# 				'type':'chat.message',
# 				'message':message
# 			}
# 		)

# 	def chat_message(self, event):
# 		message = event['message']

# 		self.send(text_data = json.dumps({
# 			'type':'chat',
# 			'message':message

# 		}))

#------------------------------------------------------------
#rough
#Note:
# 	@database_sync_to_async
# 	def checkgroupexist(self, group_name):
# 		return TokenSenderTable.objects.filter(token_id=group_name).exists()
# 	
#Note : 
#MyModel.objects.update_or_create(group=group_name, defaults={'variable': self.variable})
