"""Simple, readable helpers for exploratory data analysis.

Inspired by *Storytelling with Data* (C. N. Knaflic): show only what earns
its place, and make it easy to scan. ``summarize`` is an intuitive take on
``DataFrame.info()``; ``bar`` draws a decluttered horizontal bar chart.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# Use Arial everywhere for a clean, familiar look.
plt.rcParams["font.family"] = "Arial"

# A calm, neutral grey. Used for text summaries' backdrop bars and, in the
# chart, for every bar until you choose to highlight one.
GREY = "#8c8c8c"


def add_titles(ax, header, subheader):
    """Place a bold header and a grey subheader just above the plot.

    Positions are in axes coordinates (0 = left/bottom, 1 = right/top), so
    the titles sit above the chart without any figure-size math.
    """
    if header:
        ax.text(0, 1.10, header, transform=ax.transAxes,
                fontsize=14, fontweight="bold", color="#333333")
    if subheader:
        ax.text(0, 1.03, subheader, transform=ax.transAxes,
                fontsize=11, color=GREY)


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


def bar(df, category_col, value, indeces_lst=None, highlight_color="#2e5a87",
        prefix="", suffix="", header="", subheader=""):
    """Draw a decluttered horizontal bar chart, biggest bar on top.

    Bars are ordered greatest to least with the value printed at the end of
    each bar, so there is no need for an x-axis or gridlines.

    Args:
        df (pandas.DataFrame): Source data.
        category_col (str): Column holding the bar labels.
        value (str): Column holding the numeric bar lengths.
        indeces_lst (list[int], optional): Row numbers (into ``df``) to paint
            in ``highlight_color``; all other bars stay grey. Defaults to the
            single biggest bar.
        highlight_color (str): Colour for the highlighted bars.
        prefix (str): Text placed before each value label, e.g. "$".
        suffix (str): Text placed after each value label, e.g. "%".
        header (str): Bold title shown above the chart.
        subheader (str): Grey subtitle shown under the header.

    Returns:
        tuple: The matplotlib ``(fig, ax)`` so you can restyle further.
    """
    labels = list(df[category_col])
    values = list(df[value])

    # Sort smallest-to-largest so the biggest bars end up on top. ``order[p]``
    # is the original row number now sitting at plot position ``p``.
    order = sorted(range(len(values)), key=lambda i: values[i])
    labels = [labels[i] for i in order]
    values = [values[i] for i in order]
    n = len(values)

    # Default: highlight the biggest bar (the last one after sorting).
    if indeces_lst is None:
        indeces_lst = [order[-1]]

    height = 0.55  # thickness of each bar, from 0 (none) to 1 (bars touching)

    fig, ax = plt.subplots(figsize=(8, 0.5 * n + 1))
    xmax = max(values) * 1.18  # leave room past the bars for the value labels

    # Corner rounding is measured in x-units, so tie it to the chart width
    # (not a fixed number) to look the same whether amounts are 700 or 700k.
    # ``aspect`` corrects for the x/y scale so both corners round evenly.
    rounding = xmax * 0.01
    aspect = (n / (0.5 * n + 1)) / (xmax / 8)

    for pos, v in enumerate(values):
        # Grey unless this bar's original row was chosen for the accent colour.
        bar_color = highlight_color if order[pos] in indeces_lst else GREY
        ax.add_patch(FancyBboxPatch(
            (-rounding, pos - height / 2), v + rounding, height,
            boxstyle=f"round,pad=0,rounding_size={rounding}",
            mutation_aspect=aspect, linewidth=0, facecolor=bar_color))
        ax.text(v + xmax * 0.015, pos, f"{prefix}{v:,.0f}{suffix}",
                va="center", fontweight="bold", color=bar_color)

    ax.set_yticks(range(n))
    ax.set_yticklabels(labels)
    ax.set_xlim(0, xmax)
    ax.set_ylim(-0.7, n - 0.3)

    # Declutter to the extreme: no frame, no gridlines, no x-axis at all.
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.xaxis.set_visible(False)
    ax.tick_params(length=0)  # remove the category-side tick marks
    add_titles(ax, header, subheader)
    fig.tight_layout()
    return fig, ax


def line(df, x_col, y_col, indeces_lst=None, color="#2e5a87",
         units="", header="", subheader=""):
    """Draw a decluttered line chart, with optional highlighted points.

    Plots ``y_col`` against ``x_col`` as a single line. Any points you pick
    are marked with a dot and labelled with their value, to draw the eye to
    the moments that matter.

    Args:
        df (pandas.DataFrame): Source data.
        x_col (str): Column for the x-axis (e.g. dates or steps).
        y_col (str): Column holding the numeric y values.
        indeces_lst (list[int], optional): Row numbers (into ``df``) to mark
            with a dot and value label. Defaults to no dots.
        color (str): Colour of the line and its dots.
        units (str): Label for the y-axis, e.g. "Dollars".
        header (str): Bold title shown above the chart.
        subheader (str): Grey subtitle shown under the header.

    Returns:
        tuple: The matplotlib ``(fig, ax)`` so you can restyle further.
    """
    x = list(df[x_col])
    y = list(df[y_col])

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x, y, color=color, linewidth=2)

    # Mark the chosen points with a dot and print their value above it.
    for i in indeces_lst or []:
        ax.scatter(x[i], y[i], color=color, s=45, zorder=3)
        ax.annotate(f"{y[i]:,.0f}", (x[i], y[i]), textcoords="offset points",
                    xytext=(0, 9), ha="center", fontweight="bold", color=color)

    # Declutter: keep the left and bottom axes (with ticks) so the line can
    # be read against a scale, but drop the top and right frame.
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(GREY)
    ax.spines["bottom"].set_color(GREY)
    ax.tick_params(colors=GREY, length=5)
    ax.set_ylabel(units, color=GREY)

    add_titles(ax, header, subheader)
    fig.tight_layout()
    return fig, ax
