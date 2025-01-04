from git import Repo
import os
import pandas as pd
import numpy as np
import mysql.connector



# ## Cloning from repository

repo_url = 'https://github.com/PhonePe/pulse'
clone_path = 'E:\Desktop\Projects\PhonePe Data Visualization\phonepe\Datas'

if not os.path.exists(clone_path):
    os.makedirs(clone_path)
    
repo_path = os.path.join(clone_path, os.path.basename(repo_url).removesuffix('.git').title())
print(repo_path)

# Repo.clone_from(repo_url, repo_path)

directory = os.path.join(repo_path, 'data')
print(directory)



# ## Renaming sub-directories and extract necessary paths

# Function to rename messy state names into formatted state name
def rename(directory):
    for root, dirs, files in os.walk(directory):
        if 'state' in dirs:
            state_dir = os.path.join(root, 'state')
            
            for state_folder in os.listdir(state_dir):
                old_path = os.path.join(state_dir, state_folder)
                new_path = os.path.join(state_dir, state_folder.title().replace('-',' ').replace('&','and'))
                os.rename(old_path, new_path)
    print('Renamed all sub-directories successfully')
    
# Extract path names in the'state'-named subdirectory
def extract_paths(directory):
    path_list = []
    
    for root, dirs, files in os.walk(directory):
        if os.path.basename(root) == 'state':
            path_list.append(root.replace('\\','/'))
            
    return path_list

rename(directory)

state_directories = extract_paths(directory)
print(state_directories)




# ## Creating DataFrame from cloned json files

# ### 1) Aggregate Transaction

state_path = state_directories[0]
state_list = os.listdir(state_path)
agg_trans_dict = {
    'State':[], 'Year':[], 'Quarter':[], 'Transaction_Type':[],
    'Transaction_Count':[], 'Transaction_Amount':[]
}

for state in state_list:
    year_path = state_path + '/' + state + '/'
    year_list = os.listdir(year_path)
    
    for year in year_list:
        quarter_path = year_path + year + '/'
        quarter_list = os.listdir(quarter_path)
        
        for quarter in quarter_list:
            json_path = quarter_path + quarter
            df = pd.read_json(json_path)
            
            try:
                for transaction_data in df['data']['transactionData']:
                    type = transaction_data['name']
                    count = transaction_data['paymentInstruments'][0]['count']
                    amount = transaction_data['paymentInstruments'][0]['amount']

                    # append to agg_trans_dict

                    agg_trans_dict['State'].append(state)
                    agg_trans_dict['Year'].append(int(year))
                    agg_trans_dict['Quarter'].append(int(quarter.removesuffix('.json')))
                    agg_trans_dict['Transaction_Type'].append(type)
                    agg_trans_dict['Transaction_Count'].append(int(count))
                    agg_trans_dict['Transaction_Amount'].append(float(amount))
            except:
                pass
agg_trans_df = pd.DataFrame(agg_trans_dict)

print(agg_trans_df.head())
print(agg_trans_df.dtypes)


# ### 2) Aggregate User

state_path = state_directories[2]
state_list = os.listdir(state_path)
agg_user_dict = {
    'State':[], 'Year':[], 'Quarter':[], 'Brand':[],
    'Transaction_Count':[], 'Percentage':[]
}

for state in state_list:
    year_path = state_path + '/' + state + '/'
    year_list = os.listdir(year_path)
    
    for year in year_list:
        quarter_path = year_path + year + '/'
        quarter_list = os.listdir(quarter_path)
        
        for quarter in quarter_list:
            json_path = quarter_path + quarter
            df = pd.read_json(json_path)
            
            try:
                for user_data in df['data']['usersByDevice']:
                    brand = user_data['brand']
                    count = user_data['count']
                    percentage = user_data['percentage']

                    # append to agg_user_dict

                    agg_user_dict['State'].append(state)
                    agg_user_dict['Year'].append(int(year))
                    agg_user_dict['Quarter'].append(int(quarter.removesuffix('.json')))
                    agg_user_dict['Brand'].append(brand)
                    agg_user_dict['Transaction_Count'].append(int(count))
                    agg_user_dict['Percentage'].append(float(percentage))
            except:
                pass
                
