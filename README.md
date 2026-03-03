# NeuroTac 🧠🎮

NeuroTac is an Artificial Neural Network that learns to play Tic Tac Toe using supervised imitation learning (behavior cloning).

The model learns by imitating an optimal rule-based teacher and achieves:

- 100% win rate vs random agent
- 100% draw rate vs optimal teacher

---

## 🧠 Project Overview

This project demonstrates:

- Custom game environment implementation
- Rule-based expert policy
- Dataset generation from gameplay
- Multi-class ANN classifier
- Cross-entropy training
- Performance evaluation
- Interactive Pygame GUI

No reinforcement learning was used.

---

## 🏗 Architecture

Input: 9 board cells  
Hidden Layer: 64 neurons (ReLU)  
Hidden Layer: 64 neurons (ReLU)  
Output: 9 neurons (Softmax move probabilities)

Loss Function: CrossEntropyLoss  
Optimizer: Adam  

---

## 📊 Results

Evaluation vs Random:

Wins: 1000  
Losses: 0  
Draws: 0  

Evaluation vs Teacher:

Wins: 0  
Losses: 0  
Draws: 1000  

---

## 🚀 Installation

```bash
git clone https://github.com/KnoxCodes/NeuroTac.git
cd NeuroTac
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## ▶ Run Project

```bash
python main.py
```

The script will:

1. Generate training data
2. Train the ANN
3. Evaluate performance
4. Launch the GUI

---

## 🎮 How It Works

This project uses supervised imitation learning.

Instead of reinforcement learning, the ANN learns to approximate:

π(s) = a

Where:
- s = board state
- a = optimal move

---

## 🧩 Future Improvements

- Symmetry data augmentation
- Probability heatmap visualization
- Difficulty levels
- Web-based version
- Reinforcement learning comparison

---

## 📜 License

MIT License
