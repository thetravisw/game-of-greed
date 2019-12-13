from game_of_greed import Game

class AllThePointsPlayer:
  round_score = 0

  def _init_(self):
    self.round_score = None
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
      numdice = int(question[9])
      if numdice <3 and self.round_score < 333:
        round_score=0
        print (question, "n")
        return 'n'
      else:
        print (question, "y")
        return 'y'

    if question == "Which dice would you like to keep? \nKeeping:":
      target_score = self.game.calculate_score(self.roll)
      self.round_score += target_score
      keeping = ""
      for i in self.roll:
        val = self.roll.pop(0)
        if target_score > self.game.calculate_score(self.roll):
          keeping += f"{val}, "
        self.roll.append(val)
      return keeping



if __name__ == "__main__":
    bot = AllThePointsPlayer()
    game = Game(bot._print, bot._input)
    bot.game = game
    game.play()
