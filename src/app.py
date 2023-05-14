from dash import Dash, html, Input, Output
import dash_ag_grid as dag
import pandas as pd
import os

# this correctly displays table full-width

fn = 'Biface_main.csv'
lk_dir = 'https://raw.github.com/danwbean/Biface_data/main'  # github public url
df = pd.read_csv(os.path.join(lk_dir, fn), encoding_errors='replace',
                 skip_blank_lines=True, keep_default_na=False, dtype=object)

if 'PSAL_Catalog' in df.columns:    # convert PSAL to int32.  Works because always present (no missing data)
    df.rename(columns={'PSAL_Catalog': 'PSAL'}, inplace=True)  # requires inplace
    df.dropna(subset=['PSAL'], inplace=True)
    df['PSAL'] = df['PSAL'].astype(np.int32, errors='ignore')

dff = df[df['Processed'] == 'Processed']                    # only 'Processed' ppts
df = dff.sort_values(['Site_name', 'Local_ID'])             # sort by site, then local_id

app = Dash(__name__)
server = app.server

grid = dag.AgGrid(
    id='biface_grid',
    rowData=df.to_dict('records'),
    columnDefs=[{'field': i} for i in df.columns],
    defaultColDef={'resizable': True,
                   'sortable': True,
                   'filter': True,
                   'floatingFilter': True,
                   'minWidth': 75},
    columnSize='sizeToFit',
    className='ag-theme-alpine-dark',
    style={'height': 800, 'width': '100%'},
    dashGridOptions={'rowSelection': 'single'},
)

app.layout = html.Div([grid, html.Div(id='grid_output')])


# @app.callback(
#     Output('grid_output', 'children'),
#     Input('biface_grid', 'cellClicked')
# )
# def display_cell_clicked_on(cell):
#     if cell is None:
#         return 'Click on a cell'
#     return f"clicked on cell value:  {cell['value']}, column:   {cell['colId']}, row index:   {cell['rowIndex']}"


@app.callback(
    Output("grid_output", "children"),
    Input('biface_grid', 'selectedRows'),
)
def selected(selected):
    if selected:
        return f"You selected PSAL: {selected[0]['PSAL']}"
    return "No selections"

if __name__ == '__main__':
    app.run_server(debug=True)