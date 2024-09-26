import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.graph_objects as go
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def visualize_table(data, output_location, title, showPlot):
    try:
        fig = go.Figure(data=[go.Table(
            header=dict(values=list(data.columns),  # Use the column names as headers
                        fill_color='paleturquoise', 
                        align='left'),
            cells=dict(values=[data[col] for col in data.columns],  # Pass each column's data to the table
                    fill_color='lavender',
                    align='left'))
        ])

        # Add a title to the Plotly table
        fig.update_layout(
            title=title,  # Set the title here
            title_x=0.5  # Center the title (optional)
        )

        # fig.write_image(output_location)
        
        # if showPlot:
        fig.show()

    except Exception as e:
        logging.error("Error creating or saving the table: %s", e)
        raise

def visualize(dataframe):
    ##### BAR #######

    # Set up the plot
    plt.figure(figsize=(10, 6))

    # Create the bar plot, where each bar is an individual with their readiness score in different pillars
    for pillar in dataframe['Pillar'].unique():
        pillar_data = dataframe[dataframe['Pillar'] == pillar]
        plt.bar(pillar_data['Full Name'], pillar_data['Weighted Rating'], label=pillar)

    # Customize the plot
    plt.xticks(rotation=90)
    plt.xlabel('Full Name')
    plt.ylabel('Weighted Readiness Score')
    plt.title('Cross-Training Readiness by Pillar')
    plt.legend(title="Pillars", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    # Show the plot
    plt.show()


    #### STACKED BAR ######

    # Pivot data to have one row per 'Full Name' and separate columns for each 'Pillar'
    pivot_data = dataframe.pivot(index='Full Name', columns='Pillar', values='Weighted Rating').fillna(0)

    # Set up the stacked bar plot
    pivot_data.plot(kind='bar', stacked=True, figsize=(10, 6))

    # Customize the plot
    plt.xticks(rotation=90)
    plt.xlabel('Full Name')
    plt.ylabel('Total Weighted Readiness Score')
    plt.title('Stacked Readiness Scores Across Pillars')
    plt.legend(title="Pillars", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    # Show the plot
    plt.show()


    #### HEATMAP ######
    # Pivot data to have one row per 'Full Name' and separate columns for each 'Pillar'
    heatmap_data = dataframe.pivot(index='Full Name', columns='Pillar', values='Weighted Rating').fillna(0)

    # Set up the heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, annot=True, cmap='Blues', linewidths=0.5)

    # Customize the plot
    plt.title('Readiness Heatmap by Pillar')
    plt.xlabel('Pillar')
    plt.ylabel('Full Name')
    plt.xticks(rotation=90)
    plt.tight_layout()

    # Show the plot
    plt.show()


    #### SCATTER PLOT ######
    # Set up the scatter plot
    plt.figure(figsize=(10, 6))
    for pillar in dataframe['Pillar'].unique():
        pillar_data = dataframe[dataframe['Pillar'] == pillar]
        plt.scatter(pillar_data['Full Name'], pillar_data['Weighted Rating'], label=pillar)

    # Customize the plot
    plt.xticks(rotation=90)
    plt.xlabel('Full Name')
    plt.ylabel('Weighted Readiness Score')
    plt.title('Cross-Training Readiness Scatter by Pillar')
    plt.legend(title="Pillars", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    # Show the plot
    plt.show()


    ##### PIVOT TABLE ######
    # Create a pivot table with Full Name as the rows and Pillar as the columns
    pivot_table = dataframe.pivot(index='Full Name', columns='Pillar', values='Weighted Rating')

    # Fill any NaN values with 0 (if there are missing values in some columns for some individuals)
    pivot_table = pivot_table.fillna(0)
    print(pivot_table.head())
