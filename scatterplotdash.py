import plotly.graph_objects as go
import plotly as pl
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import io
import xlsxwriter
import flask
import base64
from flask import send_file


fig = go.Figure()
external_classNamesheets = ['assets/custom.css','https://codepen.io/chriddyp/pen/bWLwgP.css']
# https://www.w3schools.com/w3css/4/w3.css
# app = dash.Dash(__name__, external_classNamesheets=external_classNamesheets)
app = dash.Dash(__name__)
df = pd.read_csv('resources/final.csv')

df_cat_clear_download = pd.DataFrame()



states = df['State'].unique()
categories = ['Library', 'CMP', 'Wishlist']
states = states[~pd.isnull(states)]

"""
instead of creating three different dataframes one for each category we should be able to create one dataframe.
need to research more on this in future.
"""
df_lib = df[df.Category == 'library']
df_cmp = df[df.Category == 'cmp']
df_wsh = df[df.Category == 'wishlist']

df['text'] = f""" Category:
                  City: {df['City']} + '' 
                  + {df['State']} + ' ( ' + {df['StateCode']} + ') ' """

app.layout = html.Div(children=[
    #   html.H1("Map of Goodness", id='dd-output-container', className=main_title),
    #  html.Div( [ 
         html.Img(src=app.get_asset_url('OWLogoTM.png'),className='logo'),
    #  ] ),
   html.Div( [

    html.H4([
     html.Label("Data points currently displayed on the map   ",
    className='data_count_label'
    ), 
     html.Label("", id='data-count',
      className='data_count_style'
      )  
    ],
  ),
    
    dcc.Dropdown(
          id='select_category',
          options=[ {'label': category, 'value': category } for category in categories  ],
          value='All',
          placeholder="Select Category",
          multi=True
        #  className=cat_text_box
    ),

      dcc.Dropdown(
          id='select_state',
          options=[ {'label': state, 'value': state } for state in states  ],
          value='All',
          placeholder="Select State",
          multi=True
        #   className=state_text_box
    #   )]
      ),
#    html.Div( [       

   ],
     className='left_side_div'),


html.Div( [ 
    dcc.Graph(figure=fig,id='mapplot'),
],
className='graph'),



html.Div([
html.A(html.Button('Download Report', id='download-button', className='button_style'), id='download-link', className='download_link')
  ]
),


],
className='fluid_style '
)

@app.callback(
    [dash.dependencies.Output('mapplot', 'figure'),
    dash.dependencies.Output('data-count', 'children'),
    dash.dependencies.Output('download-link', 'href')],
    [dash.dependencies.Input('select_state', 'value'),
    dash.dependencies.Input('select_category', 'value')])

