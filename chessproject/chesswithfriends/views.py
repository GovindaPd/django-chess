from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
# from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, FileResponse, Http404, HttpResponseForbidden
# raise Http404("Choice does not exists")

import json, string, random, re
from datetime import datetime

from .models import TokenSenderTable, WithComputerToken
from . import content
from .chess.chessbase import ChessBase

currentdate = datetime.today()
context = {
            'title': content.title,
            'websitename': content.websitename,
            'currentyear': currentdate.year,
            }

level_dict = {'noraml':2, 'hard':3}

	
def get_user_ip_address(request):
	#get user IP address
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	
	return ip

def index(request):
	return render(request, 'chesswithfriends/index.html', context)
		

def preaprechessboard(request):
	if request.method == 'POST':
		context['chessman_names'] = {'WE':'\u2656','WK':'\u2654','WQ':'\u2655','WC':'\u2657','WH':'\u2658','WS':'\u2659',
           							'BE':'\u265C','BK':'\u265A','BQ':'\u265B','BC':'\u265D','BH':'\u265E','BS':'\u265F'}
		context['chessman_color'] = {'B':'black', 'W':'white'}
	
		#with computer
		if request.POST.get('type') == 'withcomputer':
			try:
				context['token'] = "".join(random.sample(string.ascii_letters+string.digits, 10))
				while context['token'] in WithComputerToken.objects.values_list('token_id', flat=True):
					context['token'] = "".join(random.sample(string.ascii_letters+string.digits, 10))

				context['color'] = 'W' if request.POST.get('color') not in ('W', 'B') else request.POST['color']
				context['turn'] = context['color']
				# if request.POST.get('level') not in ('noraml', 'hard') else request.POST['level']
				context['level'] = level_dict.get(request.POST['level'], 2)
				context['chessboard'] = ChessBase.BOARD
				context['castle'] = ChessBase.CASTLE
				context['dead_list'] = []

				tb = WithComputerToken.objects.create(token_id=context['token'], token_color=context['color'], 
					 token_turn=context['turn'], chessboard=json.dumps(context['chessboard']), 
					 castle=json.dumps(context['castle']))
				tb.save()
				return render(request, 'chesswithfriends/withcomputer.html', context)
			except Exception as error:
				return redirect('index')


		#Online with friend
		elif request.POST.get('type') == 'onlinewithfriend':
			context['color'] = 'W' if request.POST.get('color') not in ('W', 'B') else request.POST['color']
			try:
				context['time'] = int(request.POST.get('timeinterval', 2))
			except ValueError:
				context['time'] = 2	#minute

			context['token'] = "".join(random.sample(string.ascii_letters+string.digits, 8))
			while context['token'] in TokenSenderTable.objects.values_list('token_id', flat=True):
				context['token'] = "".join(random.sample(string.ascii_letters+string.digits, 8))
			#here flat=True mean only return list of values like [1,2] rather then list of tuples values like [(1,),(2,)] 
			# values() method return lict of dictionary [{'token_id':1},{'token_id':2}]
			
			try:
				tb = TokenSenderTable.objects.create(token_id=context['token'], token_sender_id='sender',
					token_color=context['color'], token_time=context['time'], token_turn=context['color'], 
					token_last_joiner='sender', chessboard=json.dumps(ChessBase.BOARD), castle=json.dumps(ChessBase.CASTLE))
				tb.save()
			except Exception as error:
				#messages.add_message(request, messages.INFO, 'Erorr in inserting in database.')
				return redirect('index')
			
			try:
				tb_read = TokenSenderTable.objects.get(token_id=context['token'])
				context['token'] = tb_read.token_id
				context['whois'] = tb_read.token_sender_id
				context['color'] = tb_read.token_color
				context['turn'] = tb_read.token_turn
				context['time'] = tb_read.token_time
				context['chessboard'] = json.loads(tb_read.chessboard)
				context['castle'] = json.loads(tb_read.castle)
				context['dead_list'] = json.loads(tb_read.dead_list)	
			except Exception as error:
				messages.add_message(request, messages.INFO, 'Something went wrong. Please try again.')
				return redirect('index')
		
			return render(request, 'chesswithfriends/onlinewithfriend.html', context)
		
		# on token submit
		elif request.POST['type'] == 'token_submit':
			token = request.POST.get('token')

			if re.match("^[a-zA-Z0-9]{8}$", token) == None:
				messages.add_message(request, messages.INFO, "Invalid Token")
				return redirect('index')
			try:
				tb_read = get_object_or_404(TokenSenderTable, token_id=token)
				
				if tb_read.token_busy == 1 and tb_read.game_over == False:	
					tb_read.token_busy = 2

					if tb_read.token_sender_id == '':
						tb_read.token_sender = "sender"
						tb_read.token_last_joiner = "sender"
						context['whois'] = "sender"
						context['color'] = tb_read.token_color

					elif tb_read.token_receiver_id == '':
						tb_read.token_receiver_id = "receiver"
						tb_read.token_last_joiner = "receiver"
						context['whois'] = "receiver"
						#receiver_color is annonymous lambda function
						receiver_color = lambda c: 'B' if c=='W' else 'W'
						context['color'] = receiver_color(tb_read.token_color)
					
					tb_read.save()	#commit=True
				
					context['token'] = tb_read.token_id
					context['turn'] = tb_read.token_turn
					context['time'] = tb_read.token_time
					context['chessboard'] = json.loads(tb_read.chessboard)
					context['castle'] = json.loads(tb_read.castle)
					context['dead_list'] = json.loads(tb_read.dead_list)

					return render(request, 'chesswithfriends/onlinewithfriend.html', context)
				else:
					messages.add_message(request, messages.INFO, "This token is busy right now.")
					return redirect('index')

			except Exception as error:
				context['error'] = "Something went wrong. Please try again."
				return render(request, 'chesswithfriends/index.html', context)
		else:
			messages.add_message(request, messages.INFO, "Please select a valid method")
			return redirect('index')
	else:
		return HttpResponse("h1>Method not allowed.</h1>")



def about(request):
	context['content'] = content.about_us
	return render(request, 'chesswithfriends/otherpages.html', context)

def contactus(request):
	context['content'] = content.contactus
	return render(request, 'chesswithfriends/otherpages.html', context)

def terms_and_conditions(request):
	context['content'] = content.terms_and_conditions
	return render(request, 'chesswithfriends/otherpages.html', context)

def privacy_policy(request):
	context['content'] = content.privacy_policy
	return render(request, 'chesswithfriends/otherpages.html', context)

def disclaimer(request):
	context['content'] = content.disclaimer
	return render(request, 'chesswithfriends/otherpages.html', context)


#return HttpResponseRedirect(reverse('index'))
#return redirect('index')