agg_user_df = pd.DataFrame(agg_user_dict)        

print(agg_user_df.head())
print(agg_user_df.dtypes)


# ### 3) Map Transaction

state_path = state_directories[4]
state_list = os.listdir(state_path)
map_trans_dict = {
    'State':[], 'Year':[], 'Quarter':[], 'District':[],
    'Transaction_Count':[], 'Transaction_Amount':[]
}

for state in state_list:
    year_path = state_path + '/' + state + '/'
    year_list = os.listdir(year_path)
    
    for year in year_list:
        quarter_path = year_path + year + '/'
        quarter_list = os.listdir(quarter_path)
        
        for quarter in quarter_list:
            json_path = quarter_path + quarter
            df = pd.read_json(json_path)
            
            try:
    #             for transaction_data in df['data'][0]:
                for transaction_data in df['data']['hoverDataList']:
                    district = transaction_data['name']
                    count = transaction_data['metric'][0]['count']
                    amount = transaction_data['metric'][0]['amount']

                    # append map_trans_dict 

                    map_trans_dict['State'].append(state)
                    map_trans_dict['Year'].append(int(year))
                    map_trans_dict['Quarter'].append(int(quarter.removesuffix('.json')))
                    map_trans_dict['District'].append(district.removesuffix(' district').title().replace(' And', ' and').replace('andaman', 'Andaman'))
                    map_trans_dict['Transaction_Count'].append(int(count))
                    map_trans_dict['Transaction_Amount'].append(float(amount))
                    
            except:
                pass
            
map_trans_df = pd.DataFrame(map_trans_dict)

print(map_trans_df.head())
print(map_trans_df.dtypes)


# ### 4) Map User

state_path = state_directories[6]
state_list = os.listdir(state_path)
map_user_dict = {
    'State':[], 'Year':[], 'Quarter':[], 'District':[],
    'Registered_User':[], 'App_Opens':[]
}

for state in state_list:
    year_path = state_path + '/' + state + '/'
    year_list = os.listdir(year_path)
    
    for quarter in year_list:
        quarter_path = year_path + year + '/'
        quarter_list = os.listdir(quarter_path)
        
        for quarter in quarter_list:
            json_path = quarter_path + quarter
            df = pd.read_json(json_path)
            
            try:
                for district, user_data in df['data']['hoverData'].items():
                    reg_user_count = user_data['registeredUsers']
                    app_open_count = user_data['appOpens']

                    # append to map_user_dict

                    map_user_dict['State'].append(state)
                    map_user_dict['Year'].append(int(year))
                    map_user_dict['Quarter'].append(int(quarter.removesuffix('.json')))
                    map_user_dict['District'].append(district.removesuffix(' district').title().replace(' And', ' and').replace('andaman', 'Andaman'))
                    map_user_dict['Registered_User'].append(int(reg_user_count))
                    map_user_dict['App_Opens'].append(int(app_open_count))
            except:
                pass
            
map_user_df = pd.DataFrame(map_user_dict)

print(map_user_df.head())
print(map_user_df.dtypes)


# ### 5) Top transaction district-wise 

state_path = state_directories[8]
state_list = os.listdir(state_path)
top_trans_dist_dict = {
    'State':[], 'Year':[], 'Quarter':[], 'District':[],
    'Transaction_Count':[], 'Transaction_Amount':[]
}

for state in state_list:
    year_path = state_path + '/' + state + '/'
    year_list = os.listdir(year_path)
    
    for year in year_list:
        quarter_path = year_path + year + '/'
        quarter_list = os.listdir(quarter_path)
        
        for quarter in quarter_list:
            json_path = quarter_path + quarter 
            df = pd.read_json(json_path)
            
            try:
                for district_data in df['data']['districts']:
                    district = district_data['entityName']
                    count = district_data['metric']['count']
                    amount = district_data['metric']['amount']

                    # append to top_trans_dist_dict

                    top_trans_dist_dict['State'].append(state)
                    top_trans_dist_dict['Year'].append(int(year))
                    top_trans_dist_dict['Quarter'].append(int(quarter.removesuffix('.json')))
                    top_trans_dist_dict['District'].append(district.title().replace(' And', ' and').replace('andaman', 'Andaman'))
                    top_trans_dist_dict['Transaction_Count'].append(int(count))
                    top_trans_dist_dict['Transaction_Amount'].append(float(amount))
            except:
                pass
            
