from blessed import Terminal

term = Terminal()

with term.enable_kitty_keyboard(
        report_events=True,
        report_all_keys=True):
    with term.cbreak():
        while True:
            key = term.inkey()

            if key:
                print(
                    key.key_name,
                    "pressed=", key.pressed,
                    "repeated=", key.repeated,
                    "released=", key.released
                )