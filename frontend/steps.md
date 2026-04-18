## 🟢 STEP 1 (FIRST REAL CODE) — Product Aggregates

📁 analytics/demand_analysis.py

❗ Why start here?

Almost everything depends on this

Products tab, recommendations, top products, demand badges

If this is wrong → whole app feels wrong

What to implement FIRST:

A single function:

compute_product_summary(df)

Output columns:
product
category
totalQuantity
totalRevenue
salesCount
avgQuantityPerSale


💡 Tip:

Don’t think about demandLevel yet

Just group by product

✔ When this works → you’ve unlocked 50% of analytics.

## 🟢 STEP 2 — Category Aggregates

📁 analytics/demand_analysis.py

Now add:

compute_category_summary(df)

Output:
category
revenue
quantity

Must be:

Sorted by revenue DESC

Category default = "Uncategorized"

This feeds Overview pie + bar charts.

## 🟢 STEP 3 — Top Products (Derived, Easy Win)

Still in demand_analysis.py:

compute_top_products(df, top_n=5)


This is literally:

reuse product summary

sort by revenue

slice top N

⚠️ Don’t overthink this.

## 🟢 STEP 4 — Daily Time-Series (Trends Backbone)

📁 analytics/trend_analysis.py

Now move to time logic.

Implement:

compute_daily_trends(df)

Output:
date
revenue
quantity
transactions

Rules:

date must be string YYYY-MM-DD

sorted ASC

transactions = count rows per date

Once this works:
✔ Trends tab becomes possible
✔ KPI growth logic works

## 🟢 STEP 5 — Category Time-Series

📁 analytics/trend_analysis.py

This is slightly tricky but powerful.

Implement:

compute_category_time_series(df)

Output:
{
  "categories": [...],
  "data": [
    { "date": "...", "Beverages": 100, "Bakery": 50 }
  ]
}


💡 Build this by:

Get unique dates

Get unique categories

Fill missing combinations with 0

Take your time here. This is the hardest part.

## 🟢 STEP 6 — Top Product Time-Series

📁 analytics/trend_analysis.py

Last heavy logic:

compute_top_product_time_series(df, top_n=5)


Steps:

Find top products (reuse earlier logic)

Build date × product grid

Fill missing values with 0

Once done → Trends tab is complete.

## 🟢 STEP 7 — KPIs (Fast & Easy)

📁 analytics/kpi_calculator.py

End with simple wins:

total_revenue(df)
total_quantity(df)
unique_products(df)
avg_order_value(df)


These are 5–10 lines each.
Don’t start with these — finish with them.

## ⏱️ RECOMMENDED TIME PLAN (REALISTIC)
Step	Time
Product aggregates	1–1.5 hrs
Category + Top products	30–45 min
Daily trends	45 min
Category time-series	1–1.5 hrs
Top-product time-series	45 min
KPIs	30 min