top_trans_dist_df = pd.DataFrame(top_trans_dist_dict)

print(top_trans_dist_df.head())
print(top_trans_dist_df.dtypes)


# ### 6) Top transaction pincode-wise

state_path = state_directories[8]
state_list = os.listdir(state_path)
top_trans_pin_dict = {
    'State':[], 'Year':[], 'Quarter':[], 'Pincode':[],
    'Transaction_Count':[], 'Transaction_Amount':[]
}

for state in state_list:
    year_path = state_path + '/' + state + '/'
    year_list = os.listdir(year_path)
    
    for year in year_list:
        quarter_path = year_path + year + '/'
        quarter_list = os.listdir(quarter_path)
        
        for quarter in quarter_list:
            json_path = quarter_path + quarter
            df = pd.read_json(json_path)
            
            try: 
                for regional_data in df['data']['pincodes']:
                    pin = regional_data['entityName']
                    count = regional_data['metric']['count']
                    amount = regional_data['metric']['amount']

                    # append to top_trans_pin_dict

                    top_trans_pin_dict['State'].append(state)
                    top_trans_pin_dict['Year'].append(int(year))
                    top_trans_pin_dict['Quarter'].append(int(quarter.removesuffix('.json')))
                    top_trans_pin_dict['Pincode'].append(pin)
                    top_trans_pin_dict['Transaction_Count'].append(int(count))
                    top_trans_pin_dict['Transaction_Amount'].append(float(amount))
            except:
                pass
            
top_trans_pin_df = pd.DataFrame(top_trans_pin_dict)
top_trans_pin_df = top_trans_pin_df.dropna() 
top_trans_pin_df.Pincode = top_trans_pin_df.Pincode.astype('int64')

print(top_trans_pin_df.head())
print(top_trans_pin_df.dtypes)


# ### 7) Top User District-wise

state_path = state_directories[9]
state_list = os.listdir(state_path)
top_user_dist_dict = {
    'State':[], 'Year':[], 'Quarter':[],
    'District':[], 'Registered_User':[]
}

for state in state_list:
    year_path = state_path + '/' + state + '/'
    year_list = os.listdir(year_path)
    
    for year in year_list:
        quarter_path = year_path + year + '/'
        quarter_list = os.listdir(quarter_path)
        
        for quarter in quarter_list:
            json_path = quarter_path + quarter
            df = pd.read_json(json_path)
            
            try:
                for district_data in df['data']['districts']:
                    dist = district_data['name']
                    reg_user = district_data['registeredUsers']

                    # append to top_user_dist_dict

                    top_user_dist_dict['State'].append(state)
                    top_user_dist_dict['Year'].append(int(year))
                    top_user_dist_dict['Quarter'].append(int(quarter.removesuffix('.json')))
                    top_user_dist_dict['District'].append(dist.title().replace(' And', ' and').replace('andaman', 'Andaman'))
                    top_user_dist_dict['Registered_User'].append(int(reg_user))
            except:
                pass
            
top_user_dist_df = pd.DataFrame(top_user_dist_dict)

print(top_user_dist_df.head())
print(top_user_dist_df.dtypes)


# ### 8) Top user pincode-wise

state_path = state_directories[9]
state_list = os.listdir(state_path)
top_user_pin_dict = {
    'State':[], 'Year':[], 'Quarter':[],
    'Pincode':[], 'Registered_User':[]
}

