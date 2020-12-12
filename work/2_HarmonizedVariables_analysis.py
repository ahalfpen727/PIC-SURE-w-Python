#!/usr/bin/env python
# coding: utf-8

# # Accessing BioData Catalyst Harmonized variables using python PIC-SURE API

# This tutorial notebook will demonstrate how to query and work with the BioData Catalyst cross-studies harmonized variables using python PIC-SURE API. For a more step-by-step introduction to the python PIC-SURE API, see the `PICSURE-API_101.ipynb` notebook.

# **Before running this notebook, please be sure to get a user-specific security token. For more information about how to proceed, see the `get_your_token.ipynb` notebook**

#  -------   

# # Environment set-up

# ### System requirements
# - Python 3.6 or later
# - pip package manager
# - bash interpreter

# ### Installation of external dependencies

# In[1]:


import sys
get_ipython().system('{sys.executable} -m pip install -r requirements.txt')


# In[ ]:


get_ipython().system('{sys.executable} -m pip install --upgrade --force-reinstall git+https://github.com/hms-dbmi/pic-sure-python-adapter-hpds.git')
get_ipython().system('{sys.executable} -m pip install --upgrade --force-reinstall git+https://github.com/hms-dbmi/pic-sure-python-client.git')


# In[9]:


import json
from pprint import pprint

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from scipy import stats

import PicSureHpdsLib
import PicSureClient

from python_lib.utils import get_multiIndex_variablesDict, joining_variablesDict_onCol


# In[10]:


print("NB: This Jupyter Notebook has been written using PIC-SURE API following versions:\n- PicSureHpdsLib: 1.1.0\n- PicSureClient: 1.1.0")
print("The installed PIC-SURE API libraries versions:\n- PicSureHpdsLib: {0}\n- PicSureClient: {1}".format(PicSureHpdsLib.__version__, PicSureClient.__version__))


# ## Connecting to a PIC-SURE network

# In[11]:


PICSURE_network_URL = "https://picsure.biodatacatalyst.nhlbi.nih.gov/picsure"
resource_id = "02e23f52-f354-4e8b-992c-d37c8b9ba140"
token_file = "token.txt"


# In[12]:


with open(token_file, "r") as f:
    my_token = f.read()


# In[13]:


client = PicSureClient.Client()
connection = client.connect(PICSURE_network_URL, my_token)
adapter = PicSureHpdsLib.Adapter(connection)
resource = adapter.useResource(resource_id)


# ## Harmonized Variables

# Data Harmonization effort aims at producing "a high quality, lasting resource of publicly available and thoroughly documented harmonized phenotype variables". The TOPMed Data Coordinating Center collaborates with Working Group members and phenotype experts on this endeavour. So far, 44 harmonized variables are accessible through PICS-SURE API (as well as, for each variable, the age at which the variable value as been collected for a given subject).
# 
# Which phenotypes caracteristics are included the harmonized variables?
# 
# - Key NHLBI phenotypes    
#     - Blood cell counts
#     - VTE
#     - Atherosclerosis-related phenotypes
#     - Lipids
#     - Blood pressure
# 􏰀
# - Common covariates
#     - Height
#     - Weight
#     - BMI
#     - Smoking status
#     - Race/ethnicity
# 
# More information about the variables harmonization process is available at https://www.nhlbiwgs.org/sites/default/files/pheno_harmonization_guidelines.pdf

# ### 1. Retrieving variables dictionary from HPDS Database

# Here we retrieve the harmonized variables information by searching for the "harmonized" keyword.

# In[8]:


dis = resource.dictionary().find("disease").DataFrame()


# In[ ]:


pd.set_option("display.max.rows", 50)


# In[ ]:


get_ipython().run_cell_magic('capture', '', 'multiIndexdic = get_multiIndex_variablesDict(harmonized_dic)\nmultiIndexdic_sub = multiIndexdic.loc[~ multiIndexdic["simplified_name"].str.contains("(^[Aa]ge)|(SUBJECT_ID)", regex=True),:]')


# In[ ]:


multiIndexdic = get_multiIndex_variablesDict(harmonized_dic)
multiIndexdic_sub = multiIndexdic.loc[~ multiIndexdic["simplified_name"].str.contains("(^[Aa]ge)|(SUBJECT_ID)", regex=True),:]
multiIndexdic_sub.shape


# Overall, there is 82 harmonized variables. After discarding "subject ID" and the variables only indicating age of the subject at which a given harmonized variable has been measured, there is 43 left.

# In[ ]:


multiIndexdic_sub


# ### 2. Selecting variables and retrieving data from the database

# Let's say we are interested in the subset of Harmonized Variables pertaining to the demographics. 
# 
# Subseting to keep only the phenotypical variables + the "affection status", that will be used as the dependent variable for this illustration use-case.

# In[ ]:


mask_demo = multiIndexdic_sub.index.get_level_values(1) == '01 - Demographics'
variablesDict = multiIndexdic_sub.loc[mask_demo,:]


# In[ ]:


selected_vars = variablesDict.loc[:, "name"].tolist()
#selected_vars.append("\\_Consents\\Short Study Accession with Consent Code\\")


# In[ ]:


pprint(selected_vars[:5])


# Retrieving the data:

# In[ ]:


query = resource.query()
query.select().add(selected_vars)
facts = query.getResultsDataFrame(low_memory=False)


# In[ ]:


facts = facts.set_index("Patient ID")    .dropna(axis=0, how="all")    .drop(["\\_Consents\\Short Study Accession with Consent Code\\"], axis=1)
#facts.columns = variablesDict.set_index("name").loc[selected_vars, "simplified_name"]


# ## Studying the Sex Repartition Across Studies

# In[ ]:


sex_varname = "Subject sex  as recorded by the study."
study_varname = "A distinct subgroup within a study  generally indicating subjects who share similar characteristics due to study design. Subjects may belong to only one subcohort."
race_varname = "Harmonized race category of participant."


# In[ ]:


import matplotlib.patches as mpatches
from matplotlib import cm
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage,
                                  AnnotationBbox)


# In[ ]:


plt.rcParams["figure.figsize"] = (14,8)
font = {'weight' : 'bold',
        'size'   : 12}
plt.rc('font', **font)


# In[ ]:


facts.head()


# In[ ]:


subset_facts = facts.loc[pd.notnull(facts[sex_varname]),:]
ratio_df = subset_facts.groupby(study_varname)[sex_varname].apply(lambda x: pd.value_counts(x)/(np.sum(pd.notnull(x)))).unstack(1)
annotation_x_position = ratio_df.apply(np.max, axis=1)
number_subjects = subset_facts.groupby(study_varname)[sex_varname].apply(lambda x: x.notnull().sum())
annotation_gen = list(zip(number_subjects, annotation_x_position))

fig = ratio_df.plot.barh(title="Subjects sex-ratio across studies", figsize=(10, 12))
fig.legend(bbox_to_anchor=(1, 0.5))
fig.set_xlim(0, 1.15)
fig.set_ylabel(None)

for n, p in enumerate(fig.patches[:27]):
    nb_subject, x_position = annotation_gen[n]
    fig.annotate(nb_subject, (x_position + 0.03, p.get_y()+0.1), bbox=dict(facecolor='none',
                                                                       edgecolor='black',
                                                                       boxstyle='round'))

handles, labels = fig.get_legend_handles_labels()
red_patch = mpatches.Patch(label='Study nb subjects', edgecolor="black", facecolor="white")
handles.append(red_patch)
fig.legend(handles=handles)


# In[ ]:




