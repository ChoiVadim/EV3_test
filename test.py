import keyboard

while True:
    event = keyboard.read_event()
    if event.event_type == keyboard.KEY_DOWN:
        if event.name == 'W':
            print('W pressed!')