for state in state_list:
    year_path = state_path + '/' + state + '/'
    year_list = os.listdir(year_path)
    
    for year in year_list:
        quarter_path = year_path + year + '/'
        quarter_list = os.listdir(quarter_path)
        
        for quarter in quarter_list:
            json_path = quarter_path + quarter 
            df = pd.read_json(json_path)
            
            try: 
                for user_data in df['data']['pincodes']:
                    pin = user_data['name']
                    user = user_data['registeredUsers']
                    
                    # append to top_user_pin_dict
                    
                    top_user_pin_dict['State'].append(state)
                    top_user_pin_dict['Year'].append(int(year))
                    top_user_pin_dict['Quarter'].append(int(quarter.removesuffix('.json')))
                    top_user_pin_dict['Pincode'].append(pin)
                    top_user_pin_dict['Registered_User'].append(int(user))
            except:
                pass
            
top_user_pin_df = pd.DataFrame(top_user_pin_dict)
top_user_pin_df.dropna(inplace=True)
top_user_pin_df.Pincode = top_user_pin_df.Pincode.astype('int64')

print(top_user_pin_df.head())
print(top_user_pin_df.dtypes)



# #### List of DataFrames created

df_list = [df for df in globals() if isinstance(globals()[df], pd.core.frame.DataFrame) and df.endswith('_df')]
print(df_list)


# ### Removing Delhi Districts to manage inconsistency

def add_suffix_to_districts(df):
    if 'District' in df.columns and 'State' in df.columns:
        delhi_df = df[df['State'] == 'Delhi']
        
        districts_to_suffix = [ d for d in delhi_df['District'].unique() if d != 'Shahdara']
        
        df.loc[(df['State']=='Delhi') & (df['District'].isin(districts_to_suffix)), 'District'] = df.loc[(df['State']=='Delhi') & (df['District'].isin(districts_to_suffix)), 'District'].apply(lambda a : a+'Delhi' if 'Delhi' not in a else a)
        
for df_name in df_list:
    df = globals()[df_name]
    add_suffix_to_districts(df)
    print(add_suffix_to_districts(df))


# ### Adding Latitude and Longitude columns

# lat_long_df = pd.read_csv(r'D:\Desktop\Demo Projects\Datas\Miscellaneous\dist_lat_long.csv')

# for df_name in df_list:
#     df = globals()[df_name]
#     if 'District' in df.columns:
#         df = pd.merge(df, lat_long_df, on=['State', 'District'], how='left')
#         globals()[df_name] = df


# ### Adding region column to all dataframes

def add_region_column(df):
    state_groups = {
        'Northern Region': ['Jammu and Kashmir', 'Himachal Pradesh', 'Punjab', 'Chandigarh', 'Uttarakhand', 'Ladakh', 'Delhi', 'Haryana'],
        'Central Region': ['Uttar Pradesh', 'Madhya Pradesh', 'Chhattisgarh'],
        'Western Region': ['Rajasthan', 'Gujarat', 'Dadra and Nagar Haveli and Daman and Diu', 'Maharashtra'],
        'Eastern Region': ['Bihar', 'Jharkhand', 'Odisha', 'West Bengal', 'Sikkim'],
        'Southern Region': ['Andhra Pradesh', 'Telangana', 'Karnataka', 'Kerala', 'Tamil Nadu', 'Puducherry', 'Goa', 'Lakshadweep', 'Andaman and Nicobar Islands'],
        'North-Eastern Region': ['Assam', 'Meghalaya', 'Manipur', 'Nagaland', 'Tripura', 'Arunachal Pradesh', 'Mizoram']
    }
    
    df['Region'] = df['State'].map({state: region for region, states in state_groups.items() for state in states})
    return df


for df_name in df_list:
    df = globals()[df_name]
    add_region_column(df)


# ### Columnwise null count and duplicated rows count

for df_name in df_list:
    df = globals()[df_name]
    print(f'{df_name}')
    print(f'null count : \n{df.isnull().sum().sum()}')
    df = df.drop_duplicates()
    df = df.dropna()
    print(f'null count : \n{df.isnull().sum().sum()}')
    print(f'dropped dup : {df.duplicated().any()}')
    print(f'duplicated row count : {df.duplicated().sum()}')
    print(df.shape)
    print('\n', 80*'_', '\n')




