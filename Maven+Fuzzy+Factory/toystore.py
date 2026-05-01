import pandas as pd
from sklearn.linear_model import LinearRegression

orders = pd.read_csv("orders.csv")
products = pd.read_csv("products.csv")
refunds = pd.read_csv("order_item_refunds.csv")
pageviews = pd.read_csv("website_pageviews.csv")
sessions = pd.read_csv("website_sessions.csv")
dictionary = pd.read_csv("maven_fuzzy_factory_data_dictionary.csv")
orderitems = pd.read_csv("order_items.csv")

print(orders.shape)
print(products.shape)
print(refunds.shape)
print(pageviews.shape)
print(sessions.shape)
print(dictionary.shape)
print(orderitems.shape)

print(orders.head())
print(orders.dtypes)
print(orders.isnull().sum())

import matplotlib.pyplot as plt

orders['created_at'] = pd.to_datetime(orders['created_at'])
orders['month'] = orders['created_at'].dt.to_period('M')

monthly_revenue = orders.groupby('month')['price_usd'].sum()
monthly_revenue.plot(kind='line', title='Monthly Revenue')
plt.ylabel('Revenue(USD)')
plt.tight_layout()
plt.savefig('monthly_revenue.png')
print("Chart Saved")



product_revenue = orderitems.groupby('product_id')['price_usd'].sum()

plt.figure()
plt.bar( product_revenue.index.astype(str), product_revenue.values)
plt.title('Revenue by Product')
plt.ylabel('Revenue(USD)')
plt.tight_layout()
plt.savefig('product_revenue.png')
print('Product Chart Saved')


refunds_counts = refunds.groupby('order_id')['refund_amount_usd'].sum()
print(refunds_counts.describe())

product_refunds = refunds.groupby('order_item_id')['refund_amount_usd'].sum()
plt.figure()
plt.bar(product_refunds.index.astype(str), product_refunds.values)
plt.title('Refunds by Order Item')
plt.ylabel('Refund Amount (USD)')
plt.tight_layout()
plt.savefig('refunds.png')
print('Refunds Chart Saved')

merged = refunds.merge(orderitems[['order_item_id', 'product_id', 'price_usd']], on='order_item_id')

product_refunds = merged.groupby('product_id')['refund_amount_usd'].sum()
plt.figure()
plt.bar(product_refunds.index.astype(str), product_refunds.values)
plt.title('Total Refunds By Product')
plt.ylabel('Refund Amount (USD)')
plt.tight_layout()
plt.savefig('refunds_by_product.png')
print('Refunds Chart Saved')


channel_orders = sessions.merge(orders[['website_session_id', 'price_usd']], on='website_session_id')

channel_revenue = channel_orders.groupby('utm_source')['price_usd'].sum()

plt.figure() 
plt.bar(channel_revenue.index.astype(str), channel_revenue.values)
plt.title('Revenue by Marketing Channel')
plt.ylabel('Revenue (USD)')
plt.tight_layout()
plt.savefig('channel_revenue.png')
print("Done")

orders['profit'] = orders['price_usd'] - orders['cogs_usd']

total_revenue = orders['price_usd'].sum()
total_cost = orders['cogs_usd'].sum()
total_profit = orders['profit'].sum()
margin = (total_profit / total_revenue * 100).round(2)

print("Total Revenue: $", round(total_revenue, 2))
print("Total Cost: $", round(total_cost, 2))
print("Total Profit: $", round(total_profit, 2))
print("Profit Margin:", margin, "%")

monthly_profit = orders.groupby('month')['profit'].sum()

plt.figure()
monthly_profit.index = monthly_profit.index.astype(str)
plt.plot(monthly_profit.index, monthly_profit.values)
plt.title('Monthly Profit Over Time')
plt.ylabel('Profit(USD)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('monthly_profit.png')
print('Saved')



