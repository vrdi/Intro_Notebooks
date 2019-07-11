#!/usr/bin/env python
# coding: utf-8

# # Introduction
# 
# # Setup
# Begin by importing the requests and pandas packages. We also define a constant `HOST`, which will appear at the beginning of every API request. By convention, constants are given names in all uppercase.

# In[ ]:


# Imports
import requests
import pandas as pd

# Constants
HOST = "https://api.census.gov/data"


# # Basic API Call
# 
# In this section we will use a basic API call to request median household income data for states. The data comes from the American Community Survey 2017 5-year average. The variable with median household income data is `B19013_001E`. The `E` at the end indicates that this is an **estimate**. If instead we used `M` we would get the **margin of error** at a 90% confidence interval.
# 
# Begin by specifying the year and data product, and a list of variables.
# 
# You can view a list of available Census APIs (data products) at https://www.census.gov/data/developers/data-sets.html. ACS is available in both 1-year averages (for large geographies only) and 5-year averages. The Decennial Census is available for 2010, 2000, and 1990. Long-form data (Summary File 3) is avialable for 2000 and 1990. (Remember that by 2010 the ACS was available, so there is no SF3 data for 2010).

# In[ ]:


# Census Data Products
year = "2017"
dataset = "acs/acs5"
base_url = "/".join([HOST, year, dataset])

# Specify variables to request
get_vars = ["NAME", "B19013_001E"]


# An API request takes parameters in key-value form. Python's uses dictionaries for key-value pairs, so the requests library uses this data structure. We define a dict `predicates`. We use this name because this is the name that the Census API documentation uses, but this name is arbitrary and can be changes. The `get` predicate takes the list of variables being requested. The `for` predicate takes the geographic level and identifier. `"state:*` means return the requested variables for *all* states. If you replace the `*` with a state FIPS identifier you will get a single state. For example `"state:13"` will return data only for Georgia.

# In[ ]:


# Build predicates dictionary
predicates = {}
predicates["get"] = ",".join(get_vars)
predicates["for"] = "state:*"


# Now we execute the request and store it in a response object, `r`. Examine the text of this response object.

# In[ ]:


# Execute request
r = requests.get(base_url, params=predicates)

# Examine response
print(r.text)


# The response isn't very useful until we put it in a data frame. We define a list of column names for the data frame, using more descriptive names than the Census variable names. I use a common database convention of all lower case names, with underscores in place of spaces. Remember the pandas does allow you to use names that are more like labels, with embedded spaces and proper capitalization.
# 
# We use the response objects `json` method to pass data to the data frame constructor. All the columns will be created as strings, so we use the `astype` method to convert the `median_household_income` column to type `int`.

# In[ ]:


# Build data frame
col_names = ["name", "median_household_income", "state"]
states1 = pd.DataFrame(columns = col_names, data = r.json()[1:])
states1["median_household_income"] = states1["median_household_income"].astype(int)


# Census API documentation is a little scattered. One useful source of information is to example the availabel geographies, variables, and examples for a specific Census data release. You can do this by appending a page name to the `base_url` for that product. Run the following code, then paste the URLs into your browser and look at the result.

# In[ ]:


# Viewing allowable geographies, variables, and examples
print(base_url + "/geography.html")
print(base_url + "/variables.html")
print(base_url + "/examples.html")


# # Requesting all variables from a particular table
# 
# You can request up to 50 variables in a single API request. You can provide these variable names as strings yourself, but a common need is to return all variables from a specific subject table. In this case, building the variable names programatically is easier. For example, Table B28003 "Presence Of A Computer And Type Of Internet Subscription In Household" has 6 columns. The variable names will all begin `"B28003_"` and the endings will run from `"001E"` to `"006E"`. We need a list of the numbers 1 through 6, converted to a string, with additional text added at the beginning and end.
# 
# Begin by constructing a list comprehension using `range(6)`

# In[ ]:


print([i for i in range(6)])


# Notice that his generates integers from 0 to 5, so add 1 to `i` and convert to a string.

# In[ ]:


print([str(i+1) for i in range(6)])


# This is looking good. But now we need those initial zeroes. If the number we are generating goes to two or three digits, the number of initial zeroes will be different. Fortunately Python provides the `zfill` method, that lets us zero-fill the string to the specified length. Since we want the column index to always have three characters, the correct parameter is 3.

# In[ ]:


print([str(i+1).zfill(3) for i in range(6)])


# Finally, we add the table name at the beginning and `"E"` for **estimate** at the end.

# In[ ]:


print(["B28003_" + str(i+1).zfill(3) + "E" for i in range(6)])


# Now that we have the string of variable names, we can request the data and construct a data frame as we did before.

# In[ ]:


get_vars = ["NAME"] + ["B28003_" + str(i+1).zfill(3) + "E" for i in range(6)]

predicates["get"] = ",".join(get_vars)

# Execute request
r = requests.get(base_url, params=predicates)

# Build data frame
col_names = ["name", "households", "computer", "computer_with_dialup", 
             "computer_with_broadband", "computer_no_internet",
             "no_computer", "state"]
states2 = pd.DataFrame(columns = col_names, data = r.json()[1:])


# In[ ]:


# Set column data types
int_cols = col_names[1:-1]
states2[int_cols] = states2[int_cols].astype(int)


