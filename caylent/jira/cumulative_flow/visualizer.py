import matplotlib.pyplot as plt
import pandas as pd

def visualize(df, output_path, showPlot):
    # Ensure columns are converted to DatetimeIndex
    df.columns = df.columns.to_timestamp()

    # Transpose the DataFrame
    df = df.transpose()

    plt.figure(figsize=(14, 8))
    plt.stackplot(df.index.astype(str), df.T, labels=df.columns, alpha=0.8)
    plt.xlabel('Date')
    plt.ylabel('Number of Issues')
    plt.title('Cumulative Flow Diagram')
    plt.legend(loc='upper left')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_path)

    if showPlot:
        plt.show()  