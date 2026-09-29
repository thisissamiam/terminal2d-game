from blessed import Terminal

term = Terminal()

with term.enable_kitty_keyboard(
        report_events=True,
        report_all_keys=True):
    with term.cbreak():
        while True:
            key = term.inkey()

            if key:
                print("----------------")
                print("str:", key)
                print("repr:", repr(key))
                print("key_name:", key.key_name)
                print("code:", key.code)
                print("pressed:", key.pressed)
                print("repeated:", key.repeated)
                print("released:", key.released)