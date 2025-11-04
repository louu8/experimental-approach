from expyriment import design, control, stimuli
from expyriment.misc.constants import C_WHITE, C_BLACK, K_d, K_s
import random

N_ITEMSETS = 20
TRIAL_TYPES = ["def", "diff-sametopo", "diff2", "diff-difftopo"]
PROPORTIONS = [0.4, 0.2, 0.2, 0.2]   
N_TOTAL_TRIALS = 200
N_PRACTICE_TRIALS = 2

import os

#BASE_DIR = r"C:\Users\charl\CogSup\programming\Assignements\group_project"
IMG_FOLDER = r"SameDiff"

BLANK_DURATION = 500 
FEEDBACK_DURATION = 1000

exp = design.Experiment(name="Topology Line Shift", background_colour=C_WHITE, foreground_colour=C_BLACK)
control.initialize(exp)

def load_stimuli():
    """Load all images by naming convention"""
    items = {}
    for i in range(1, N_ITEMSETS + 1):
        items[i] = {}
        for t in TRIAL_TYPES:
            filename = f"{i}-{t}.png"
            path = os.path.join(IMG_FOLDER,filename)
            items[i][t] = stimuli.Picture(path)
            items[i][t].preload()
    return items

def present_instructions(text):
    screen = stimuli.TextScreen("Instructions", text)
    screen.present()
    exp.keyboard.wait()

def run_trial(set_id, trial_type, base_item, comp_item):
    """Present A → blank → B → collect response"""
    base_item.present()
    exp.clock.wait(800)
    exp.screen.clear(); exp.screen.update()
    exp.clock.wait(BLANK_DURATION)
    comp_item.present()

    key, rt = exp.keyboard.wait([K_d, K_s])
    if (comp_item.filename==base_item.filename and key==K_s) or (any(comp_item.filename[12:] == f"{a}.png" for a in TRIAL_TYPES[1:]) and key==K_d):
        correct = True
    else :
        correct = False

    exp.data.add([set_id, trial_type, key, rt, correct])
    feedback = stimuli.TextLine("Response recorded", text_colour=C_BLACK)
    feedback.present()
    exp.clock.wait(FEEDBACK_DURATION)

stimuli_dict = load_stimuli()

exp.add_data_variable_names(["set_id", "trial_type", "key", "rt", "correct"])

control.start(subject_id=1)
present_instructions("Welcome! You will see two items.\nYour task is to decide if they are the same or different.\nPress D or S.\n\nPress SPACE to start practice.")

practice_trials = random.sample(range(1, N_ITEMSETS + 1), N_PRACTICE_TRIALS)
for pid in practice_trials:
    base = stimuli_dict[pid]["def"]
    comp = stimuli_dict[pid]["diff-sametopo"]
    run_trial(pid, "practice", base, comp)

present_instructions("Practice done. Press SPACE to start the main experiment.")

trial_pool = []
for set_id in range(1, N_ITEMSETS + 1):
    for t in TRIAL_TYPES:
        for _ in range(2):
            trial_pool.append((set_id, t))

trial_pool = trial_pool * 2  
trial_pool = random.sample(trial_pool, N_TOTAL_TRIALS) 

for (set_id, trial_type) in trial_pool:
    base_item = stimuli_dict[set_id]["def"]
    comp_item = stimuli_dict[set_id][trial_type]
    run_trial(set_id, trial_type, base_item, comp_item)

present_instructions("Thank you for participating!\nPress SPACE to end.")
control.end()
