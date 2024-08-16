import matplotlib.pyplot as plt
import seaborn as sns
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_heatmap(pivot_percentages, show_plot, output_path):
    try:
        # Create the heat map
        plt.figure(figsize=(30, 10))
        sns.heatmap(pivot_percentages, annot=True, fmt=".1f", cmap='coolwarm', cbar_kws={'label': 'Percentage of Engineers'})
        plt.title('Distribution of Skill Levels Across Core Skills (Percentage of Engineers)')
        plt.xlabel('Skill')
        plt.ylabel('Skill Level')

        # Adjust the bottom margin
        plt.subplots_adjust(bottom=0.35)  # Increase the bottom margin as needed

        # Save the heatmap as an image file
        plt.savefig(output_path, bbox_inches='tight')
        logging.info("Heatmap saved to %s", output_path)

        # Show the heatmap
        if show_plot:
            plt.show()
    except Exception as e:
        logging.error("Error creating or saving the heatmap: %s", e)
        raise