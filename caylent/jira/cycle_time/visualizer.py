import numpy as np
import matplotlib.pyplot as plt

def visualize(df, output_path, showPlot):
    plt.figure(figsize=(10, 6))
    counts, bins, patches = plt.hist(df['cycle_time'], bins=20, color='skyblue', edgecolor='black')
    plt.xlabel('Cycle Time (Days)')
    plt.ylabel('Number of Issues')
    plt.title('Cycle Time Distribution')
    
    # Annotate bars with counts
    for count, bin_edge in zip(counts, bins):
        if count > 0:
            plt.text(bin_edge + (bins[1] - bins[0]) / 2, count, f'{int(count)}', ha='center', va='bottom')

    # Set custom x-axis ticks
    plt.xticks(np.arange(0, df['cycle_time'].max() + 1, step=5))  # Adjust step as needed

    plt.tight_layout()
    plt.savefig(output_path)

    if showPlot:
        plt.show()  