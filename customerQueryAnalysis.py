##Bernard Adabankah
## June 2016

import pymysql
from pandas import DataFrame
import seaborn as sns
import matplotlib.pyplot as plt



#define a glabal dataframe variable to contain our database result query
df_hesk_kb_articles = DataFrame

#connect to MySql database on server
print("Connecting to Mysql Database....")

'''
Connect to the database
put in a try and except block to catch any  problems
'''
Connection = pymysql.connect(host='@dbhostname', user='@dbuser', password='@dbpassword', 
                 db='siradaba_hesk',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor )
try:
                
    #ExecuteQuery(Connection)
    print("Connected to Mysql Database....")
    
    #create cursur to query the database
    cursor = Connection.cursor()
    
    #check all the tables in the database
    cursor.execute("SHOW tables in siradaba_hesk")
    
    #get names of tables into table_names variable
    table_names= cursor.fetchall()
    
    #get only customer queries templates which has been used 10 or more times
    cursor.execute("SELECT * FROM hesk_kb_articles WHERE views >= 10")
    
    #get all those customer query templates
    df_hesk_kb_articles = DataFrame(cursor.fetchall())
except Exception as e:
    print("Check your code for issue ", e)
finally:
    #mop up
    #close connection and reserve resources when done querying the databasel
    Connection.close()
    
    

#Connection.close()

#check the colums in the df_hesk_kb_articles
df_hesk_kb_articles.columns


#Get only dates, query template subjects and number of times used (represented as views)
articles_by_date = df_hesk_kb_articles[['dt','subject','views']]


##lets group by query template subject
articles_by_date = articles_by_date.groupby('subject')
articles_by_date.size()


#sum up all views(number of times template has been used) by subject
totals_by_query = articles_by_date.sum()
totals_by_query.sort(columns='views').head()


#create bar chart with to views(number of times template has been used) 
my_plot = totals_by_query.plot(kind='bar')

'''
let's clean up graph to make it look a bit neater
'''

my_plot = totals_by_query.sort(columns="views", ascending=False).plot(kind="bar", \
 legend=None, title = "Customer Queries")
my_plot.set_xlabel("Query Subject")
my_plot.set_ylabel("Total Number of Queries")


'''
examine customer query patterns
'''
query_patterns = df_hesk_kb_articles[['dt','views']]
query_patterns.head()


'''
histogram with 15 bins to show views pattern
'''
views_plot = query_patterns['views'].hist(bins=15)
views_plot.set_title("Query patterns")
views_plot.set_xlabel("Total Queries")
views_plot.set_ylabel("Number of times")

'''
a look at the data show most of the queries were asked less than 30 times with
few over 50 and 60

Let’s get the data down to order size and date.
If we want to analyze the data by date, we need to set the date column as the 
index using set_index 
'''
query_patterns = query_patterns.set_index("dt")
query_patterns.head()

'''
view data by month  using value "M", view by week using "W"
'''

query_patterns.resample('M', how=sum)

#plot
query_plot = query_patterns.resample('M', how=sum).plot(title="Total Queries by Month", legend=None)

'''
Looking at the chart, and we knowing from our previous graphs that the higest number of 
queries is less than 70 we can now see there might be issue with the data for  June
hence our peak month is December
data not avaivable sept, oct, nov yet
'''
fig = query_plot.get_figure()
fig.savefig("CustomerQueries.png")
