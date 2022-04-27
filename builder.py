import random
import json
import torch
from neuralNet import NeuralNet
from nlp import bag_of_words, tokenize
from autodesigner.window.py_new_form import PyNewFormHandler

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
with open("intents.json", 'r') as json_data:
    intents = json.load(json_data)

FILE = "TrainData.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

# --------------------------------------------------------

Name = "BOB"

from listen import Listen
from speak import Say
from task import InputExecution
from task import NonInputExecution


def Main():
    sentence = Listen()
    result = str(sentence)

    if sentence == "exit":
        exit()

    obj = PyNewFormHandler()
    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)

    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                reply = random.choice(intent["responses"])

                if "open qt designer" in reply:
                    obj.open_designer()

                elif "open startup dialog" in reply:
                    obj.check_startup_dialog()

                elif "open ui file" in reply:
                    obj.open_file()

                elif "select main window form" in reply:
                    obj.create_from_templates("main_window")

                elif "select new widget" in reply:
                    obj.create_from_templates("widget")

                elif "select dialog without button" in reply:
                    obj.create_from_templates("no_btn_dialog")

                elif "select dialog with right buttons" in reply:
                    obj.create_from_templates("right_btn_dialog")

                elif "select dialog with bottom buttons" in reply:
                    obj.create_from_templates("bottom_btn_dialog")

                elif "close startup dialog" in reply:
                    obj.close_new_form_dialog()

                elif "close qt designer" in reply:
                    obj.close_designer()

                elif "drag push button to top of window" in reply:
                    obj.drag_element_to_window("push_button", "top")

                elif "drag push button to bottom of window" in reply:
                    obj.drag_element_to_window("push_button", "bottom")

                elif "drag push button to left of window" in reply:
                    obj.drag_element_to_window("push_button", "left")

                elif "drag push button to right of window" in reply:
                    obj.drag_element_to_window("push_button", "right")

                elif "drag push button to center of window" in reply:
                    obj.drag_element_to_window("push_button", "center")

                elif "create login form" in reply:
                    obj.create_login_form()

                elif "create signup form" in reply:
                    obj.create_signup_form()

                else:
                    Say(reply)


while True:
    Main()
