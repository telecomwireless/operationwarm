"""
Script to preprocess data so that it can be used to plot on the map.
This scripts takes in the three datasets  (CMP, Library and wishlist)

"""
import pandas as pd

def write_to_csv(input_file, filename):
    with open(f"resources\\{filename}.csv", 'a') as f:
      input_file.to_csv(f, mode='a', header=f.tell()==0)

df_cities = pd.read_csv("resources\\uscities.csv", usecols = ['city', 'state_id','state_name', 'lat', 'lng'], encoding = 'unicode_escape')
df_cities = df_cities.applymap(lambda s:s.lower() if type(s) == str else s)
df_states = df_cities.copy()
df_states.drop_duplicates(subset=['state_id','state_name'],keep='first',inplace=True)
df_state_series =  df_states['state_name']
df_state_id = df_states['state_id']
df_city_series = df_cities['city']
df_missing_places = pd.DataFrame(columns= ['Category','City', 'State'])
# write_to_csv(df_cities, "cities_trimmed")

def get_lat_lng(city, state):
    lat_lng = ()
    if city in df_cities.city.values:
        city_index = df_city_series[df_city_series == city].index.tolist()
        for i in city_index:
            if df_cities['state_id'][i] == state and df_cities['city'][i] == city:
                lat_lng = (df_cities['lat'][i], df_cities['lng'][i])
                break
            # else:
            #     print(f"state and city is::: {df_cities['state_id'][i]} and {df_cities['city'][i]}")
    return lat_lng


def state_finder(state):
    state_code = ""
    if len(state) > 2:
        if state in df_states.state_name.values:
           state_index = df_state_series[df_state_series == state].index[0]
           state_code = df_states['state_id'][state_index]
    else:
        if state in df_states.state_id.values:
            state_index = df_states[df_states.state_id == state].index[0]
            state_code = df_states['state_name'][state_index]

    return state_code


df_category = pd.DataFrame(columns= ['Category','Name','City', 'State'])


cat_dict = {
     "Library": "Library.csv",
     "CMP": "CMP.csv",
     "Wishlist" : "Wishlist.csv"  
}

for key in cat_dict:
    df = pd.read_csv(f"resources\\{cat_dict[key]}", usecols = ['City', 'State', 'Name'], encoding = 'unicode_escape')
    df['Category'] = key
    df_category = df_category.append(df, ignore_index=True)

df_category = df_category.dropna()
df_category = df_category.applymap(lambda s:s.lower() if type(s) == str else s)
# df_category.drop_duplicates(subset=['Category','City', 'State'],keep='first',inplace=True)
# df_category = df_category.reset_index(drop=True)
df_category['City'] = df_category['City'].str.strip()
df_category['State'] = df_category['State'].str.strip()

df_category = df_category.assign(StateCode='',Latitude='', Longitude='')

"""
 Color list is used for assigning a color to a category. plotly geoscatter seems to be accepting only
 integer or rgba() values so using below we are giving a number for each category.
"""
# color_list=[1,2,3]

for index, row in df_category.iterrows():
    df_category['Name'][index] = row['Name']
    if len(row['State']) > 2:
        df_category['State'][index] = row['State']
        state_code =  state_finder(df_category['State'][index])
        df_category['StateCode'][index] = state_code
    else:
        df_category['StateCode'][index] = row['State']
        df_category['State'][index] = state_finder(df_category['State'][index])
          
    lat_lng = get_lat_lng(row['City'],row['StateCode'])
    if lat_lng:
       df_category['Latitude'][index] = lat_lng[0]
       df_category['Longitude'][index] = lat_lng[1]
    else:
         df_missing_places = df_missing_places.append({'Category': row['Category'], 'City':row['City'], 'State': row['State']},ignore_index=True)
    
    # if df_category['Category'][index] == "library":
    #     df_category['Color'][index] = color_list[0]

    # elif df_category['Category'][index] == "cmp":
    #     df_category['Color'][index] = color_list[1]

    # elif df_category['Category'][index] == "wishlist":
    #     df_category['Color'][index] = color_list[2]

df_category['State'] = df_category['State'].apply(lambda x: x.capitalize())
df_category['City'] = df_category['City'].apply(lambda x: x.capitalize())
df_category['StateCode'] = df_category['StateCode'].apply(lambda x: x.upper())
df_category = df_category[df_category['Latitude'].notnull()]
write_to_csv(df_category, "final")