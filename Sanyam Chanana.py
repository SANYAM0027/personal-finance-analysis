import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# 1. Load Dataset
# -----------------------------
data = pd.read_csv("/Users/sanyamchanana/Desktop/personal-finance.csv")

# Check columns (always good practice)
print(data.columns)

# -----------------------------
# 2. Data Preprocessing
# -----------------------------

# Convert Transaction_Date column to datetime
data['Transaction_Date'] = pd.to_datetime(data['Transaction_Date'])

# Create Month column
data['Month'] = data['Transaction_Date'].dt.to_period('M')

# Create Income column
data['Income'] = data.apply(
    lambda row: row['Amount'] if row['Transaction_Type'] == 'Income' else 0,
    axis=1
)

# Create Expense column
data['Expense'] = data.apply(
    lambda row: row['Amount'] if row['Transaction_Type'] == 'Expense' else 0,
    axis=1
)

# -----------------------------
# 3. Monthly Expense Trend (Bar Graph)
# -----------------------------

monthly_expense = data.groupby('Month')['Expense'].sum()

plt.figure(figsize=(10,5))
monthly_expense.plot(kind='bar')

plt.title("Monthly Expense Trend")
plt.xlabel("Month")
plt.ylabel("Total Expense")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# -----------------------------
# 4. Category-wise Expense Analysis
# -----------------------------

# Filter only Expense transactions
expense_data = data[data['Transaction_Type'] == 'Expense']

# Group by Category
category_expense = expense_data.groupby('Category')['Amount'].sum().sort_values(ascending=False)

plt.figure(figsize=(10,6))
category_expense.plot(kind='bar')

plt.title("Category-wise Expense Distribution")
plt.xlabel("Category")
plt.ylabel("Total Expense")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# -----------------------------
# 5. Income vs Expense Share (Pie Chart)
# -----------------------------

# Calculate totals correctly
total_income = data[data['Transaction_Type'] == 'Income']['Amount'].sum()
total_expense = data[data['Transaction_Type'] == 'Expense']['Amount'].sum()

plt.figure(figsize=(6,6))
plt.pie(
    [total_income, total_expense],
    labels=['Income', 'Expense'],
    autopct='%1.1f%%'
)

plt.title("Income vs Expense Share")

plt.tight_layout()
plt.show()

# -----------------------------
# 6. Savings Calculation
# -----------------------------

# Calculate totals properly
total_income = data.loc[data['Transaction_Type'] == 'Income', 'Amount'].sum()
total_expense = data.loc[data['Transaction_Type'] == 'Expense', 'Amount'].sum()

# Calculate savings
savings = total_income - total_expense

# Print formatted results
print(f"Total Income: ₹{total_income:,.2f}")
print(f"Total Expense: ₹{total_expense:,.2f}")
print(f"Total Savings: ₹{savings:,.2f}")

# Calculate savings rate safely
if total_income > 0:
    savings_rate = (savings / total_income) * 100
    print(f"Savings Rate: {savings_rate:.2f}%")
else:
    print("Savings Rate: Cannot calculate (Income is 0)")

# -----------------------------
# 7. Monthly Savings Trend
# -----------------------------

# Create monthly summary table
monthly_summary = (
    data.groupby(['Month', 'Transaction_Type'])['Amount']
    .sum()
    .unstack(fill_value=0)
)

# Create Savings column
monthly_summary['Savings'] = monthly_summary['Income'] - monthly_summary['Expense']

# Plot Savings Trend
plt.figure(figsize=(10,5))
monthly_summary['Savings'].plot(marker='o')

plt.title("Monthly Savings Trend")
plt.xlabel("Month")
plt.ylabel("Savings")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# -----------------------------
# 8. Top 5 Highest Expenses
# -----------------------------

# Filter only expense transactions
expense_data = data[data['Transaction_Type'] == 'Expense']

# Sort by Amount (highest first)
top_expenses = expense_data.sort_values(by='Amount', ascending=False).head(5)

print("Top 5 Highest Expenses:")
print(top_expenses[['Transaction_Date', 'Category', 'Amount']])

# -----------------------------
# 9. Transaction Count by Category (All)
# -----------------------------

transaction_count = data['Category'].value_counts()

plt.figure(figsize=(8,6))
transaction_count.plot(kind='bar')

plt.title("Transaction Count by Category")
plt.xlabel("Category")
plt.ylabel("Number of Transactions")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# -----------------------------
# 10. Correlation Heatmap (Monthly Income vs Expense)
# -----------------------------

# Create monthly summary
monthly_summary = (
    data.groupby(['Month', 'Transaction_Type'])['Amount']
    .sum()
    .unstack(fill_value=0)
)

plt.figure(figsize=(6,4))
sns.heatmap(monthly_summary.corr(), annot=True, cmap='coolwarm')

plt.title("Correlation Heatmap (Income vs Expense)")

plt.tight_layout()
plt.show()