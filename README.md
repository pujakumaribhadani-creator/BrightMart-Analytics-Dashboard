# 📊 BrightMart Analytics Dashboard

An interactive retail analytics dashboard built using **Python, Pandas, Streamlit, and Plotly**.

The project combines customer, product, order, and order-item data to analyze sales performance, customer behavior, and regional revenue.

## 🌐 Live Demo

[View Live Dashboard](https://brightmart-analytics-dashboard-dktqrvffb9kqjeph2fwrmn.streamlit.app/)

## 🚀 Key Features

- Multi-table data merging and data preparation using Pandas
- Interactive filters for **Region, Category, Segment, and Date**
- KPI tracking:
  - Total Revenue
  - Total Orders
  - Average Order Value
  - Unique Customers
- Interactive visualizations:
  - Monthly Revenue Trend
  - Revenue by Category
  - Top 10 Customers by Revenue
  - Revenue by Region
- Customer Deep Dive with Lifetime Value, Orders, Products Purchased, and Order History
- Filtered data export as CSV

## 🛠️ Tech Stack

**Python | Pandas | Streamlit | Plotly**

## 💡 Key Insights

- Furniture generated the highest revenue among categories.
- South was the highest revenue-generating region.
- Home Office had the highest Average Order Value among customer segments.
- Revenue showed noticeable monthly fluctuations with a peak around January 2025.

## 📁 Dataset

The dashboard uses four related CSV files:

`customers.csv` | `products.csv` | `orders.csv` | `order_items.csv`

## ▶️ Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
