import tushare as tus
import pandas as pd
from pandas import DataFrame
import numpy as np
import datetime
import seaborn as sns
import time

code_list=['000001','399001','399005','399006','000016','000300','000905']
code_name=['上证综指','深证成指','中小板指','创业板指','上证50','沪深300','中证500']
def get_index_data(code_list=code_list):
    n=len(code_list)
    data_list=[0 for i in range(n)]
    now=str(datetime.date.today())
    k=0
    for code_id in code_list:
        table=tus.get_k_data(code=code_id,start='2014-01-01',end='2017-06-16',index=True,ktype='D')
        data=np.array(table['close'])
        data_list[k]=np.log([data[i]/data[i-1] for i in range(1,len(data))])
        k+=1
    data_array=np.array(data_list).reshape(n,-1)
    data_frame=DataFrame(data_array,index=code_list).T
    date_s=table['date']
    date_t=DataFrame(date_s.ix[1:])
    date_r=DataFrame.reset_index(date_t)
    date_r=date_r.drop('index',axis=1)
    data_frame=pd.concat([date_r,data_frame],axis=1)
    # 真是费了半天劲才拼好！！
    return data_frame
# index_data=get_index_data()
# DataFrame.to_csv(index_data,'index.csv',index=0)
index_data=pd.read_csv('index.csv',index_col='date')
data_before=index_data.loc[:'2016-02-22']
data_after=index_data.loc['2016-02-22':]
before_describe=data_before.describe()
after_describe=data_after.describe()
DataFrame.to_csv(before_describe,path_or_buf='before.csv',index=0)
DataFrame.to_csv(after_describe,path_or_buf='after.csv',index=0)

for code_id in code_list:
    DataFrame.to_csv(pd.concat([before_describe[['%s' %code_id]],after_describe[['%s' %code_id]]],axis=1)\
                     ,path_or_buf='%s.csv' %code_id)
    data_array=np.array(index_data['%s' %code_id])
    sns.plt.plot(data_array,label='%s' %code_id)
    # sns.plt.ylim([-0.03,0.03])
    sns.plt.legend(loc="best")
    sns.plt.title('%s' %code_id)
    sns.plt.savefig("pictures/%s.png" %code_id)
    time.sleep(0.5)
    sns.plt.close()
