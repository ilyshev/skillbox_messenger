#!/usr/bin/env python
# coding: utf-8

# In[7]:


fname = 'ДЗ1.csv'

import csv

with open(fname) as f:
    reader = csv.DictReader(f)
    print(reader.fieldnames)
    lines = list(reader)

codes = [l['Код '] for l in lines]
print(len(codes))


# In[8]:


config_codes = []

for code in codes:
    if 'BOT_CONFIG =' in code:
        code = code.split('BOT_CONFIG =')[1]
    if 'def ' in code:
        code = code.split('def ')[0]

    code = code.strip()

    config_codes.append(code)

print(len(config_codes))


# In[9]:


# print(config_codes[4])


# In[10]:


try:
    response = eval("{'a': 'b'}")
    type(response)
except:
    print(1)


# In[11]:


configs = []
errors = 0
for code in config_codes:
    try:
        configs.append(eval(code))
    except Exception as e:
#         print(code)
#         print('-' * 30)
#         print(e)
#         print('-' * 100)
        errors += 1


# In[12]:


print(f'{errors} errors ({errors / len(config_codes) * 100:.2f}%)')
print(len(configs), 'configs')


# In[13]:


big_config = {
    'intents': {},
    'failure_phrases': []
}

for config in configs:
    if isinstance(config, dict):
        if 'intents' in config:
            for intent, value in config['intents'].items():
                if intent not in big_config['intents']:
                    big_config['intents'][intent] = {
                        'examples': [],
                        'responses': []
                    }
                if isinstance(value, dict):
                    big_config['intents'][intent]['examples'] += value.get('examples', [])
                    big_config['intents'][intent]['responses'] += value.get('responses', [])
        big_config['failure_phrases'] += config.get('failure_phrases', [])


# In[14]:


for intent, value in big_config['intents'].items():
    value['examples'] = list(set(value['examples']))
    value['responses'] = list(set(value['responses']))
    value['examples'] = [s.strip() for s in value['examples'] if s.strip()]
    value['responses'] = [s.strip() for s in value['responses'] if s.strip()]

big_config['failure_phrases'] = list(set(big_config['failure_phrases']))
big_config['failure_phrases'] = [s.strip() for s in big_config['failure_phrases'] if s.strip()]


# In[15]:


big_config


# In[16]:


# намерений
print(len(big_config['intents']))


# In[17]:


# примеров
print(sum(len(intent_data['examples']) for intent_data in big_config['intents'].values()))


# In[18]:


# ответов
print(sum(len(intent_data['responses']) for intent_data in big_config['intents'].values()))


# In[19]:


# заглушек
print(len(big_config['failure_phrases']))


# In[20]:


print(big_config)


# In[ ]:




