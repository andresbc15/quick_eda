"""Quick smoke test: import the package and run overview() on a sample frame."""

import pandas as pd

from quick_eda import summarize, bar

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

# Horizontal bar chart from a DataFrame, largest group highlighted.
offenses = pd.DataFrame(
    {
        "offense": [
            "Drug Offenses", "Immigration", "Sex Offenses", "Weapons",
            "Fraud", "Burglary", "Robbery", "Homicide", "Other",
        ],
        "count": [75, 21, 12, 11, 10, 8, 7, 5, 3],
    }
)
fig, ax = bar(offenses, "offense", "count", highlight_color="#a23b3b")
fig.savefig("bar_demo.png", dpi=150, bbox_inches="tight")
print("saved bar_demo.png")

