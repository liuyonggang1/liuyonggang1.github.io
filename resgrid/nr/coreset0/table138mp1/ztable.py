from browser import alert
from browser.html import TABLE, TR, TH, TD, CAPTION

def transpose(data):
    # equivalent to excel transpose paste. row to col, col to row.
    if data is None:
        return None
    result = []
    ncols = len(data[0])
    result = [[] for i in range(ncols)]
    for row in data:
        for col, v in enumerate(row):
            result[col].append(v)
    return result

def create_table(data=None, 
                 class_data=None, 
                 num_head_rows=0, 
                 num_head_cols=0, 
                 caption=None, 
                 num_merge_rows=None, 
                 num_merge_cols=None):
    """
    head-a1                      | num_head_row0 
                                 | num_head_row1 
    ------------------------------------------------------------
    num_head_col0  num_head_col1 | Data    
    """
    if data is None and class_data is not None:
        data = [['' for col in row] for row in class_data]
    elif data is not None and class_data is None:
        class_data = [['' for col in row] for row in data]
    elif data is None and class_data is None:
        alert('Error in ztable.create_table, both data and class_data are None. This is invalid')
    nrows = len(data)
    ncols = len(data[0])
    for i in range(num_head_rows):
        for j in range(num_head_cols):
            class_data[i][j] += ' head-a1'
    
    for i in range(num_head_rows):
        for j in range(num_head_cols, ncols):
            class_data[i][j] += ' head-row'
            class_data[i][j] += f' head-row{i}'
            
    for i in range(num_head_rows, nrows):
        for j in range(num_head_cols):
            class_data[i][j] += ' head-col'
            class_data[i][j] += f' head-col{j}'
    
    for i in range(num_head_rows, nrows):
        for j in range(num_head_cols, ncols):
            try:
                class_data[i][j] += ' cell-data'
            except:
                print("ztable.py 54", num_head_rows, nrows)
                print("ztable.py 55", i, j)
                raise
            
    rowSpan_data = [[1 for col in row] for row in data]
    colSpan_data = [[1 for col in row] for row in data]
    
    if num_merge_rows is None:
        num_merge_rows = num_head_rows
    if num_merge_cols is None:
        num_merge_cols = num_head_cols
        
    # merge head rows's colSpan
    for r in range(num_merge_rows):
        cursor = 0
        for c in range(1, ncols):
            if data[r][cursor] == data[r][c]:
                data[r][c] = None
                colSpan_data[r][cursor] += 1
            else:
                cursor = c
    # merge head cols's rowSpan
    for c in range(num_merge_cols):
        cursor = 0
        for r in range(1, nrows):
            if data[cursor][c] == data[r][c]:
                data[r][c] = None
                rowSpan_data[cursor][c] += 1
            else:
                cursor = r
    # merge head rows's colSpan
    table = TABLE()
    if caption is not None:
        table <= CAPTION(caption)
    for r in range(nrows):
        tds = []
        for c in range(ncols):
            if data[r][c] is not None:
                td = TD(data[r][c])
                class_name = class_data[r][c].strip()
                if class_name != '':
                    td.class_name = class_name
                rowSpan = rowSpan_data[r][c]
                if rowSpan > 1:
                    td.rowSpan = rowSpan
                colSpan = colSpan_data[r][c]
                if colSpan > 1:
                    td.colSpan = colSpan
                tds.append(td)
        table <= TR(tds)
    return table

#######################################################################################################################

def create_htable(a1=None, 
                  x=None, 
                  y=None, 
                  data=None, 
                  class_data=None, 
                  caption=None, 
                  num_merge_rows=None, 
                  num_merge_cols=None):
    """
    A1 | X 
    ----------
    Y  | Data

    A1, X, Y, Data: list of list [[], [],...], 
    If input type is [], but not [[]],  it will be changed [a1/x/y/Data]

    A1, X, Data is [row0, row1, ...]
    Y = [col0, col1, ...]
    """
    if x is None:
        x = []
    elif not isinstance(x[0], list):
        x = [x]

    if y is None:
        y = []
    elif not isinstance(y[0], list):
        y = [y]
        
    num_head_rows = len(x)
    num_head_cols = len(y)
    
    if a1 is None:
        a1 = [['' for c in range(num_head_cols)] for r in range(num_head_rows)]
    elif not isinstance(a1[0], list):
        a1 = [a1]

    if data is None:
        # class_data should not be None
        data = [['' for c in row] for row in class_data]
        
    table_data = []
    for a1_row, x_row in zip(a1, x):
        table_data.append(a1_row+x_row)
        
    if y != []:
        ty = transpose(y)
    else:
        ty = [[] for row in data]
        
    for ty_row, data_row in zip(ty, data):
        table_data.append(ty_row+data_row)
        
    if class_data is None:
        table_class_data = None
    else:
        table_class_data = [['' for c in row] for row in table_data]
        for i, row in enumerate(class_data):
            for j, v in enumerate(row):
                table_class_data[num_head_rows+i][num_head_cols+j] = v
                
    return create_table(data=table_data, 
                 class_data=table_class_data, 
                 num_head_rows=num_head_rows, 
                 num_head_cols=num_head_cols, 
                 caption=caption, 
                 num_merge_rows=num_merge_rows, 
                 num_merge_cols=num_merge_cols)
