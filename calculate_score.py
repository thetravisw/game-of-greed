import collections

def calc_score(dice):
    """Input of dice roll as a list.  Output score"""
    score = 0
    dice = collections.Counter(dice)

    # checking for 6 dice rolls (straight, 3 pair, McFlurry
    straight = True
    pairs = 0
    if sum(dice.values()) == 6:
      for i in dice:
        if dice[i] != 1:
          straight = False
        if dice[i] == 2:
          pairs +=1
      if straight:
        return 1500 
      if pairs == 3:
        return 1500
      if dice[5] == 4 and dice[1] ==2:
        return 2000

    # checking for 3-6 of a kind
    for i in dice:
      multiplier = 100*i
      if i == 1:
        multiplier*=10
      if dice[i] > 2:
        score += (dice[i]-2)*multiplier

    # checking for 1s
    if dice[1] < 3:
      score += dice[1]*100

    # checking for 5s
    if dice [5] < 3:
      score += dice[5]*50
    
    return score
