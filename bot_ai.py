from game_of_greed import Game

class AllThePointsPlayer:
  round_score = 0

  def _init_(self):
    self.roll = None
    self.game = None

  def _print(self, *args):
    msg = args[0]
    
    if msg.startswith('you rolled '):
      self.roll = [int(char) for char in msg if char.isdigit()]
    print(msg)

  def _input(self, *args):
    question = args[0]

    if question == "Wanna play?":
      print(question,'y')
      return 'y'

    if question.startswith("You have "):
      wanna = self.wanna_reroll(int(question[9]))
      print (question, wanna)
      return wanna
      
    if question == "Which dice would you like to keep? \nKeeping:":
      return self.what_to_keep()

  def what_to_keep(self):
    target_score = self.game.calculate_score(self.roll)
    if target_score < 401 and 1 in self.roll:
      self.round_score +=100
      return "1"
    elif target_score < 401 and 5 in self.roll:
      self.round_score +=50
      return "5"
    else:
      self.round_score += target_score
      keeping = ""
      for i in self.roll:
        val = self.roll.pop(0)
        if target_score > self.game.calculate_score(self.roll):
          keeping += f"{val}, "
        self.roll.append(val)
      return keeping

  def wanna_reroll(self, numdice):
    if numdice <3 and self.round_score > 201:
      self.round_score = 0
      return 'n'
    else:
      return 'y'




if __name__ == "__main__":
    bot = AllThePointsPlayer()
    game = Game(bot._print, bot._input)
    bot.game = game
    game.play()
