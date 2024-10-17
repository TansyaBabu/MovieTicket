from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
import numpy as np

# Example data (replace these with your actual data)
# y_test should be the true binary labels
# y_pred_proba should be the predicted probabilities for the positive class

# Example data
y_test = np.array([0, 0, 1, 1])  # Replace with your actual test labels
y_pred_proba = np.array([0.1, 0.4, 0.35, 0.8])  # Replace with your actual predicted probabilities

# Compute ROC curve and ROC area
fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
roc_auc = auc(fpr, tpr)

# Plotting the ROC curve
plt.figure()
plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic')
plt.legend(loc="lower right")
plt.show()
