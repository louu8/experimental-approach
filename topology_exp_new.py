from expyriment import design, control, stimuli
from expyriment.misc.constants import C_WHITE, C_BLACK, K_d, K_s
import random

N_ITEMSETS = 20
TRIAL_TYPES = ["def", "diff-sametopo", "diff2", "diff-difftopo"]
N_PRACTICE_TRIALS = 2

import os

IMG_FOLDER = r"SameDiff"

BLANK_DURATION = 500 
FEEDBACK_DURATION = 1000

exp = design.Experiment(name="Topology Exp", background_colour=C_WHITE, foreground_colour=C_BLACK)
control.initialize(exp)

def load_stimuli():
    items = {}
    for i in range(1, N_ITEMSETS + 1):
        items[i] = {}
        for t in TRIAL_TYPES:
            filename = f"{i}-{t}.png"
            path = os.path.join(IMG_FOLDER, filename)
            items[i][t] = stimuli.Picture(path)
            items[i][t].preload()
    return items

def present_instructions(text):
    screen = stimuli.TextScreen("Instructions", text)
    screen.present()
    exp.keyboard.wait()

def run_trial(set_id, trial_type, base_item, comp_item):
    base_item.present()
    exp.clock.wait(800)
    exp.screen.clear(); exp.screen.update()
    exp.clock.wait(BLANK_DURATION)
    comp_item.present()

    key, rt = exp.keyboard.wait([K_d, K_s])
    is_same = (trial_type == "def")
    correct = (is_same and key == K_s) or (not is_same and key == K_d)

    exp.screen.clear()
    exp.screen.update()
    exp.clock.wait(BLANK_DURATION)

    exp.data.add([set_id, trial_type, key, rt, correct])
    if trial_type=="practice":
        feedback = stimuli.TextLine(f"Response recorded : {correct}", text_colour=C_BLACK)
        feedback.present()
        exp.clock.wait(FEEDBACK_DURATION)

stimuli_dict = load_stimuli()

exp.add_data_variable_names(["set_id", "trial_type", "key", "rt", "correct"])

control.start(subject_id=1)
present_instructions("Welcome! You will see two items.\nYour task is to decide if they are the same (S) or different (D).\nPress D or S.\n\nPress SPACE to start practice.")

practice_trials = random.sample(range(1, N_ITEMSETS + 1), N_PRACTICE_TRIALS)
for pid in practice_trials:
    base = stimuli_dict[pid]["def"]
    comp = stimuli_dict[pid]["diff-sametopo"]
    run_trial(pid, "practice", base, comp)

present_instructions("Practice done. Press SPACE to start the main experiment.")

trial_pool = []

for set_id in range(1, N_ITEMSETS + 1):
    trial_pool.extend([
        (set_id, "def"),
        (set_id, "def"),
        (set_id, "diff-sametopo"),
        (set_id, "diff2"),
        (set_id, "diff-difftopo"),
    ])

trial_pool = trial_pool * 2

random.shuffle(trial_pool) 

for (set_id, trial_type) in trial_pool:
    base_item = stimuli_dict[set_id]["def"]
    comp_item = stimuli_dict[set_id][trial_type]
    run_trial(set_id, trial_type, base_item, comp_item)

present_instructions("Thank you for participating!\nPress SPACE to end.")
control.end()
