from load_positions import *
from neural_network import *
from train import train

BATCH_SIZE = 64
EPOCHS = 10
LR = 0.001
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print("LOADING PGN and BUILDING DATASET")
X, y, _, _ = load_positions_with_result(
    pgn_path="games/Modern.pgn", 
    games=100)
print(f"Dataset size: {len(X)} positions")


print("Initializing model...")
model = EvalNet()

print("Training model...")
train(model, X, y, epochs=EPOCHS, batch_size=BATCH_SIZE, lr=LR)

# Save model
torch.save(model.state_dict(), "chess_eval_model.pt")
print("Model saved as chess_eval_model.pt")