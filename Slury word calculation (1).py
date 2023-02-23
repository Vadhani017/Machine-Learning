#!/usr/bin/env python
# coding: utf-8

# # Degree of profanity 

# ## Problem Statement: Calculating the degrees of profanity using tweets from twitter. 

# Consider that we have a list of racial slurs words, (i.e., the words that are considered to be offensive or profane). And the twitter file name is "file_name.txt". 

# ### Assumptions:
# 
# 1. The file containing the Twitter tweets is a text file, with one tweet per line.
# 
# 2. The set of words indicating racial slurs is provided as a Python set.
# 
# 3. The degree of profanity for each sentence will be represented by a number between 0 and 1, with 0 indicating no profanity and 1 indicating maximum profanity.
# 
# 

# ### Here is the needed coding

# Importing re (Regular expressions) to find those words. This will be used later to split the sentences into words.

# In[1]:


import re


# Below is the list of slurry words (instead of list, we can also store in tuples.)

# In[4]:


racial_slurs = {"slur_word1", "slur_word2", "slur_word3", "slur_word4",...}


# Here is the definition of the function which will calculate the profanity.

# In[9]:


def calculate_profanity(sentence):
    
    words = re.findall(r'\w+', sentence.lower())
    # splitting the words
    num_slurs = sum(1 for word in words if word in racial_slurs)
    return num_slurs / len(words)
    # counting the number slur words which present in the above list and returning the degree of profanity. 


# Calculating formula:
#         Degree of profanity = number of slurs / Total number of words in the file or line

# Opening the text file. Instead of file_name.txt, give the original file name with text format. 

# In[ ]:


with open("file_name.txt", "r") as f:


# Calculating the profanity line by line

# In[ ]:


for line in f:
    profanity = calculate_profanity(line)
    print(line.strip(), profanity)


# Line strip is used to avoid the unnecessary space and displaying the line's profanity.
