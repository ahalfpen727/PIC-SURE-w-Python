#!/usr/bin/env python
# coding: utf-8

# ## Import the needed libraries

# In[1]:


import PicSureHpdsLib
import pandas
import matplotlib


# ## Create an instance of the datasource adapter and get a reference to the data resource 

# In[2]:


adapter = PicSureHpdsLib.BypassAdapter("http://pic-sure-hpds-nhanes:8080/PIC-SURE")
resource = adapter.useResource()


# ## Get a listing of all "demographics" entries in the data dictionary. Show what actions can be done with the "demographic_results" object

# In[3]:


demographic_entries = resource.dictionary().find("\\demographics\\disease")
demographic_entries.help()
demographic_entries.DataFrame()


# ## Examine the demographic_entries results by converting it into a pandas DataFrame

# In[4]:


demographic_entries.DataFrame()


# In[5]:


resource.query().help()


# In[6]:


resource.query().filter().help()


# In[7]:





# In[1]:





# ## Convert the query results for females into a DataFrame and plot it by BMI and Age

# In[11]:


df_f = query_female.getResultsDataFrame()
plot_f = df_f.plot.scatter(x="\\demographics\\AGE\\", y="\\examination\\body measures\\Body Mass Index (kg per m**2)\\", c="#ffbabb40")

# ____ Uncomment if graphs are not displaying ____
#plot_f.plot()
#matplotlib.pyplot.show()


# ## Convert the query results for males into a DataFrame and plot it by BMI and Age

# In[10]:


df_m = query_male.getResultsDataFrame()
plot_m = df_m.plot.scatter(x="\\demographics\\AGE\\", y="\\examination\\body measures\\Body Mass Index (kg per m**2)\\", c="#5a7dd040")

# ____ Uncomment if graphs are not displaying ____
#plot_m.plot()
#matplotlib.pyplot.show()


# ## Replot the results using a single DataFrame containing both male and female

# In[12]:


d = resource.dictionary()
criteria = []
criteria.extend(d.find("\\disease\\").keys())
criteria.extend(d.find("\\Body Mass Index").keys())
criteria.extend(d.find("\\AGE\\").keys())

query_unified = resource.query()
query_unified.require().add(criteria)
df_mf = query_unified.getResultsDataFrame()

# map a color field for the plot to use
sex_colors = {'male':'#5a7dd040', 'female':'#ffbabb40'}
df_mf['\\sex_color\\'] = df_mf['\\demographics\\SEX\\'].map(sex_colors)


# plot data
plot_mf = df_mf.plot.scatter(x="\\demographics\\AGE\\", y="\\examination\\body measures\\Body Mass Index (kg per m**2)\\", c=df_mf['\\sex_color\\'])

# ____ Uncomment if graphs are not displaying ____
#plot_mf.plot()
#matplotlib.pyplot.show()


# ## Replot data but trim outliers

# In[13]:


q = df_mf["\\examination\\body measures\\Body Mass Index (kg per m**2)\\"].quantile(0.9999)

# create a masked array to remove outliers
test = df_mf.mask(df_mf["\\examination\\body measures\\Body Mass Index (kg per m**2)\\"] > q)

# plot data
plot_mf = test.plot.scatter(x="\\demographics\\AGE\\", y="\\examination\\body measures\\Body Mass Index (kg per m**2)\\", c=df_mf['\\sex_color\\'])

# ____ Uncomment if graphs are not displaying ____
#plot_mf.plot()
#matplotlib.pyplot.show()


# In[ ]:




