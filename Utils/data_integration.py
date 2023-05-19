# Copy to top of each Module.py or Utility.py
project_name = 'Obsolescence_Predictions'
dependencies_path = f'C:/Users/delst/OneDrive/Desktop/Code/Workspace/{project_name}/Libraries/dependencies.py'
with open(dependencies_path, 'r') as file:
    code = file.read()
    exec(code)

class SheetMerger:
    def __init__(self, 
                 df_store:list, 
                 how_to_join:str
                 ):
        self.df_store = df_store
        self.how_to_join = how_to_join
    
    def merge_dfs_and_columns(self
                             ):
        """
        merge_dfs_and_fillna 
        Merge df_store on 'id' common column. 
        Duplicate features (_y) are removed, leaving on _x duplicate column

        Args:
            df_store: _description_
            how_to_join: _description_

        Returns:
            _x
        """    
        
        if len(self.df_store) == 0:
            return None

        # Use reduce to merge all dataframes
        df = reduce(lambda left,right: pd.merge(left,right,on='id', how=self.how_to_join), self.df_store)

        # Get columns with suffixes '_x' and '_y'
        cols_x = [col for col in df.columns if col.endswith('_x')]
        cols_y = [col.replace('_x', '_y') for col in cols_x]

        # Fill NaN values in '_x' column with values from '_y' column
        for col_x, col_y in zip(cols_x, cols_y):
            if col_y in df.columns:
                df[col_x].fillna(df[col_y], inplace=True)
                df.drop(columns=col_y, inplace=True)  # remove the '_y' column as it's no longer needed
        
        # If a column end in '_x' suffix, replace '_x'with ''
        df.columns = df.columns.str.replace('_x$', '')

        return df
    