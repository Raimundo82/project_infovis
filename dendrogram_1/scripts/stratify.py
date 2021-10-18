import pandas as pd

def filterColumns(df, cols_to_maintain):
    cols_to_remove = [*df.columns]
    for c in cols_to_maintain:
        cols_to_remove.remove(c)    
    df.drop(cols_to_remove, axis=1,inplace=True)

def filterRows(df, column, values):
    for v in values:
        df = df[df[column] != v]
    return df

df = pd.read_csv("data/input/DBP_wiki_data.csv", delimiter=",",  na_values=['..', " ", None])

df.dropna(
    #axis=0, # 0 => rows ; 1 => columns
    #how='any', # any => drop if any; all => drop only if all
    #subset=[], # if axis=1 =>  columns names to dropna; axis=0 => the indices of the rows tp dropna
    inplace=True
)

filterColumns(df, ["l1","l2","l3"])

df = filterRows(df, "l1", ['Agent', 'Device', 'Event'])

fpair = df.drop(['l3'], axis=1)

fpair = fpair.groupby(by=["l1","l2"], as_index=False).count()

fpair.rename({'l1':'parent', 'l2':'child'}, axis=1, inplace=True)

for p in fpair.parent.unique():
    fpair = fpair.append({'child':p, 'parent':'root'}, ignore_index=True)

fpair = fpair.append({'child':'root'}, ignore_index=True)

spair = df.drop(['l1'], axis=1)

spair = spair.groupby(by=["l2","l3"], as_index=False).count()

spair.rename({'l2':'parent', 'l3':'child'}, axis=1, inplace=True)

fpair = fpair.append(spair)


fpair.to_csv("data/output/h_data.csv", index=False)