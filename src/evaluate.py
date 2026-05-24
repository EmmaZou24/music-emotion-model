import torch
import torch.nn as nn
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix

def evaluate_model(model, dataloader, device=DEVICE):
  model.eval()
  all_y = []
  all_y_pred = []
  all_probs = []
  criterion = nn.CrossEntropyLoss(weight=class_weights.to(device))
  val_loss = 0.0

  with torch.no_grad():
    for images, tabular, labels, _ in dataloader:
      images = images.to(device)
      tabular = tabular.float().to(device)
      labels = labels.to(device).long()

      logits = model(images, tabular)
      probs = torch.softmax(logits, dim=1)
      preds = torch.argmax(logits, dim=1)

      loss = criterion(logits, labels)
      val_loss += loss.item()

      all_y.append(labels.detach().cpu().numpy())
      all_y_pred.append(preds.detach().cpu().numpy())
      all_probs.append(probs.detach().cpu().numpy())

  y_true = np.concatenate(all_y)
  y_pred = np.concatenate(all_y_pred)
  y_prob = np.vstack(all_probs)

  metrics = dict()
  metrics['accuracy'] = accuracy_score(y_true, y_pred)
  n_classes = y_prob.shape[1]
  metrics['F1'] = f1_score(
        y_true,
        y_pred,
        average='macro'
      )
  metrics['confusion_matrix'] = confusion_matrix(y_true, y_pred, labels=np.arange(n_classes))
  metrics['avg_val_loss'] = val_loss / len(dataloader)
  return metrics