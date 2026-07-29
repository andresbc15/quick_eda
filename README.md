# quick_eda

Exploratory data analysis helpers to quickly summarize and visualize your data. Three small functions, limited dependencies (pandas + matplotlib).

## Install

```bash
pip install quick-eda-andresbc15
```

## Usage

```python
import pandas as pd
from quick_eda_andresbc15 import summarize, bar_plot, line_plot

df = pd.DataFrame({
    "area": ["Construction", "Retail", "Transportation", "Consulting"],
    "amount": [710000, 190000, 620000, 630000],
})

# 1. A friendlier df.info(): shape, dtypes, missing counts, and a note when
#    a column secretly mixes Python types.
summarize(df)

# 2. Horizontal bar chart that is sorted in Descending order.
fig, ax = bar_plot(df, 
            category_col="area", 
            value="amount", 
            indeces_lst=[0], 
            prefix="$",
            header="Investment by area of impact",
            subheader="Dollars")
fig.savefig("bar.png", bbox_inches="tight")

df2 = pd.DataFrame({
    "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
    "revenue": [120, 135, 130, 160, 175, 168, 210],
})

# 3. A line chart with chosen points highlighted.
fig, ax = line_plot(df2, 
                x_col="month", 
                y_col="revenue", indeces_lst=[0, 3], units="USD")
fig.savefig("line.png", bbox_inches="tight")
```

## License

MIT — see [LICENSE](LICENSE).