print('Dataframe info : \n')

for df_name in df_list:
    df = globals()[df_name]
    print(df_name + ': \n')
    df.info()
    print('\n', 75*'_', '\n')



for df_name in df_list:
    print(df_name)



agg_trans_df = agg_trans_df.dropna()
agg_user_df = agg_user_df.dropna()
map_trans_df = map_trans_df.dropna()
map_user_df = map_user_df.dropna()
top_trans_dist_df = top_trans_dist_df.dropna()
top_trans_pin_df = top_trans_pin_df.dropna()
top_user_dist_df = top_user_dist_df.dropna()
top_user_pin_df = top_user_pin_df.dropna()




agg_trans_df = agg_trans_df.drop_duplicates()
agg_user_df = agg_user_df.drop_duplicates()
map_trans_df = map_trans_df.drop_duplicates()
map_user_df = map_user_df.drop_duplicates()
top_trans_dist_df = top_trans_dist_df.drop_duplicates()
top_trans_pin_df = top_trans_pin_df.drop_duplicates()
top_user_dist_df = top_user_dist_df.drop_duplicates()
top_user_pin_df = top_user_pin_df.drop_duplicates()



print(top_user_pin_df.duplicated().any())


# ### Outliers finding across all dataframes

def outliers(df):
    outliers = {}
    for col in df.select_dtypes(include=[np.number]).columns:
        if col in ['Transaction_Count', 'Transaction_Amount']:
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1 
            lower = q1 - (1.5 * iqr)
            upper = q3 + (1.5 * iqr)
            outliers[col] = len(df[(df[col]>upper) | (df[col]<lower)])
        else:
            continue
    return outliers



print('Outliers all dataframes : \n')
for df_name in df_list:
    df = globals()[df_name]
    outliers_all = outliers(df)
    if len(outliers_all) == 0:
        pass
    else:
        print(df_name, '\n', outliers_all, '\n')
        print(50*'_', '\n')


# ### Unique values count across all dataframes
        
def unique_values_count(df, exclude_cols=[]):
    for col in df.columns:
        if col in exclude_cols:
            continue
        unique_values = df[col].nunique()
        print(f'{col} : {unique_values} unique values')
        if unique_values < 10:
            print(df[col].unique())





print('Unique value count across all dataframes \n\n')

for df_name in df_list:
    df = globals()[df_name]
    print(df_name, ':\n')
    unique_values_count(df, exclude_cols = ['State', 'Year', 'Quarter', 'Percentage'])
    print('\n', 80*'_', '\n')


# ### Creating CSV files out of refined dataframes

def save_dfs_as_csv(df_list):
    subfolder = 'E:\Desktop\Projects\PhonePe Data Visualization\phonepe\Datas\Miscellaneous'
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
        
    for df_name in df_list:
        df = globals()[df_name]
        file_path = os.path.join(subfolder, df_name.replace('_df','') + '.csv')
        df.to_csv(file_path, index=False)
        
save_dfs_as_csv(df_list)




# ### SQL Part

# #### Establishing connection and create cursor

import mysql.connector
conn = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '123456'
)

cursor = conn.cursor()



print(top_user_dist_df.dtypes)


# #### Database creation

cursor.execute('drop database if exists phonepe')

cursor.execute('create database phonepe')

cursor.execute('use phonepe')


# #### Creating tables


cursor.execute('''create table agg_trans(
                  state varchar(255)
                  ,year year
                  ,quarter int
                  ,transaction_type varchar(255)
                  ,transaction_count int
                  ,transaction_amount float
                  ,region varchar(255)
                  ,primary key(state(255), year, quarter, transaction_type(255), region(255))
                  )''')

cursor.execute('''create table agg_user(
                  state varchar(255)
                  ,year year
                  ,quarter int
                  ,brand varchar(255)
                  ,transaction_count int
                  ,percentage float
                  ,region varchar(255)
                  ,primary key(state(255), year, quarter, brand(255), region(255))
                  )''')

