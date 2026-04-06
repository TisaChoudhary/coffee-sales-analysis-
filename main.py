import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Resolve paths from this script's directory so the code works from any CWD.
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "Coffee sales in a vending machine.csv"
if not DATA_PATH.exists():
    DATA_PATH = BASE_DIR.parent / "Data" / "Coffee sales in a vending machine.csv"

VISUALIZATIONS_DIR = BASE_DIR / "Visualizations"
VISUALIZATIONS_DIR.mkdir(parents=True, exist_ok=True)
INTERACTIVE_BACKEND = "agg" not in plt.get_backend().lower()

df = pd.read_csv(DATA_PATH)

def finalize_plot(filename: str) -> None:
    plt.tight_layout()
    plt.savefig(VISUALIZATIONS_DIR / filename)
    plt.show()   # 👈 ALWAYS show graph

df.head() # Quick view of the data

df.info() # Check data types and missing values

df["date"]=pd.to_datetime(df["date"])

df["time"] = pd.to_datetime(df["datetime"]).dt.strftime("%H:%M:%S")
df.drop("datetime",axis=1,inplace=True) # Removing the old column

df.drop_duplicates(inplace=True) # Remove duplicates row

df.head()

# Total Revenue and average spending per transaction
print("The total revenue: {:.1f}".format(df["money"].sum()))
print("The average spending: {:.1f}".format(df["money"].mean()))

# Daily sales chart
daily_sales = df.groupby("date")["money"].sum()
plt.figure(figsize=(12,6))
plt.plot(daily_sales.index, daily_sales.values, color='b')
plt.xlabel("Date")
plt.ylabel("Total sales")
plt.title("Daily sales trend")
plt.xticks(rotation=45)
plt.grid()
finalize_plot("daily_sales_trend.png")

# Best-selling product analysis
counts = df["coffee_name"].value_counts()

# Best Selling Coffee Chart
plt.figure(figsize=(10,5))
sns.barplot(x=counts.index, y=counts.values, hue=counts.index, palette="mako", legend=False)
plt.title("Best-selling product")
finalize_plot("best_selling_coffee.png")

# Total revenue for each type of coffee
df.groupby("coffee_name")["money"].sum().sort_values(ascending=False)

# Revenue chart for each type of coffee.
coffee_revenue = df.groupby("coffee_name")["money"].sum().sort_values(ascending=False)
plt.figure(figsize=(13,6))
sns.barplot(x=coffee_revenue.index, y=coffee_revenue.values, hue=coffee_revenue.index, palette="viridis", legend=False)
plt.title("Revenue per type of coffee")
finalize_plot("revenue_per_coffee.png")

# Payment methods distribution account
df["cash_type"].value_counts()

# pie chart of payment methods
plt.figure(figsize=(6,6))
plt.pie(df["cash_type"].value_counts(),labels=df["cash_type"].value_counts().index,
        autopct='%1.1f%%',startangle=30,pctdistance=0.85)
plt.axis('equal')
plt.title("Distribution of payment methods")
finalize_plot("payment_methods_pie.png")

# Take the top 10 customers by number of purchases
df["card"].value_counts().head(10)

# Chart of repeat customers
top_customers = df["card"].value_counts().head(10)
plt.figure(figsize=(10,5))
sns.barplot(x=top_customers.index, y=top_customers.values, hue=top_customers.index, palette="rocket", legend=False)
plt.xticks(rotation=90)
plt.title("Most frequent customers")
finalize_plot("repeat_customers.png")

# Extract hours from `datetime`
df['hour'] = pd.to_datetime(df['time'], format="%H:%M:%S").dt.hour

# the number of sales per hour
df.groupby("hour").size()

# Peak time chart
plt.figure(figsize=(10,5))
df.groupby("hour").size().plot(marker='o',color='r')
plt.ylabel("sales")
plt.title("Peak sales analysis")
plt.xticks(range(0, 24))
plt.ylim(bottom=0)
plt.grid()
finalize_plot("peak_sales_hours.png")

# Extract days from `date`
df["weekday"]=df["date"].dt.day_name()
# Total sales for each day of the week
df.groupby("weekday")["money"].sum()

# Arrange the days correctly
sales_weekday = df.groupby("weekday")["money"].sum()
days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
sales_weekday = sales_weekday.reindex(days_order)

# Sales chart by days of the week
plt.figure(figsize=(10,5))
sns.barplot(x=sales_weekday.index, y=sales_weekday.values, hue=sales_weekday.index, palette="crest", legend=False)
plt.title("Sales analysis by days of the week")
plt.xticks(rotation=45)
finalize_plot("sales_by_weekday.png")

# Extract months from `date`
df["month"] = df["date"].dt.month
# Monthly sales
df.groupby("month")["money"].sum()

# Sales chart by months
sales_monthly = df.groupby("month")["money"].sum()
plt.figure(figsize=(10,6))
sns.barplot(x=sales_monthly.index, y=sales_monthly.values, hue=sales_monthly.index, palette="Spectral", legend=False)
plt.title("Sales analysis by months")
finalize_plot("sales_by_month.png")

# Classify transactions into morning (before 12 o'clock) or evening
df["Am or Pm"] = df["hour"].apply(lambda x : "Pm" if x>=12 else "Am")
# Sales account for each period
df.groupby("Am or Pm")["money"].sum()

# Sales chart for morning and evening
period = df.groupby("Am or Pm")["money"].sum()
plt.figure(figsize=(7,5))
sns.barplot(x=period.index, y=period.values, hue=period.index, palette="pastel", legend=False)
plt.title("Morning vs. Evening Sales")
finalize_plot("morning_vs_evening_sales.png")
