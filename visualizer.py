import matplotlib.pyplot as plt
import seaborn as sns

def visualize(df, chart_type='bar', x=None, y=None):
    if x not in df.columns or y not in df.columns:
        print("Invalid columns for visualization.")
        return

    plt.figure(figsize=(10, 6))
    if chart_type == 'bar':
        sns.barplot(data=df, x=x, y=y)
    elif chart_type == 'line':
        sns.lineplot(data=df, x=x, y=y)
    elif chart_type == 'scatter':
        sns.scatterplot(data=df, x=x, y=y)
    else:
        print("Unsupported chart type.")
        return

    plt.title(f"{chart_type.capitalize()} chart of {y} vs {x}")
    plt.show()

