import matplotlib.pyplot as plt
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_barchart(data, show_plot, output_path):
    try:
        plt.figure(figsize=(10, 6))
        bars = plt.bar(list(data.keys()), list(data.values()), color='skyblue')
        plt.xlabel('Number of Skills Defined')
        plt.ylabel('Team Member Count')
        plt.title('Count of Skills Team Members Have Rated Themselves In')
        plt.xticks(rotation=45)
        
        # Annotate bars with throughput values
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height, f'{int(height)}', ha='center', va='bottom')

        plt.tight_layout()
        plt.savefig(output_path)

        # Show the heatmap
        if show_plot:
            plt.show()
    except Exception as e:
        logging.error("Error creating or saving the bar chart: %s", e)
        raise