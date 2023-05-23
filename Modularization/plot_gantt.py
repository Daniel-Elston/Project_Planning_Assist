# Copy to top of each Module.py or Utility.py
project_name = 'Project_Planning_Assistant'
dependencies_path = f'C:/Users/delst/OneDrive/Desktop/Code/Workspace/{project_name}/Libraries/dependencies.py'
with open(dependencies_path, 'r') as file:
    code = file.read()
    exec(code)
    
def gantt_input_data(stage_list, 
                     start_dates, 
                     end_dates, 
                     suggested_end_hours,
                    #  get_diff, 
                     completion_hour,
                    #  randomize_hours
                     ):

    diff = []
    for i in range(len(suggested_end_hours)):
        if i == 0:
            diff.append(suggested_end_hours[i])
        else:
            diff.append(suggested_end_hours[i] - suggested_end_hours[i-1])
            
    # compute the initial variables
    estimated_hours_to_complete = diff
    starting_hour = pd.Series([0] + completion_hour[:-1])  # shift operation
    hours_spent = (completion_hour - starting_hour).fillna(0) 
    estimated_end_hour = starting_hour + estimated_hours_to_complete

    # create the dataframe
    df = pd.DataFrame({
        'Stage': stage_list,
        'start_date': start_dates,
        'end_date': end_dates,
        'starting_hour': starting_hour,
        'estimated_end_hour': estimated_end_hour,
        'estimated_hours_to_complete': estimated_hours_to_complete,
        'completion_hour': completion_hour,
        'hours_spent': hours_spent, 
        })

    # add exceeded_hours and finished_early_hours to the dataframe
    df['exceeded_hours'] = np.where(df['hours_spent'] > df['estimated_hours_to_complete'], df['hours_spent'] - df['estimated_hours_to_complete'], 0)
    df['finished_early_hours'] = np.where(df['hours_spent'] < df['estimated_hours_to_complete'], df['estimated_hours_to_complete'] - df['hours_spent'], 0)
    
    return df

def create_gantt_chart(df):
    axis_label_color = 'black'

    light_navy = px.colors.qualitative.Pastel1[1]
    navy = px.colors.qualitative.T10[0]
    dark_navy = px.colors.qualitative.Antique[4]

    dark_grey = px.colors.qualitative.Set1[8]
    darker_grey = px.colors.qualitative.Dark2[7]
    light_grey = px.colors.qualitative.Pastel[10]
    lighter_grey = px.colors.qualitative.Pastel2[7]
    
    bar_color = dark_grey

    grid_color = axis_label_color

    graph_color = dark_navy
    bg_color = dark_navy
    
    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=df['Stage'],
        x=df['hours_spent'],
        base=df['starting_hour'],
        orientation='h',
        marker=dict(
            color=dark_grey,
            line=dict(color='rgba(0,0,0,0)')  # Set the line color to transparent

        ),
        name='Hours Spent'
    ))

    fig.add_trace(go.Bar(
        y=df['Stage'],
        x=df['exceeded_hours'],
        base=df['estimated_end_hour'],
        orientation='h',
        marker=dict(
            color='red',
            opacity=0.5,
            line=dict(color='rgba(0,0,0,0)')  # Set the line color to transparent
        ),
        name='Exceeded Hours'
    ))

    fig.add_trace(go.Bar(
        y=df['Stage'],
        x=df['finished_early_hours'],
        base=df['completion_hour'],
        orientation='h',
        marker=dict(
            color='green',
            opacity=0.5,
            line=dict(color='rgba(0,0,0,0)')  # Set the line color to transparent
        ),
        name='Finished Early'
    ))



    fig.update_layout(
        barmode='stack',
        title={
            'text':'Gantt Chart',
            'font':{
                'size':24,
                'color':axis_label_color,
                # 'bold': True,
            },
            },
        xaxis_title='Project Hours',
        yaxis_title='Stage',
        xaxis=dict(
            showgrid=True,  # Add grid lines on the x-axis
            tickmode='linear',  # Use linear tick mode
            dtick=5,  # Set the tick interval to 3
            gridcolor=grid_color,  # Set the color of the grid lines
            showline=True,  # Show x-axis line
            linewidth=1,  # Set x-axis line width
            linecolor=grid_color,  # Set x-axis line color
            title=dict(
                font=dict(color=axis_label_color)  # Set the x-axis label text color to white
            ),
            tickfont=dict(color=axis_label_color)  # Set the x-axis tick labels color to white
        ),
        yaxis=dict(
            showgrid=False,  # Remove grid lines on the y-axis
            showline=True,  # Show y-axis line
            linewidth=1,  # Set y-axis line width
            linecolor='grey',  # Set y-axis line color
            title=dict(
                font=dict(color=axis_label_color)  # Set the y-axis label text color to white
            ),
            tickfont=dict(color=axis_label_color)  # Set the y-axis tick labels color to white
        ),
        height=800,  # Set the plot height to 600 pixels
        plot_bgcolor=graph_color,  # Set the background color
        paper_bgcolor=bg_color,  # Set the paper background color
        showlegend=False,  # Hide legend
        margin=dict(l=20, r=20, t=40, b=20),  # Set margin
        hovermode='closest',  # Set hover mode
        shapes=[
            dict(
                type='rect',
                xref='paper',
                yref='paper',
                x0=0,
                y0=0,
                x1=1,
                y1=1,
                line=dict(
                    color=grid_color,
                    width=2
                )
            )
        ]
    )

    fig.show()