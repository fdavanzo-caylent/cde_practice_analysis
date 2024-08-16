import matplotlib.pyplot as plt

def visualize(df, output_path, showPlot):
    df['week'] = df['week'].astype(str)

    plt.figure(figsize=(10, 6))
    bars = plt.bar(df['week'], df['throughput'], color='skyblue')
    plt.xlabel('Week')
    plt.ylabel('Throughput (Issues Closed)')
    plt.title('Weekly Throughput')
    plt.xticks(rotation=45)
    
    # Annotate bars with throughput values
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, f'{int(height)}', ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(output_path)

    if showPlot:
        plt.show()  