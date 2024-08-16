import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from config.config import WIP_ISSUE_STATUSES_TO_TRACK

# Plot the WIP chart
def visualize_line_chart(wip_df, output_path, showPlot):
    plt.figure(figsize=(12, 6))

    for status in WIP_ISSUE_STATUSES_TO_TRACK:
        plt.plot(wip_df['status_change_date'], wip_df[status], label=status)

        # Customize X-Axis labels
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))  # Labels every 5 days
        plt.gca().xaxis.set_minor_locator(mdates.DayLocator())  # Minor ticks for every day
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)

    # Add labels and title
    plt.xlabel('Date')
    plt.ylabel('Number of Issues in Status')
    plt.title('Work In Progress (WIP) Over Time')
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Show the plot
    plt.tight_layout()
    plt.savefig(output_path)

    if showPlot:
        plt.show()  

# Plot the WIP as a stacked bar chart
def visualize_bar_chart(wip_df, output_path, showPlot):
    plt.figure(figsize=(12, 6))
    bottom = None
    for status in WIP_ISSUE_STATUSES_TO_TRACK:
        if bottom is None:
            bottom = wip_df[status]
            plt.bar(wip_df.index, wip_df[status], label=status)
        else:
            plt.bar(wip_df.index, wip_df[status], bottom=bottom, label=status)
            bottom = bottom + wip_df[status]

    # Calculate the total number of issues across all statuses
    total_issues = wip_df[WIP_ISSUE_STATUSES_TO_TRACK].sum(axis=1)

    # Calculate the average
    avg_issues = total_issues.mean()

    # Plot the average line
    plt.axhline(y=avg_issues, color='green', linestyle='--', linewidth=1, label='Average')

    # Calculate the running average
    running_avg = total_issues.expanding().mean()

    # Plot the running average line
    plt.plot(wip_df.index, running_avg, color='black', linestyle='--', linewidth=1, label='Running Average')

    # Customize X-Axis labels
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))  # Labels every 5 days
    plt.gca().xaxis.set_minor_locator(mdates.DayLocator())  # Minor ticks for every day
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)

    # Set the y-axis limit to provide more space for the bars
    plt.ylim(0, total_issues.max() + 1)

    # Add labels and title
    plt.xlabel('Date')
    plt.ylabel('Number of Issues in Status')
    plt.title('Work In Progress (WIP) Over Time')
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Show the plot
    plt.tight_layout()
    plt.savefig(output_path)
    
    if showPlot:
        plt.show()  