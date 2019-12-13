import collections
from calculate_score import calc_score
import random
import re
import copy
import os

class Game:
  def __init__(self, print_func=print,input_func=input):
    self._print = print_func
    self._input = input_func
    self.total_rounds = 100_000
    self.current_round = 0

  def begin(self):
    self._print('Welcome to Game of Greed')
    wanna_play = self._input("Wanna play?")  
    if wanna_play == 'y':
      return "new game"
    else:
      self._print ('OK. Maybe another time')
      return ""

  def print_rolls(self, rolled_dice):
    """prints the results of a dice roll.  rolled_dice should be in list form"""
    self._print(f'you rolled {rolled_dice}.\n')


  def calculate_score (self, dice):
    """Takes in a list of integers representing dice rolls.  Returns an integer representing the score of that roll in Farkle"""
    return calc_score(dice)

  def roll_dice(self, n):
    '''Rolls n dice.   Returns the results as a list'''
    results = []
    for _ in range (n):
      results.append(random.randint(1,6))
    return results


  def convert_data (self, dice, user_input):
    """dice data is generated in list form, and user input comes in string form.   This function converts both to collections for use elsewhere in the program.  Also returns user input in list form"""
    dice_c = collections.Counter(dice)
    dice_collection = collections.Counter(dice)
    user_input = re.sub(r'" "', '',user_input).split(",")
    if user_input[-1] == "" or user_input[-1] == " ":
      user_input.pop()
    for i in range(0, len(user_input)): 
      user_input[i] = int(user_input[i]) 
    keepers_collection = collections.Counter(user_input)
    return dice_collection, keepers_collection, user_input

  def prompt_keep_dice(self,dice):
    """Asks the user what dice they dice they want to keep, and calls functions to validate that input.  If input is bad, function recursively calls itself until input is good.  Returns the points scored and the number of dice the player used"""
    keepers = self._input("Which dice would you like to keep? \nKeeping:")
    dice_collection, keepers_collection, keepers_as_list = self.convert_data(dice,keepers)
    valid_input = self.validate_input_matches_roll(dice_collection, keepers_collection)
    if not valid_input:
      self._print("I don't like your sassy little input.   Stick to the dice you actually rolled champ.")
      score, dice_used = self.prompt_keep_dice(dice)
    elif self.user_is_cheating(keepers_as_list):
      self._print("Try again.   You can't keep non-scoring dice.\n")
      score, dice_used = self.prompt_keep_dice(dice)
    else:
      dice_used = len(keepers_as_list)
      score = self.calculate_score(keepers_collection)
      self._print (f"you scored {score}\n")
    return score, dice_used
      

  def user_is_cheating(self, keepers):
    """Checks that the user isn't cheating by keeping non-scoring dice to try and get 6 fresh ones.  For example, attempting to keep [6,6,1,1] Returns true/false"""
    potential_score = self.calculate_score(keepers)
    for i in keepers:
      val = keepers.pop(0)
      if potential_score == self.calculate_score(keepers):
        return True
      keepers.append(val)
    return False
    

  def validate_input_matches_roll(self, dice, keepers):
    """Checks to make sure the set of kept dice is entirely contained within the set of dice that were rolled.  Returns true/false"""
    for i in keepers:
      if keepers[i]>dice[i]:
        return False
    return True
 
  def prompt_reroll(self, num):
    """asks the user if they'd like to re-roll.  Returns true if yes, and false if no, and keeps them trapped in recursive until the input is valid"""
    ans = self._input(f"You have {num} dice left.\nRoll Again?  y/n:  ")
    if ans == "y":
      return True
    elif ans == "n":
      return False
    else:
      self._print("Invalid input.  Try again")
      return self.prompt_reroll(num)

  
  def play_one_round(self):
    """Control function that handles exactly one round of Farkle.  Round structure is as follows:
    * While the Round is ongoing
      *  Player Rolls Dice
      *  Dice Roll is printed to screen
      *  The score of submitting all dice is evaluted.
      *  If that score is zero, the player farkled.  Score for the round is 0, and the round is over.
      *  If the player didn't farkle, they're asked which dice they'd like to keep
      *  They're asked this repeatedly, until they enter a valid input.
      *  Score of kept dice is evaluated and added to round score.
      *  Player is prompted if they'd like to bank or re-roll
      *  If player banks, round ends.
      *  If player re-rolls, return to 1
      
      Returns score for the round"""
    
    score = 0
    round_ongoing = True
    dice_left = 6
    while round_ongoing:
      dice = self.roll_dice(dice_left)
      self.print_rolls(dice)
      # checking for a farkle
      did_not_farkle = self.calculate_score(dice)
      self._print (f"Score on the round thus far: {score}\nmax score possible from these dice = {did_not_farkle}\n")
      if not did_not_farkle: #if farkled
        score = 0
        break
      # player did not farkle

      roll_score, dice_used = self.prompt_keep_dice(dice)
      score += roll_score
      dice_left -= dice_used
      if dice_left == 0:
          dice_left=6
          self._print ("Hot Streak! Bonus Dice!")
      round_ongoing = self.prompt_reroll(dice_left)
    return score


  def play(self):
    """Main control function.  Runs the actual game"""
    new_game = self.begin()
    if new_game:
      score = 0
      for self.current_round in range (self.total_rounds):
        self._print (f"It is round {self.current_round + 1} of {self.total_rounds} and your score is {score}")
        points = self.play_one_round()
        # os.system('clear')
        score += points
        if points == 0:
          self._print("You farkled out.  The round is over :(")
        else:
          self._print(f"you scored {points} points last round")
      self._print(f"your final score was {score}")


if __name__ == "__main__":
    game = Game()
    game.play()
