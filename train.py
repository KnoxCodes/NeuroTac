import torch
import torch.optim as optim
import matplotlib.pyplot as plt
from model import ANN

def train_model(X, y, epochs=30):
    model = ANN()
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    criterion = torch.nn.CrossEntropyLoss()

    X = torch.FloatTensor(X)
    y = torch.LongTensor(y)

    losses = []

    for epoch in range(epochs):
        optimizer.zero_grad()
        outputs = model(X)
        loss = criterion(outputs, y)
        loss.backward()
        optimizer.step()

        losses.append(loss.item())
        print(f"Epoch {epoch+1}: Loss = {loss.item():.4f}")

    torch.save(model.state_dict(), "saved_model.pth")

    # Plot loss curve
    plt.plot(losses)
    plt.title("Training Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.show()

    return model