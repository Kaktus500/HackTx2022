import PySimpleGUI as sg

from Abilities import Abilities


def print_nick_name(nickname):
    print(nickname)


def print_task(task):
    print(task)


def find_val(values):
    for i in range(4):
        if values[i] is True:
            return i


class ThisIsTerrible:
    actions = {}
    start = 1

    def start_window(self):
        """The initial screen shown by the gui"""
        sg.theme("Dark Amber")
        layout = [[sg.Text("Start Training"), sg.Button("Train")],
                  [sg.Text("Update Models"), sg.Button("Update")],
                  [sg.Button("Exit")]]
        window = sg.Window("Start", layout)
        while True:
            event, values = window.read()
            if event == "Train":
                window.close()
                self.training_window()
                break
            if event == "Update":
                window.close()
                self.update_window()
                break
            if event in (sg.WIN_CLOSED, 'Exit'):
                break
        window.close()

    def training_window(self):
        sg.theme("Dark Amber")
        layout = [[sg.Text("Nickname"), sg.Input(key="-NICKNAME-")],
                  [sg.Text("Process Name"), sg.Input(key="-PROCESS-")],
                  [sg.Radio(ability.name, "AbilityRadio")
                   for ability in Abilities],
                  [sg.Button("Start"), sg.Button("Exit")]]
        window = sg.Window("Training", layout)
        while True:
            event, values = window.read()
            if event == "Start":
                window.close()
                self.actions[self.start] = {}
                self.actions[self.start]["-NICKNAME-"] = values["-NICKNAME-"]
                self.actions[self.start]["-PROCESS-"] = values["-PROCESS-"]
                # determine which radio button was pressed
                key = find_val(values)
                self.actions[self.start]["-ACTION-"] = Abilities(key).name
                self.start += 1
                print_nick_name(values["-NICKNAME-"])
                print_task(values["-PROCESS-"])
                self.start_window()
                break
            if event in (sg.WIN_CLOSED, 'Exit'):
                break
        window.close()

    def update_window(self):
        sg.theme("Dark Amber")
        layout = [[sg.Text("Nickname"), sg.Text("Process"), sg.Text("Action Performed")]]
        layout += [[sg.Text(self.actions[action]["-NICKNAME-"]),
                    sg.Text(self.actions[action]["-PROCESS-"]),
                    sg.Text(self.actions[action]["-ACTION-"]),
                    sg.Button(button_text="DELETE", key=action),
                    sg.Button(button_text="Edit", key=-action)]
                   for action in self.actions]
        layout += [[sg.Button("Back"), sg.Button("Exit")]]
        window = sg.Window("Training", layout)
        while True:
            event, values = window.read()
            if type(event) == int:
                if event > 0:
                    window.close()
                    self.actions.pop(event)
                    self.start_window()
                    break
                else:
                    window.close()
                    self.edit_window(-event)

            if event == "BACK":
                window.close()
                self.start_window()
                break
            if event in (sg.WIN_CLOSED, 'Exit'):
                break
        window.close()

    def edit_window(self, key):
        before_vals = self.actions[key]
        sg.theme("Dark Amber")
        layout = [[sg.Text("Nickname"), sg.Input(default_text=before_vals["-NICKNAME-"], key="-NICKNAME-")],
                  [sg.Text("Task"), sg.Input(default_text=before_vals["-PROCESS-"], key="-PROCESS-")],
                  [sg.Radio(ability.name, "AbilityRadio", default=ability.name == before_vals["-ACTION-"])
                   for ability in Abilities],
                  [sg.Button("Confirm Edits"), sg.Button("Exit")]]
        window = sg.Window("Training", layout)
        while True:
            event, values = window.read()
            if event == "Confirm Edits":
                window.close()
                self.actions[key]["-NICKNAME-"] = values["-NICKNAME-"]
                self.actions[key]["-PROCESS-"] = values["-PROCESS-"]
                # determine which radio button was pressed
                key1 = find_val(values)
                self.actions[key]["-ACTION-"] = Abilities(key1).name
                print_nick_name(values["-NICKNAME-"])
                print_task(values["-PROCESS-"])
                self.start_window()
                break
            if event in (sg.WIN_CLOSED, 'Exit'):
                break
        window.close()

    def __init__(self):
        self.start = 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Terrible = ThisIsTerrible()
    Terrible.start_window()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
