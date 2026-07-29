"""Quick smoke test: import the package and run overview() on a sample frame."""
import pandas as pd
from quick_eda_andresbc15 import summarize, bar_plot, line_plot

# A small frame that exercises the interesting cases:
#   - a clean numeric column
#   - a column that secretly mixes types (int + str)
#   - a column with missing values
df = pd.DataFrame(
    {
        "id": [1, 2, 3, 4, 5],
        "name": ["Ana", "Ben", "Cy", "Dee", "Eli"],
        "age": [34, "unknown", 29, 41, "n/a"],  # mixed int / str
        "score": [88.5, 92.0, None, 75.5, None],  # has missing
    }
)

summarize(df)

# Horizontal bar chart with the full storytelling treatment.
grants = pd.DataFrame(
    {
        "area": [
            "Construction", "Wholesale Distribution", "Consulting Services",
            "Transportation", "Medical Manufacturing", "Accounting Firms", "Retail",
        ],
        "amount": [710, 670, 630, 620, 360, 340, 190],
    }
)
fig, ax = bar_plot(
    grants, "area", "amount",
    indeces_lst=[0, 1],  # row numbers into `grants` to accent; rest stay grey
    prefix="$",
    header="Investment by area of impact",
    subheader="Dollars in 000s",
)
fig.savefig("bar_demo.png", dpi=150, bbox_inches="tight")
print("saved bar_demo.png")

# Line chart with a couple of highlighted points.
trend = pd.DataFrame(
    {
        "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
        "revenue": [120, 135, 130, 160, 175, 168, 210],
    }
)
fig, ax = line_plot(
    trend, "month", "revenue",
    indeces_lst=[0, 6],  # mark the first and last points with a dot + value
    header="Revenue climbed through the first half",
    subheader="IN MILLIONS (USD)",
)
fig.savefig("line_demo.png", dpi=150, bbox_inches="tight")
print("saved line_demo.png")

