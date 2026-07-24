"""Simple, readable helpers for exploratory data analysis.

Inspired by *Storytelling with Data* (C. N. Knaflic): show only what earns
its place, and make it easy to scan. ``summarize`` is an intuitive take on
``DataFrame.info()``; ``bar`` draws a decluttered horizontal bar chart.
"""

import matplotlib.pyplot as plt

# A calm, neutral grey. Used for text summaries' backdrop bars and, in the
# chart, for every bar until you choose to highlight one.
GREY = "#8c8c8c"


def count_types(values):
    """Count how many values of each Python type are in a column.

    Returns a dict like ``{"int": 3, "str": 2}``. We build it with a plain
    loop so it's easy to follow — no extra libraries needed.
    """
    counts = {}
    for value in values:
        type_name = type(value).__name__ # provides the name as text
        counts[type_name] = counts.get(type_name, 0) + 1
    return counts


def summarize(df):
    """Print a clear, human-readable summary of a pandas ``DataFrame``.

    Reads top to bottom: the shape first, then one line per column showing
    its type, how much is missing, and a note for anything worth a second
    look. Clean columns stay quiet so problems stand out.
    """
    n_rows, n_cols = df.shape

    # Build one row of info per column.
    rows = []
    for name in df.columns:
        column = df[name]
        missing = n_rows - int(column.notna().sum())

        # Show missing as a count and a percentage; a dash means none.
        if missing == 0:
            missing_text = "-"
        else:
            percent = round(missing / n_rows * 100)
            missing_text = f"{missing} ({percent}%)"

        # Only object columns can secretly hold more than one type.
        note = ""
        if column.dtype == "object":
            types = count_types(column.dropna())
            if len(types) > 1:
                pieces = [f"{t} ({n})" for t, n in types.items()]
                note = "mixed types: " + ", ".join(pieces)

        rows.append((str(name), str(column.dtype), missing_text, note))

    # Work out how wide each column must be so everything lines up.
    name_width = len("Column")
    type_width = len("Type")
    miss_width = len("Missing")
    for name, dtype, missing_text, note in rows:
        name_width = max(name_width, len(name))
        type_width = max(type_width, len(dtype))
        miss_width = max(miss_width, len(missing_text))

    # Print the summary.
    print()
    print(f"{n_rows} rows x {n_cols} columns")
    print()
    print(f"{'Column':<{name_width}}  {'Type':<{type_width}}  {'Missing':<{miss_width}}  Note")
    for name, dtype, missing_text, note in rows:
        print(f"{name:<{name_width}}  {dtype:<{type_width}}  {missing_text:<{miss_width}}  {note}".rstrip())
    print()


def bar(df, category, value=None, highlight_color=GREY, title=None):
    """Draw a horizontal bar chart from a DataFrame, biggest bar on top.

    ``category`` is the column to use for the bar labels. If ``value`` is
    given, that column sets the bar lengths; if it's left out, the bars show
    how often each category appears (a simple count).

    Every bar is grey. Pass ``highlight_color`` (e.g. ``"#a23b3b"``) to make
    the largest bar stand out; leave it as the default grey to keep the
    chart neutral. Returns the matplotlib ``(fig, ax)`` so you can save it.
    """
    if value is None:
        # No value column: count how many times each category shows up.
        counts = df[category].value_counts()
        labels = list(counts.index)
        values = list(counts.values)
    else:
        labels = list(df[category])
        values = list(df[value])

    # Sort smallest-to-largest so the biggest bar ends up on top.
    order = sorted(range(len(values)), key=lambda i: values[i])
    labels = [labels[i] for i in order]
    values = [values[i] for i in order]

    # Grey everywhere, except the largest bar (the last one after sorting).
    colors = [GREY] * len(values)
    if values:
        colors[-1] = highlight_color

    # Taller figures for more bars, so labels never crowd each other.
    fig, ax = plt.subplots(figsize=(8, 0.5 * len(values) + 1))
    ax.barh(labels, values, color=colors)

    # Declutter: drop the frame and gridlines, move the scale to the top.
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.xaxis.tick_top()
    ax.tick_params(length=0)  # remove the category-side tick marks
    ax.tick_params(axis="x", colors=GREY, length=5)  # short grey ticks + numbers

    if title:
        ax.set_title(title, loc="left")

    fig.tight_layout()
    return fig, ax
