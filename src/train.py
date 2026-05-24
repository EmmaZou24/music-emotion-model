import torch
import torch.nn as nn
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix

def train_model(model, train_loader, val_loader, epochs, lr=1e-3, device=DEVICE, model_path="results/best_model.pt"):
  model.to(device)
  optimizer = optim.Adam(model.parameters(), lr=lr)
  best_val_F1 = float('-inf')
  history = {
    'train_loss': [],
    'val_loss': [],
    'val_accuracy': [],
    'val_F1': []
  }
  criterion = nn.CrossEntropyLoss(weight=class_weights)

  for _ in range(epochs):
    model.train()
    running_loss = 0.0

    for images, tabular, labels, _ in train_loader:
      images = images.to(device)
      tabular = tabular.float().to(device)
      labels = labels.to(device).long()

      logits = model(images, tabular)
      loss = criterion(logits, labels)

      optimizer.zero_grad()
      loss.backward()
      optimizer.step()
      running_loss += loss.item()

    avg_loss = running_loss / len(train_loader)
    metrics = evaluate_model(model, val_loader, device)

    history['train_loss'].append(avg_loss)
    history['val_accuracy'].append(metrics['accuracy'])
    history['val_F1'].append(metrics['F1'])
    history['val_loss'].append(metrics['avg_val_loss'])

    current_F1 = metrics['F1']
    if not np.isnan(current_F1) and current_F1 >= best_val_F1:
      best_val_F1 = current_F1
      torch.save(model.state_dict(), model_path)

  print(best_val_F1)
  return history