def update_output(value, cat_value):
    fig = go.Figure()
    
    df_wsh_state = pd.DataFrame()
    df_cmp_state = pd.DataFrame()
    df_lib_state = pd.DataFrame()
    df_cat_Clear = pd.DataFrame()

    global df_cat_clear_download

    df_wsh_nulled = pd.DataFrame()
    df_lib_nulled = pd.DataFrame()
    df_cmp_nulled = pd.DataFrame()

    cmp_visible = True
    lib_visible = True
    wsh_visible = True

    """
    We have to do below if condition because when we select the clear button (x) mark in the drop down
    for some reason the 'value' is assigned with null or None but, we have to show the full datapoints 
    when no state is selected or the drop down is empty.
    """
    
    if not cat_value:
        cat_value = ["Clear"]

    if not value:
        value = ["Clear"]

    if "All" in value or "Clear" in value:
        if 'All' in cat_value or 'Clear' in cat_value:
            df_wsh_state = df_wsh
            df_cmp_state = df_cmp
            df_lib_state = df_lib
            df_cat_clear_download = df_wsh_state.append(df_cmp_state.append(df_lib_state)).reset_index(drop=True)
            # download_csv(df_cat_clear_download)
            # print(df_cat_clear_download)
        else:
            if 'Wishlist' not in cat_value:
                  df_wsh_nulled = df_wsh.iloc[0:0]
            else:
                  df_wsh_nulled = df_wsh

            if 'CMP' not in cat_value:
                df_cmp_nulled = df_cmp.iloc[0:0]
            else:
                df_cmp_nulled = df_cmp
    
            if 'Library' not in cat_value:
                df_lib_nulled = df_lib.iloc[0:0]
            else:
                df_lib_nulled = df_lib
              
            df_wsh_state = df_wsh_nulled
            df_cmp_state = df_cmp_nulled
            df_lib_state = df_lib_nulled
            df_cat_Clear  = df_wsh_state.append(df_cmp_state.append(df_lib_state)).reset_index(drop=True)
            df_cat_clear_download = df_cat_Clear.copy()
                
    else:
        for stat in value:

              if 'Wishlist' not in cat_value:
                  df_wsh_nulled = df_wsh.iloc[0:0]
              elif 'Clear' in cat_value:
                  df_wsh_nulled = df_wsh[df_wsh.State == stat]
              else:
                  df_wsh_nulled = df_wsh[df_wsh.State == stat]
                  
              if 'CMP' not in cat_value:
                  df_cmp_nulled = df_cmp.iloc[0:0]
              elif 'Clear' in cat_value:
                  df_cmp_nulled = df_cmp[df_cmp.State == stat]
              else:
                  df_cmp_nulled = df_cmp[df_cmp.State == stat]
       
              if 'Library' not in cat_value:
                  df_lib_nulled = df_lib.iloc[0:0]
              elif 'Clear' in cat_value:
                  df_lib_nulled = df_lib[df_lib.State == stat]
              else:
                  df_lib_nulled = df_lib[df_lib.State == stat]
                
              df_wsh_state = df_wsh_state.append(df_wsh_nulled)
              df_cmp_state = df_cmp_state.append(df_cmp_nulled)
              df_lib_state = df_lib_state.append(df_lib_nulled)
              df_cat_Clear  = df_wsh_state.append(df_cmp_state.append(df_lib_state)).reset_index(drop=True)
              df_cat_clear_download = df_cat_Clear.copy()

    row_count = len(df_cmp_state.index) + len(df_wsh_state.index) + len(df_lib_state.index)

    fig.add_trace(go.Scattergeo(
        lon = df_wsh_state['Longitude'],
        lat = df_wsh_state['Latitude'],
        name='Wishlist',
        text = df_wsh_state['City'] + ' , ' + df_wsh_state['State'],
        mode = 'markers',
        marker_color = 'rgba(0, 102, 0)',
        marker = dict(size = 8, line=dict(width=1)),
     ))
   
    fig.add_trace(go.Scattergeo(
         lon = df_cmp_state['Longitude'],
         lat = df_cmp_state['Latitude'],
         name='CMP',
         text = df_cmp_state['City'] + ' , ' + df_cmp_state['State'],
         mode = 'markers',
         marker_color = 'rgba(255, 102, 0)',
         marker = dict(size = 8, line=dict(width=1)),
       ))
       
    fig.add_trace(go.Scattergeo(
         lon =  df_lib_state['Longitude'],
         lat =  df_lib_state['Latitude'],
         name='Library',
         text =  df_lib_state['City'] + ' , ' +  df_lib_state['State'],
         mode = 'markers',
         marker_color = 'rgba(128, 0, 255)',
         marker = dict(size = 8, line=dict(width=1)),
       ))
   
    fig.update_layout(
               margin=dict(l=20, r=20, t=20, b=20),
               autosize=True,
               geo_scope='usa',
               showlegend=True
            #    width=1000,
            #    height=600    
           )
       
    return fig, row_count, '/reportDownload'


@app.server.route('/reportDownload')
def download_csv():
    
    filename = 'Report.xlsx'
    buf = io.BytesIO()
    excel_writer = pd.ExcelWriter(buf, engine="xlsxwriter")
    df_cat_clear_download.reset_index(drop=True).to_excel(excel_writer, sheet_name="sheet1", index=False)
    excel_writer.save()
    excel_data = buf.getvalue()
    buf.seek(0)

    return send_file(
        buf,
        mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
        attachment_filename=filename,
        as_attachment=True,
        cache_timeout=0
    )

if __name__ == '__main__':
    app.run_server(host='0.0.0.0',debug=True)