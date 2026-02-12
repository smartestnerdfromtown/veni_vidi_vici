import chess
import chess.pgn
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import TensorDataset, DataLoader


PGN_PATH = "big_games.pgn"
BATCH_SIZE = 64
EPOCHS = 10
LR = 0.001
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

def train(
        model, 
        X, 
        y, 
        epochs=10, 
        batch_size=64, 
        lr=0.001):
    
    dataset = TensorDataset(X, y) 
    loader = DataLoader(
                dataset=dataset, 
                batch_size=batch_size, 
                shuffle=True
    )

    model.to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.MSELoss()

    for epoch in range(epochs):
        total_loss = 0
        for xb, yb in loader:
            xb, yb = xb.to(DEVICE), yb.to(DEVICE)
            optimizer.zero_grad()
            out = model(xb)
            loss = loss_fn(out, yb)
            loss.backward()
            optimizer.step()
            total_loss += loss.item() * xb.size(0)
        print(f"Epoch {epoch+1}/{epochs}," 
              f"Loss: {total_loss/len(dataset):.4f}")