# We now have two data frames with data by state. We can use `pd.merge` to join them. The 

# In[ ]:


# Join data frames
states = pd.merge(states1, states2, on = "state")
print(states.head())


# Note that the `name` column appears twice in the joined data frame. This code will drop `name` from one of the input data frames, so that it only appears once in the result.

# In[ ]:


states = pd.merge(states1, states2.drop(columns = "name"), on = "state")
print(states.head())


# # Requesting Different Geographies
# 
# So far we've been working with states data, but we can request many other geographies. The full list of available geographies for ACS 2017 can be viewed at https://api.census.gov/data/2017/acs/acs5/geography.html. Notice that summary level 050 is "state> county". This means that counties nest in states. You can therefore request all the counties *in* a particular state, using the `in` predicate to specify the state FIPS code. This uses the same format as the `for` predicate.
# 
# > NOTE: It is also acceptable to leave out the `in` predicate, in which case you will get all counties in the country. Which small geographies require the `in` predicate is not clear from the available geographies web page, and I don't know anywhere that this documented.

# In[ ]:


# Get data for counties
get_vars = ["NAME", "B19013_001E"]

predicates = {}
predicates["get"] = ",".join(get_vars)
predicates["for"] = "county:*"
predicates["in"] = "state:13"

r = requests.get(base_url, params=predicates)

# Examine the response
print(r.text)


# Now we'll try to request the same variables for block groups. Notice that we enter the geography exactly as it appears in the available geographies web page. `"block group"` is entered as lower case with a space in between the words. This will apply to other geographies as well, even if they have slashes or parentheses. For example `"metropolitan statistical area/micropolitan statistical area"` is an acceptable `for` or `in` predicate.

# In[ ]:


# Get data for block groups
predicates["for"] = "block group:*"
predicates["in"] = "state:13"

r = requests.get(base_url, params=predicates)

# Examine the response
print(r.text)


# Hmm. Something went wrong. This error message is somewhat generic, and can be produced for the following reasons:
# 
# 1. You have requested a geography that just does not exist (or maybe just misspelled it).
# 2. The geography is not available *via API* for that data product. For example block groups are available via API for recent ACS years, but not for earlier years, even though that data exists and can be downloaded from the Census in other ways.
# 3. You have requested a small geography that must be restricted to a specific containing geography. This is to prevent API calls that pull down too much data at once.
# 
# In this case, the reason is #3. Block groups must be requested in a specific county. Since block groups nest in tracts, you could also request block groups in a specific tract, but the API does not enforce this.
# 
# The following code requests block groups in Appling County (`001`), Georgia (`13`).

# In[ ]:


# Get data for block groups
predicates["for"] = "block group:*"
predicates["in"] = "state:13 county:001"

r = requests.get(base_url, params=predicates)

# Examine the response
print(r.text)


# # Concatenating Multiple API Requests
# 
# What if we want to get all of the block groups in Georgia? We will have to loop through all of the counties in Georgia, and create one request for each county.
# 
# We begin by requesting all the counties, just so that we have a list of county FIPS codes to iterate.

# In[ ]:


# Get data for all block groups in state
predicates["get"] = "NAME"
predicates["for"] = "county:*"
predicates["in"] = "state:13"

r = requests.get(base_url, params=predicates)

col_names = ["name", "state", "county"]
counties = pd.DataFrame(columns = col_names, data = r.json()[1:])
county_fips = list(counties["county"])
print(county_fips)


# Now we set up our API calls. Certain things will be the same on each call, including the `get` and `for` parameters, which indicate that we want the same variables for all block groups. The part that will vary is the containing county.
# 
# We also specify the column names of the data frames we will construct. Note that each level in the geographic hierarchy will be returned as a column.

# In[ ]:


get_vars = ["NAME", "B19013_001E"]
col_names = ["name", "median_household_income", "state", "county", "tract", "block_group"]

predicates = {}
predicates["get"] = ",".join(get_vars)
predicates["for"] = "block group:*"


# Now we're ready to construct our loop. Start by initializing `dfs` as an empty list. This is a **collector**, which will have data frames added to it on each pass through the loop.
# 
# We iterate the `county_fips` list. In this example, we use slicing to only step through the first three counties in the list, just so that this code doesn't take too long to run. You would normally interate the entire list. Feel free to try it out after the workshop.
# 
# On each pass through the list, a data frame `df` is built, and appended to `dfs`. Note that this is *not* the same as appending rows from one data frame to another. When you are done, `dfs` is a **list** which is a collection of separate data frames.

# In[ ]:


dfs = []
for fips in county_fips[0:3]:

    predicates["in"] = "state:13 county:{}".format(fips)
    
    r = requests.get(base_url, params=predicates)
    df = pd.DataFrame(columns=col_names, data=r.json()[1:])
    dfs.append(df)
    


# When you have a collection of data frames that have the same columns, you can use `pd.concat` to combine them into one data frame. We concatenate the data frames, then set the data type of the `median_household_income` column to `int`.

# In[ ]:


block_groups = pd.concat(dfs)
block_groups["median_household_income"] = block_groups["median_household_income"].astype(int)


# Finally, view the output. We drop the `name` column because the block group names are somewhat lengthy.

# In[ ]:


print(block_groups.drop(columns = "name").head())

