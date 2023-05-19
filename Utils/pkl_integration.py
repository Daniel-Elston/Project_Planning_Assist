# Copy to top of each Module.py or Utility.py
project_name = 'Project_Planning_Assistant'
dependencies_path = f'C:/Users/delst/OneDrive/Desktop/Code/Workspace/{project_name}/Libraries/dependencies.py'
with open(dependencies_path, 'r') as file:
    code = file.read()
    exec(code)


def file_loader(data):
    """
    load_file 
    Load the file path specified and store dataframes in a list.

    Args:
        raw_data: Selected file

    Returns:
        List of dataframes
    """    
    
    df_dict = pd.read_excel(data, sheet_name=None)
    df_list = list(df_dict.values())
    
    # Creates an if statement, if just 1 element in the list, load as a pd.DataFrame
    if len(df_list) == 1:
        df_list = df_list[0]
    else:
        pass

    return df_list


def save_data_to_pickle(data_to_save:object, 
                        file_name:str, 
                        directory:str
                        ):
    """
    Saves a Python object to a pickle file in the specified directory.

    Parameters:
    data (object): the Python object to save
    filename (str): the name of the pickle file to save
    directory (str): the directory to save the pickle file in

    Returns:
    None
    """
    # create the directory if it doesn't exist
    # if not os.path.exists(directory):
    #     os.makedirs(directory)

    # save the data to a pickle file in the specified directory
    filepath = os.path.join(directory, file_name)
    with open(filepath, 'wb') as f:
        pickle.dump(data_to_save, f)

    print(f"Data saved to {filepath}")
    
    
def load_raw_and_store(df_store,
                       output_dir,
                       file_name
                       ):
    
    # df_store = file_loader(data)
    data_to_save = df_store

    # Save to outputs dir
    save_data_to_pickle(data_to_save, file_name, output_dir)
    
    # df_store_output = os.path.join(output_dir, 'df_pipe_store.pkl')
    df_store_output = os.path.join(output_dir, file_name)

    # Load .pkl from outputs directory as a list of dataframes
    with open(df_store_output, 'rb') as file:
        df_store = pickle.load(file)
        
    return df_store


def file_pipeline(data,
                  output_dir,
                  file_name
                  ):
    
    
    file_loader(data)
    df_store = load_raw_and_store(df_store, output_dir, file_name)

    df_store_output = os.path.join(output_dir, file_name)

    with open(df_store_output, 'rb') as file:
        df_store = pickle.load(file)
    return df_store