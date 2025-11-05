# sales_analysis.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from matplotlib.backends.backend_pdf import PdfPages

# ---------------------------------------------------------------------
# Step 1: Load Data
# ---------------------------------------------------------------------
# Replace this with your actual dataset if available
data = {
    "OrderDate": pd.date_range(start="2023-01-01", periods=100, freq="D"),
    "Region": ["North", "South", "East", "West"] * 25,
    "Product": ["Laptop", "Headphones", "Smartphone", "Camera", "Tablet"] * 20,
    "Quantity": [5, 3, 2, 4, 6] * 20,
    "UnitPrice": [800, 50, 500, 300, 200] * 20,
}

df = pd.DataFrame(data)

# Add calculated columns
df["Revenue"] = df["Quantity"] * df["UnitPrice"]
df["Month"] = df["OrderDate"].dt.to_period("M")

# ---------------------------------------------------------------------
# Step 2: Compute KPIs
# ---------------------------------------------------------------------
total_revenue = df["Revenue"].sum()
average_order_value = df["Revenue"].mean()
region_sales = df.groupby("Region")["Revenue"].sum()
top_region = region_sales.idxmax()
top_region_value = region_sales.max()

kpi_summary = pd.DataFrame({
    "KPI": ["Total Revenue", "Average Order Value", "Top Region"],
    "Value": [
        f"${total_revenue:,.2f}",
        f"${average_order_value:,.2f}",
        f"{top_region} (${top_region_value:,.2f})"
    ]
})

# ---------------------------------------------------------------------
# Step 3: Business Insights
# ---------------------------------------------------------------------
top_products = df.groupby("Product")["Revenue"].sum().sort_values(ascending=False).head(5)
monthly_revenue = df.groupby("Month")["Revenue"].sum()
region_revenue = df.groupby("Region")["Revenue"].sum()

# ---------------------------------------------------------------------
# Step 4: Print Console Output
# ---------------------------------------------------------------------
print("\n================ SALES ANALYSIS REPORT ================\n")

print("📊 KEY PERFORMANCE INDICATORS:")
print(kpi_summary.to_string(index=False))

print("\n🏆 TOP 5 PRODUCTS BY REVENUE:")
print(top_products.reset_index().rename(columns={"index": "Product", "Revenue": "Revenue ($)"}).to_string(index=False))

print("\n📈 MONTHLY REVENUE TREND:")
print(monthly_revenue.reset_index().rename(columns={"Month": "Month", "Revenue": "Revenue ($)"}).to_string(index=False))

print("\n🌎 REVENUE BY REGION:")
print(region_revenue.reset_index().rename(columns={"Region": "Region", "Revenue": "Revenue ($)"}).to_string(index=False))

# ---------------------------------------------------------------------
# Step 5: Visualization + PDF Export
# ---------------------------------------------------------------------
sns.set_theme(style="whitegrid")

with PdfPages("sales_summary.pdf") as pdf:
    # Top Products
    plt.figure(figsize=(8, 5))
    sns.barplot(x=top_products.index, y=top_products.values, palette="Blues_d")
    plt.title("Top 5 Products by Revenue", fontsize=14)
    plt.ylabel("Revenue ($)")
    plt.xlabel("Product")
    plt.tight_layout()
    pdf.savefig()
    plt.show()

    # Monthly Trend
    plt.figure(figsize=(8, 5))
    monthly_revenue.plot(marker="o", color="darkgreen")
    plt.title("Monthly Revenue Trend", fontsize=14)
    plt.ylabel("Revenue ($)")
    plt.xlabel("Month")
    plt.grid(True)
    plt.tight_layout()
    pdf.savefig()
    plt.show()

    # Region Revenue
    plt.figure(figsize=(8, 5))
    sns.barplot(x=region_revenue.index, y=region_revenue.values, palette="magma")
    plt.title("Revenue by Region", fontsize=14)
    plt.ylabel("Revenue ($)")
    plt.xlabel("Region")
    plt.tight_layout()
    pdf.savefig()
    plt.show()

    # Summary Table
    fig, ax = plt.subplots(figsize=(8, 4))
    plt.axis("off")
    table = ax.table(cellText=kpi_summary.values,
                     colLabels=kpi_summary.columns,
                     cellLoc='center',
                     loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1.2, 1.5)
    plt.title("Sales Performance KPIs", fontsize=14, pad=20)
    pdf.savefig()
    plt.close()

print("\n✅ Sales Analysis Complete! PDF summary saved as 'sales_summary.pdf'\n")
