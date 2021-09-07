import random
import csv


class game:
  csvlist = []
  def build_csvlist():
    global csvlist
    with open('sorted_data_items.csv') as csvfile:
      csvlist = list(csv.reader(csvfile))
    return csvlist

  def pull_item(start=2132,end=2964):
    global csvlist
    index = random.randint(start,end)
    return_csvlist = csvlist[index]
    return_csvlist.append(index)
    return return_csvlist
    
  def check_item(price1,price2,round,pity):
    percentage = 1
    base_amount = 1000
    if price1 == price2:
      return random.choice([-1,1])
    if round > 4 and round < 9:
      percentage = .7
      base_amount = 700
    elif round > 8 and round < 13:
      percentage = .5
      base_amount = 500
    elif round > 12:
      percentage = .3
      base_amount = 100
    if pity > 10:
      percentage += pity*.005
    lower_bound = price2-(price2*percentage) 
    
    upper_bound = price2+(price2*percentage)
    if percentage == 1:
      lower_bound = price2-(price2*.7)
    if(price1 > 3000):
      if price1 < lower_bound:
       return -1
      if price1 > upper_bound:
       return 1
    else:
      if pity > 10:
        base_amount += pity*10
      lower_bound_number = price2-base_amount
      upper_bound_number = price2+base_amount
      if price1 < lower_bound_number:
        return -1
      if price1 > upper_bound_number:
        return 1
    return 0

  def correct(price1,price2,input_answer,amount=0):
    if input_answer == '1':
      if price1>price2:
        return True
      return False

    elif input_answer == '2':
      if price1<price2:
        return True
      return False
    #unused in discord version
    if amount == 1:
      print('Ahem... please read the prompt')
    if amount == 2:
      print('...')
    if amount == 3:
      print('This is the last time im asking')
    if amount == 4:
      print('Seriously, I WILL erase your progress')
    if amount == 5:
      print('You know what?')
    if amount == 6:
      print('I dont even care')
    if amount == 7:
      print('I\'m just a bot you\'re the one wasting your time')
    if amount == 8:
      print('waste')
    if amount == 9:
      print('more')
    if amount == 10:
      print('time')
    if amount == 11:
      print('Ok im done doing this')
    if amount >= 12:
      print('...')
    else:
      print('Type 1 for MORE or 2 for LESS only')
      next_answer = input()
      amount+=1
      return game.correct(price1,price2,next_answer,amount)




# game.build_csvlist()
# round = 1
# print('Welcome to Higher or Lower (Runescape Edition): Type 1 to begin')
# print('Note: Unspecified dose potions are assumed to be one dose')
# if input() == '1':
#   while(True):
#     if round == 1:
#       first_item = game.pull_item()
#       second_item = game.pull_item()
#     else:
#       first_item = second_item
#       second_item = game.pull_item()
#     if first_item[0] == second_item[0]:
#       second_item = game.pull_item()
#     pity = 0
#     check_result = game.check_item(int(first_item[1]),int(second_item[1]),round,pity)
#     upper_bound = len(csvlist)
#     lower_bound = 0
#     while(check_result != 0):
#       if(check_result == -1):
#         pity+=1
#         upper_bound = int(second_item[3])
#         second_item = game.pull_item(lower_bound,upper_bound)
#         check_result = game.check_item(int(first_item[1]),int(second_item[1]),round,pity)
#       else:
#         pity+=1
#         lower_bound = int(second_item[3])
#         second_item = game.pull_item(lower_bound,upper_bound)
#         check_result = game.check_item(int(first_item[1]),int(second_item[1]),round,pity)
#     if round == 1:
#       score = 0
#     else:
#       score = math.factorial(round)-1
#     print('\nRound: ' + str(round) + ' Score: ' + str(score))
#     print('Is a(n) "' + first_item[0] + '" worth MORE (1) or LESS (2) than a "' + second_item[0] + '"')
#     response = input()
#     if game.correct(int(first_item[1]),int(second_item[1]),response):
#       print('Correct! The actual prices were')
#       print(first_item[0] + ": " + first_item[1])
#       print(second_item[0] + ": " + second_item[1])
#       round += 1
#     else:
#       print('Nope thats incorrect! The actual prices were')
#       print(first_item[0] + ": " + first_item[1])
#       print(second_item[0] + ": " + second_item[1])
#       if input('Continue? (y/n)\n') == 'y':
#         round = 1
#       else:
#         break
# print('Ok then, Goodbye!')


