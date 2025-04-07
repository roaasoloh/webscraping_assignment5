import pandas as pd

# Load the cleaned dataset
df = pd.read_csv("cleaned_ebay_deals.csv")
print("Loaded rows:", len(df))

# Create a new column: high_discount (True if discount > 20%)
df['high_discount'] = df['discount_percentage'] > 20

# Display sample rows
print(df[['price', 'original_price', 'discount_percentage', 'high_discount']].head())
# Features (X): price and original price
X = df[['price', 'original_price']]

# Target (y): high_discount (boolean)
y = df['high_discount']
print("Final dataset shape (X):", X.shape)
print("Final labels shape (y):", y.shape)

from sklearn.model_selection import train_test_split

# 80% training, 20% testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
from sklearn.linear_model import LogisticRegression

# Initialize and train the model
model = LogisticRegression()
model.fit(X_train, y_train)
from sklearn.metrics import accuracy_score, classification_report

# Predict on test data
y_pred = model.predict(X_test)

# Evaluate performance
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

# Detailed performance report
print(classification_report(y_test, y_pred))
import seaborn as sns
import matplotlib.pyplot as plt

# Plot prediction counts
sns.countplot(x=y_pred)
plt.title("Predicted: High Discount Classification")
plt.xlabel("High Discount (True/False)")
plt.ylabel("Number of Products")
plt.show()
