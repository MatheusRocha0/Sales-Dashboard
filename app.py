import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.title("")

path = "data.csv"
df = pd.read_csv(path)
df.head()
 
df.drop_duplicates(inplace = True)
 
df["Date"] = pd.to_datetime(df.Date)
df["day"] = df.Date.dt.day
 
sales_by_day = df.groupby("day")["Unit price"].sum()
total_gross = df["gross income"].sum()
total_sales = df["Unit price"].sum()
total_units = df["Total"].sum()
sales_by_city = df.groupby("City")["Unit price"].sum()
sales_by_line = df.groupby("Product line")["Unit price"].sum()
sales_by_cust = df.groupby("Customer type")["Unit price"].sum()
sales_by_gender = df.groupby("Gender")["Unit price"].sum()
 
 
fig = make_subplots(
rows = 3, cols = 4,
specs = [
[{"type": "indicator"}, {"type": "indicator", "colspan": 2}, None, {"type": "indicator"}],
[{"type": "scatter", "colspan": 4}, None, None, None],
[{"type": "bar"}, {"type": "bar"}, {"type": "bar"}, {"type": "pie"}]
],
subplot_titles = 
[
"", "", "",
"Sales By Day Of Month",
"Sales By City", "Sales By Line", "Sales By Cust. Type", "Sales By Gender"
]
)
 
# indicators
fig.add_trace(go.Indicator(mode = "number", title = "Total Gross Income", value = total_gross), row = 1, col = 1)
fig.add_trace(go.Indicator(mode = "number", title = "Total Sales", value = total_sales), row = 1, col = 2)   
fig.add_trace(go.Indicator(mode = "number", title = "Total Units", value = total_units), row = 1, col = 4)
 
# time series
fig.add_trace(go.Scatter(x = sales_by_day.index, y = sales_by_day.values, marker_color = "springgreen", name = "Sales By Day of Month"), row = 2, col = 1)
 
# bottom
fig.add_trace(go.Bar(x = sales_by_city.index, y = sales_by_city.values, marker_color = "mediumspringgreen", name = "Sales By City"), row = 3, col = 1)
fig.add_trace(go.Bar(x = sales_by_line.index, y = sales_by_line.values, marker_color = "mediumspringgreen", name = "Sales By Product Line"), row = 3, col = 2)
fig.add_trace(go.Bar(x = sales_by_cust.index, y = sales_by_cust.values, marker_color = "mediumspringgreen", name = "Sales By Customer Type"), row = 3, col = 3)
fig.add_trace(go.Pie(values = sales_by_gender.values, labels = sales_by_gender.index, hole = .6, marker_colors = ["lime", "lightgreen"], name = "Sales By Gender"), row = 3, col = 4)
 
fig.update_layout(template = "plotly_dark", title = "Sales Dashboard", width = 800, height = 600, legend_orientation = "v")
fig.show()