cursor.execute('''create table map_trans(
                  state varchar(255)
                  ,year year
                  ,quarter int
                  ,district varchar(255)
                  ,transaction_count int
                  ,transaction_amount float
                  ,latitude float
                  ,longitude float
                  ,region varchar(255)
                  ,primary key(state(255), year, quarter, district(255), region(255))
                  )''')

cursor.execute('''create table map_user(
                  state varchar(255)
                  ,year year
                  ,quarter int
                  ,district varchar(255)
                  ,registered_user int
                  ,app_opens int
                  ,latitude float
                  ,longitude float
                  ,region varchar(255)
                  ,primary key(state(255), year, quarter, district(255),  region(255))
                  )''')

cursor.execute('''create table top_trans_dist(
                  state varchar(255)
                  ,year year
                  ,quarter int
                  ,district varchar(255)
                  ,transaction_count int
                  ,transaction_amount float
                  ,latitude float
                  ,longitude float
                  ,region varchar(255)
                  ,primary key(state(255), year, quarter, district(255),  region(255))
                  )''')

cursor.execute('''create table top_trans_pin(
                  state varchar(255)
                  ,year year
                  ,quarter int
                  ,pincode int
                  ,transaction_count int
                  ,transaction_amount float
                  ,region varchar(255)
                  ,primary key(state(255), year, quarter, pincode,  region(255))
                  )''')

cursor.execute('''create table top_user_dist(
                  state varchar(255)
                  ,year year
                  ,quarter int
                  ,district varchar(255)
                  ,registered_user int
                  ,latitude float
                  ,longitude float
                  ,region varchar(255)
                  ,primary key(state(255), year, quarter, district(255),  region(255))
                  )''')

cursor.execute('''create table top_user_pin(
                  state varchar(255)
                  ,year year
                  ,quarter int
                  ,pincode int 
                  ,registered_user int
                  ,region varchar(255)
                  ,primary key(state(255), year, quarter, pincode,  region(255))
                  )''')


# #### Pushing data into MySQL

def push_data_into_mysql(conn, cursor, dfs, table_columns):
    for table_name in dfs.keys():
        df = dfs[table_name]
        columns = table_columns[table_name]
        placeholders = ', '.join(['%s'] * len(columns))
        query = f"insert into {table_name} ({', '.join(columns)}) values ({placeholders})"
        for _, row in df.iterrows():
            data = tuple(row[column] for column in columns)
            cursor.execute(query, data)
        conn.commit()
    print('Datas successfully pushed into MySQL Tables')




dfs = {
    'agg_trans':agg_trans_df,
    'agg_user':agg_user_df,
    'map_trans':map_trans_df,
    'map_user':map_user_df,
    'top_trans_dist':top_trans_dist_df,
    'top_trans_pin':top_trans_pin_df,
    'top_user_dist':top_user_dist_df,
    'top_user_pin':top_user_pin_df
}

table_columns = {
    'agg_trans':list(agg_trans_df.columns),
    'agg_user':list(agg_user_df.columns),
    'map_trans':list(map_trans_df.columns),
    'map_user':list(map_user_df.columns),
    'top_trans_dist':list(top_trans_dist_df.columns),
    'top_trans_pin':list(top_trans_pin_df.columns),
    'top_user_dist':list(top_user_dist_df.columns),
    'top_user_pin':list(top_user_pin_df.columns)
}




push_data_into_mysql(conn, cursor, dfs, table_columns)




# cursor.execute('use phonepe')




cursor.execute('show tables')
tables = cursor.fetchall()

for table in tables:
    table_name = table[0]
    cursor.execute(f'select count(*) from {table_name}')
    row_count = cursor.fetchone()[0]
    cursor.execute(f"select count(*) from information_schema.columns where table_name='{table_name}'")
    column_count = cursor.fetchone()[0]
    
    df = dfs[table_name]
    if df.shape == (row_count, column_count):
        print(f'{table_name} table has {row_count} rows and {column_count} columns,  Shape matched')
    else:
        print(f'{table_name} table has {row_count} rows and {column_count} columns,Shape not matched')
        
cursor.close()
conn.close()

