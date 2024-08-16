import plotly.graph_objects as go
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_table(cells, design, output_location, showPlot):
    
    try:
        # # if includeHeaders:
        # report_headers = None
        # if headers != None:
        report_headers = design['headers']

        report_cells = dict(
            values=cells,  # Set cell values
            fill_color=design['cells']['fill_color'],  # Set cell fill color
            align=design['cells']['align'],  # Align cell text to the left
            height=design['cells']['height'],
            font=dict(color=design['cells']['font_color'], size=design['cells']['font_size'])
        )
        
        # Create Plotly table
        table = go.Table(
            columnwidth=design['layout'].get('column_widths'),
            header=report_headers,
            cells=report_cells
        )

        # Create a Plotly figure and add the table
        layout = go.Layout(
            autosize=True,
            width=design['layout']['width'],
            height=design['layout']['height']
        )
        fig = go.Figure(data=[table], layout=layout)

        # Update the color if we don't include headers so that it doesn't look like an empty header row
        if design['headers'] == None:
            fig.layout['template']['data']['table'][0]['header']['fill']['color']='rgba(0,0,0,0)'
        
        # Clean up margins
        fig.update_layout(
            margin=design['layout']['margin']
        )

        fig.write_image(output_location)
        if showPlot:
            fig.show()

    except Exception as e:
        logging.error("Error creating or saving the table: %s", e)
        raise