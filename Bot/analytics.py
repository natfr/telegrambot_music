import pandas as pd
import os


def analytics_bot(user_info):
    """
    The function adds info about users to .csv file
    """
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "chat_id.csv"), delimiter=",")
    list_id = df['Chat_id'].values.tolist()
    list_username = df['Username'].values.tolist()
    list_lastname = df['Lastname'].values.tolist()
    list_firstname = df['Firstname'].values.tolist()

    if user_info.id not in list_id:
        list_id.append(user_info.id)
        df_temporary = pd.DataFrame(data=list_id)
        df_temporary.columns = ['Chat_id']

        if user_info.username == None:
            list_username.append('None')
        else:
            list_username.append(user_info.username)
        df_temporary['Username'] = pd.DataFrame(data=list_username)

        if user_info.first_name == None:
            list_firstname.append('None')
        else:
            list_firstname.append(user_info.first_name)
        df_temporary['Firstname'] = pd.DataFrame(data=list_firstname)

        if user_info.last_name == None:
            list_lastname.append('None')
        else:
            list_lastname.append(user_info.last_name)
        df_temporary['Lastname'] = pd.DataFrame(data=list_lastname)

        df_temporary.to_csv(os.path.join(os.path.dirname(__file__), "chat_id.csv"))
