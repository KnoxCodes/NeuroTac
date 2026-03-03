from dataset import generate_dataset
from train import train_model
from evaluate import evaluate
from gui import run_gui
import torch
from model import ANN

def main():
    print("Generating dataset...")
    X,y = generate_dataset()

    print("Training...")
    model = train_model(X,y)

    print("Evaluating...")
    evaluate(model,"random")
    evaluate(model,"teacher")

    print("Launching GUI...")
    run_gui(model)

if __name__ == "__main__":
    main()