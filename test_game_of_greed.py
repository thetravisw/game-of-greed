import pytest
from game_of_greed import Game


# IO Testing

def test_greeting(test_game):
  set_scripts(['Welcome to Game of Greed'])

def test_wanna_play_1(test_game):
  set_scripts(['Welcome to Game of Greed'],['Wanna play?'])
  test_game.play()

def test_wanna_play_yes(test_game):
  set_scripts(['Welcome to Game of Greed', "Great! Check back tomorrow :D"],['Wanna play?'],["y"])
  test_game.play()


def test_wanna_play_no(test_game):
  set_scripts(['Welcome to Game of Greed',"OK. Maybe another time"],['Wanna play?'],["n"])
  test_game.play()

#  Scoring Testing

def test_1s(test_game):
  assert test_game.calculate_score([2,2,1,3,4,4]) == 100
  assert test_game.calculate_score([2,2,1,3,1,4]) == 200
  assert test_game.calculate_score([2,2,1,3,1,1]) == 1000
  assert test_game.calculate_score([2,1,1,3,1,1]) == 2000

def test_1_thru_six(test_game):
  for i in range (1,7):
    if i == 1:
      multiplier = 1000
    else:
      multiplier = 100*i
    if i == 1:
      assert test_game.calculate_score([i]) == 100
      assert test_game.calculate_score([i,i]) == 200
    elif i == 5:
      assert test_game.calculate_score([i]) == 50
      assert test_game.calculate_score([i,i]) == 100
    else:
      assert test_game.calculate_score([i]) == 0
      assert test_game.calculate_score([i,i]) == 0
    assert test_game.calculate_score([]) == 0
    assert test_game.calculate_score([i,i,i]) == multiplier
    assert test_game.calculate_score([i,i,i,i]) == 2*multiplier
    assert test_game.calculate_score([i,i,i,i,i]) == 3*multiplier
    if i < 6:
      assert test_game.calculate_score([i,i,i, i+1,i+1,i+1]) == multiplier + 100*(i+1)
  assert test_game.calculate_score([2,2]) == 0
  

def test_straight(test_game):
  assert test_game.calculate_score([1,2,3,4,5,6]) == 1500
  assert test_game.calculate_score([7,2,3,4,4,6]) == 0

def test_3pair(test_game):
  assert test_game.calculate_score([2,2,3,3,4,4]) == 1500

def test_McFlurry(test_game):
  assert test_game.calculate_score([5,5,5,5,1,1]) == 2000

def test_zilch(test_game):
  assert test_game.calculate_score([2,2,3,3,4,6]) == 0




# Scripts for IO testing 

scripts = {
    'prints' : [],
    'prompts' : [],
    'inputs' : [],
}

def set_scripts(prints=[], prompts=[],inputs=[]):
    scripts['prints'] = prints
    scripts['prompts'] = prompts
    scripts['inputs'] = inputs

@pytest.fixture()
def test_game():
  return Game(mock_print, mock_input)
    
def mock_print(msg, *args):
  if len(scripts['prints']):
    assert scripts['prints'].pop(0) == msg


def mock_input(prompt, *args):
  if len(scripts['prompts']):
    assert prompt == scripts['prompts'].pop(0)

  if len(scripts['inputs']):
    return scripts['inputs'].pop(0)