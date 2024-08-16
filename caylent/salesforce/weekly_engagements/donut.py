import plotly.graph_objects as go
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_donut(labels, values, output_location, showPlot):
    
    try:
        # Create the donut chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4)])

        # Update layout for the donut chart
        fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(line=dict(color='#000000', width=2)))

        fig.write_image(output_location)

        if showPlot:
            fig.show()

    except Exception as e:
        logging.error("Error creating or saving the table: %s", e)
        raise