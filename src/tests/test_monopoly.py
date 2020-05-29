import pytest

from p084_monopoly_odds import monopoly

@pytest.fixture
def player():
    return monopoly.Player()

def test_init_player_class_succeeds(player):
    assert player.pos == 0
    assert len(player.hist.keys()) == 0

def test_player_setpos(player):
    player._setpos(33)
    assert player.pos == 33

def test_move_normal_increment(player):
    player.move(10)
    assert player.pos == 10
    assert player.hist == { 10: 1 }

def test_move_round_start_point(player):
    player._setpos(35)
    player.move(5)
    assert player.pos == 0
    assert player.hist == { 0: 1 }

def test_rolling_community(player):
    n, go_0, go_10 = 0, 0, 0
    for i in range(32):
        cc = player.community_chest(33)
        if cc == 0:
            go_0 += 1
        elif cc == 10:
            go_10 += 1
        else:
            n += 1
    assert go_0 == 2
    assert go_10 == 2
    assert n == 28 

def test_rolling_chance(player):
    n, go_0, go_10, go_11, go_24, go_39, go_5, go_r, go_u, go_3 = 0,0,0,0,0,0,0,0,0,0
    for i in range(32):
        cc = player.chance(33)
        if cc == 0:
            go_0 += 1
        elif cc == 5:
            go_5 += 1
        elif cc == 10:
            go_10 += 1
        elif cc == 11:
            go_11 += 1
        elif cc == 24:
            go_24 += 1
        elif cc == 39:
            go_39 += 1
        elif cc == 35:
            go_r += 1
        elif cc == 12:
            go_u += 1
        elif cc == 30:
            go_3 += 1
        elif cc == 33:
            n += 1
        else:
            assert True == False # You shouldnt be here dude !!
    assert go_0 == 2
    assert go_10 == 2
    assert go_11 == 2
    assert go_24 == 2
    assert go_39 == 2
    assert go_5  == 2
    assert go_r  == 4
    assert go_u  == 2
    assert go_3  == 2
    assert n == 12 

