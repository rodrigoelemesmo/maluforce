# Description
This module contains an extension of simple-salesforce Salesforce class (https://github.com/simple-salesforce/) and utility functions that help you manage files and reports in large scales.

# Reference

This module's main data structre is a "list of dict" e.g. "lod": [{'a':1},{'a':2}], which is the accepted format by salesforce. 

# Installation
```
pip install maluforce
```

For edit mode installation, n parent directory:
```
git clone git@github.com:stone-payments/maluforce
pip3 install -e maluforce
```
For global installation:
```
pip3 install git+https://github.com/stone-payments/maluforce.git
```
For ubuntu: 
```
python3 -m pip install git+ssh://git@github.com/stone-payments/maluforce.git --user
```
To install it as a package on your project:
- clone the git repo
- delete .git and .gitgnore files
- install with `pipenv install -e maluforce`

# Usage

## Authenticate
```
from maluforce import *
sf = Maluforce(username='', password='', security_token='', sandbox=False)
```

## Query

### Query as usual:
```
lod_users = sf.query_salesforce('User',"select id from user limit 10")
```

### Query for a list of of e-mails using `format`:
```
l_emails = ['rodrigo@gmail.com','rodrigo2@gmail.com'] 
soql = "select id, email from user where email in ('{}')".format("','".join(l_emails))
lod_users = sf.query_salesforce('User',soql))
```

### Parsing to a dataframe:
```
import pandas as pd
df_users = pd.DataFrame(lod_users)
```

## DML

### insert
- don't pass and `Id` or you will get an error.

```
lod_users = [{'LastName': 'Poto','Email': 'ctrcctrlv@gmail.com'},{'LastName': 'Poto2','Email': '2ctrcctrlv@gmail.com'}]

lod_resp = sf_live.lod_to_saleforce('user','insert',lod_users)
```

### delete/ update
- only required field is the `Id`

## Report Utilities

### to_lod
Parses a `pandas.DataFrame` to a `lod`. You can specify which columns from the dataframe tou want to mantain, and rename them.

```
df_permissionset
```

|AssigneeId | AssigneeName |	Id | PermissionSetId |
|---|---|---|---|
|00541000004OVfCAAW | Leonardo |	0Pa1L000007L0flSAC | 0PS410000026AhIGAU |	
|00541000004Om8jAAC | Oliveira |	0Pa1L000007L0fmSAC | 0PS410000026AhIGAU |	
|005410000035wnXAAQ | Paulo | 0Pa1L000007L0fnSAC	| 0PS410000026AhIGAU |	
|00541000004OvYEAA0 | Lucas | 0Pa1L000007L0foSAC	| 0PS410000026AhIGAU |	
|005410000065T1AAAU | Brizolla |	0Pa1L000007L0fpSAC | 0PS410000026AhIGAU |	

```
to_lod(df_permissionset,key_map={"AssigneeId","UserId"},drop=True)
```

results:

```
[{'UserId': '00541000004OVfCAAW'},
 {'UserId': '00541000004Om8jAAC'},
 {'UserId': '005410000035wnXAAQ'},
 {'UserId': '00541000004OvYEAA0'},
 {'UserId': '005410000065T1AAAU'},
 {'UserId': '00541000004MpidAAC'}]
```

## Other functions
```
from maluforce import adjust_report,lod_rename,to_lod
```
### adjust_report
Parses a Salesforce response object into a pandas.DataFrame

### lod_rename
Renames a lod

## Files Utilities
```
from maluforce import save_lod_files,read_lod_file,read_lod_files
```
Used for storing large files into small chunks, so that Salesforce's api character limits are respected. 
