import time
import sys
import json


class TerminalTimer:
    modes = {"F": "focus_time", "M": "meditation_time"}
    indent = "                  "

    def __init__(self):
        self.mode = None
        self.duration = 0


    def set_mode(self):
        mode = str(input(
            "Input F if you want to focus, input M if you want to meditate:"
            ))
        while True:
            try:
                if mode not in [str('F'), str('M'), str('f'), str('m')]:
                    raise ValueError("Wrong value")
                self._delete_line()
                return str(mode).upper()
            
            except ValueError:
                print("Hm, it looks like you inputed a wrong letter!")
                mode = input(
                    "Input F if you want to focus, input M if you want to meditate:")


    def set_time(self, mode):
        while True:
            if mode == 'F':
                print('How much time do you want to focus?')
                duration = input("Minutes: ")
                self._delete_line()
            elif mode == 'M':
                print('How long do you want to meditate?')
                duration = input("Minutes: ")
                self._delete_line()
            try:
                duration = int(duration)
                if duration == 1:
                    print(f"The timer is set to {duration} minute") # 1 minute scenario
                else:
                    print(f"The timer is set to {duration} minutes")

                duration = duration * 60 # Convert to seconds
                return duration
            except ValueError:
                print("Please make sure to input the number!")


    def start_timer(self, duration, mode):
        with open("sprout.txt", "r") as ascii_art:
            # Print a sprout art at the start of the session
            sys.stdout.write(ascii_art.read())
            print()

        for i in range(duration, 0, -1):
            minutes, seconds = self._convert_number(i)

            # Overwrite the current line
            sys.stdout.write("\r" + self.indent + str(minutes) + ':' + str(seconds))
            sys.stdout.flush()
            time.sleep(1)

        with open("tree.txt", "r") as tree_art, open('tomato.txt') as tomato_art:
            # Print a grown tree art at the end
            # Remove the lines above to overwrite the sprout image
            for i in range(16):
                self._delete_line()
            if mode == 'M':
                sys.stdout.write(tree_art.read())
            elif mode == 'F':
                sys.stdout.write(tomato_art.read())

        total_minutes, total_seconds = self._convert_number(duration)
        print("\n" + self.indent + str(total_minutes) + ':' + str(total_seconds)) 

        self._save_session(duration, "data.txt", mode)
        total_duration = str(self._get_total_time("data.txt", mode))
        print()
        if mode == 'F':
            print("\rCongrats on finishing the focus session \U0001F389")
            print(f"Total time spent focusing: {total_duration} minutes")
        elif mode == 'M':
            print("\rCongrats on finishing the meditation session \U0001F64F")
            print(f"Total time spent practicing: {total_duration} minutes")


    def _save_session(self, duration, file, mode):
        current_time = time.time()
        with open(file, 'a') as repo:
            session = {}
            session['id'] = self._generate_id(file)
            session['time'] = current_time
            session[self.modes[mode]] = duration
            repo.write(json.dumps(session))
            repo.write("\n")


    def _get_total_time(self, file, mode):
        with open(file, 'r') as repo:
            repo = [json.loads(r) for r in repo.readlines()]
            result = 0 # Store total time in the result variable
            for line in repo:
                try:
                    result += int(line[self.modes[mode]])
                except KeyError:
                    pass

            result /= 60
            return result


    def _generate_id(self, file):
        with open(file, 'r') as repo:
            try:
                return json.loads(repo.readlines()[-1])['id'] + 1
            except IndexError:
                return 0
    

    def _double_digit_time(self, time):
        if len(str(time)) == 1:
            time = str(0) + str(time)
        return time
    

    def _convert_number(self, duration):
        if duration >= 60:
            minutes = duration // 60
            seconds = duration % 60
        else:
            minutes = 0
            seconds = duration

        # Adding a zero before a number if it's a signle digit
        # For example, transform 2:0 -> 02:00 
        minutes = self._double_digit_time(minutes)
        seconds = self._double_digit_time(seconds)
        return minutes, seconds


    def _delete_line(self):
        sys.stdout.write("\033[A")  # Move cursor up one line
        sys.stdout.write("\033[K")  # Clear to the end of line


if __name__ == "__main__":
    print("Hello! What do you want to do today? \U0001F31E\U0001F33F\U0001F9D8")
    timer = TerminalTimer()

    mode = timer.set_mode()
    duration = timer.set_time(mode)

    timer.start_timer(duration, mode)