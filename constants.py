import os

dataset_table = 'dataset_table'

    # If in a workspace, then write to a different table
    # If you want to read from or write to the same data as your deployed app,
    # then you can remove this line
dataset_table = 'workspace_dataset_table' if os.environ.get('DASH_ENTERPRISE_ENV') == 'WORKSPACE' else 'dataset_table'

