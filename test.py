from UI import Button

def do_nothing(*agrs):
    return 1

def test_button():
    b = Button(10, 10, ['keys/add_song1.png'], ['keys/add_song1.png'], ['keys/add_song1.png'], do_nothing)
    assert b.is_in((10, 10))
    assert b.is_in((15, 15))
    assert not b.is_in((100, 100))
