import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
from jupyter_dash import JupyterDash
from dash import dcc, dash_table
from dash import html
from dash.dependencies import Input, Output


# For this lab, we will be working with the 2019 General Social Survey one last time.

%%capture
gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])


# In[3]:


# Here is code that cleans the data and gets it ready to be used for data visualizations:

# In[4]:


mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')

# ## Problem 2
# Generate a table that shows the mean income, occupational prestige, socioeconomic index, and years of education for men and for women. Use a function from a `plotly` module to display a web-enabled version of this table. This table is for presentation purposes, so round every column to two decimal places and use more presentable column names. [3 points]

# In[5]:


table = gss_clean.groupby('sex').agg({'income':'mean', 'job_prestige':'mean', 'socioeconomic_index':'mean',
                       'education':'mean'}).round(2).rename(columns={'income': 'Mean_Income',
                                                                    'job_prestige': 'Mean_Occupational_Prestige',
                                                                    'socioeconomic_index': 'Mean_Socioeconomic_Index',
                                                                    'education': 'Mean_Years_of_Education'}).reset_index()


# In[6]:


table=ff.create_table(table)


# ## Problem 3
# Create an interactive barplot that shows the number of men and women who respond with each level of agreement to `male_breadwinner`. Write presentable labels for the x and y-axes, but don't bother with a title because we will be using a subtitle on the dashboard for this graphic. [3 points]

# In[7]:


gss_groupbar = pd.crosstab(gss_clean.sex, gss_clean.male_breadwinner).reset_index()
gss_groupbar = pd.melt(gss_groupbar, id_vars = 'sex', value_vars = ['strongly agree', 'agree', 'disagree', 'strongly disagree'])


# In[8]:


fig_bar= px.bar(gss_groupbar, x='male_breadwinner', y='value', color='sex',
       labels={'value':'Number of Respondents', 'male_breadwinner':'Response'}, barmode = 'group')



# ## Problem 4
# Create an interactive scatterplot with `job_prestige` on the x-axis and `income` on the y-axis. Color code the points by `sex` and make sure that the figure includes a legend for these colors. Also include two best-fit lines, one for men and one for women. Finally, include hover data that shows us the values of `education` and `socioeconomic_index` for any point the mouse hovers over. Write presentable labels for the x and y-axes, but don't bother with a title because we will be using a subtitle on the dashboard for this graphic. [3 points]

# In[9]:


fig_line = px.scatter(gss_clean, x='job_prestige', y='income', color='sex', trendline='ols', opacity=0.4,
                 height=600, width=600,
                 labels={'job_prestige':'Job Prestige Rating',
                        'income':'Personal Income'},
                 hover_data=['education', 'socioeconomic_index'])
fig_line.update(layout=dict(title=dict(x=0.5)))


# ## Problem 5
# Create two interactive box plots: one that shows the distribution of `income` for men and for women, and one that shows the distribution of `job_prestige` for men and for women. Write presentable labels for the axis that contains `income` or `job_prestige` and remove the label for `sex`. Also, turn off the legend. Don't bother with titles because we will be using subtitles on the dashboard for these graphics. [3 points]

# In[10]:


fig_box1 = px.box(gss_clean, x='income', y = 'sex', color = 'sex',
                   labels={'income':'Personal Income', 'sex':''}
                   )
fig_box1.update(layout=dict(title=dict(x=0.5)))
fig_box1.update_layout(showlegend=False)


# In[11]:


fig_box2 = px.box(gss_clean, x='job_prestige', y = 'sex', color = 'sex',
                   labels={'job_prestige':'Job Prestige', 'sex':''}
                   )
fig_box2.update(layout=dict(title=dict(x=0.5)))
fig_box2.update_layout(showlegend=False)


# ## Problem 6
# Create a new dataframe that contains only `income`, `sex`, and `job_prestige`. Then create a new feature in this dataframe that breaks `job_prestige` into six categories with equally sized ranges. Finally, drop all rows with any missing values in this dataframe.
# 
# Then create a facet grid with three rows and two columns in which each cell contains an interactive box plot comparing the income distributions of men and women for each of these new categories. 
# 
# (If you want men to be represented by blue and women by red, you can include `color_discrete_map = {'male':'blue', 'female':'red'}` in your plotting function. Or use different colors if you want!) [3 points]

# In[12]:


cols = ['sex', 'income', 'job_prestige']

new_gss = gss_clean[cols]

new_gss = new_gss.loc[~new_gss.income.isna()]
new_gss = new_gss.loc[~new_gss.job_prestige.isna()]
new_gss = new_gss.loc[~new_gss.sex.isna()]


new_gss['job_prestige'].min()
new_gss['job_prestige'].max()

80-16

64/6

new_gss['job_prestige'] = pd.cut(new_gss['job_prestige'],
                   [16, 80/3, 112/3, 144/3,176/3, 208/3, 240/3],
                   labels=['Very Low', 'Low', 'Average', 'Slightly Above Average', 'Above Average', 'High'])

new_gss = new_gss.loc[~new_gss.job_prestige.isna()]


# In[13]:


fig = px.box(new_gss, x='income', y = 'sex', color = 'sex',
             facet_col='job_prestige', facet_col_wrap=2, 
             color_discrete_map = {'male':'blue', 'female':'red'})
fig.update(layout=dict(title=dict(x=0.5)))
fig.update_layout(showlegend=False)
fig.for_each_annotation(lambda a: a.update(text=a.text.replace("job_prestige=", "")))


# ## Problem 7
# Create a dashboard that displays the following elements:
# 
# * A descriptive title
# 
# * The markdown text you wrote in problem 1
# 
# * The table you made in problem 2
# 
# * The barplot you made in problem 3
# 
# * The scatterplot you made in problem 4
# 
# * The two boxplots you made in problem 5 side-by-side
# 
# * The faceted boxplots you made in problem 6
# 
# * Subtitles for all of the above elements
# 
# Use `JupyterDash` to display this dashboard directly in your Jupyter notebook.
# 
# Any working dashboard that displays all of the above elements will receive full credit. [4 points]

# In[14]:


markdown_text = '''
The gender wage gap has been a point of contention for years. Some suggest the issue is overblown, other say the media is overstating the issue, and still other claim that the gender wage gap is a myth that does not exist at all. According to Americanprogress.org, a woman earns 82 cents for every dollar a man makes. "This calculation is the ratio of median annual earnings for women working full time, year round to those of their male counterparts." (Americanprogress.org). There are many factors that compound the wage gap issue. Two large reasons the wage gap persists is employers basing salaries off a worker's prior job history as well as prohibiting employees from discussing their wages (aauw.org).

The General Social Survey (GSS) is a national survey of adults in the United States that tries to monitor and explain opinions, attitudes, and behaviors in American society. The data provided to us to answer this question contains 2348 responses on questions discussing job presitge, job satisfaction, and who the breadwinner of the household is. The GSS website contains a large FAQ section discussing how they obtained the data in the survey, which can be found here: https://gss.norc.org/faq. The test is admistered twice a year in even years to about 1500 people, meaning about 3000 people participate in the survey every other year. Not every question is asked to every respondent in the data.
'''


# In[ ]:


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

graphlist = [fig_bar, fig_line, fig_box1, fig_box2, fig]

for x in graphlist:
    x.update_layout(
        plot_bgcolor='#87CEFA',
        paper_bgcolor='#6495ED',
        font_color = '#DA70D6')

app.layout = html.Div(
    [
        html.H1("General Social Survey Dashboard"),
        dcc.Markdown(children = markdown_text),
        html.H2("Mean Income, occupational Prestige, Socioeconomic Index, and Years of Education by Sex"),
        dcc.Graph(figure=table),
        html.H2("Number of Men and Women's level of agreement to a Question about Male Breadwinners"),
        dcc.Graph(figure=fig_bar),
        html.H2("Income Against Job Prestige by Sex"),
        dcc.Graph(figure=fig_line),

        html.Div([

            html.H2("Personal Income by Sex"),

            dcc.Graph(figure=fig_box1)

        ], style = {'width':'48%', 'float':'left'}),

        html.Div([

            html.H2("Job Prestige by Sex"),

            dcc.Graph(figure=fig_box2)]

            , style = {'width':'48%', 'float':'right'}),

        html.H2("Income by Sex, Grouped by Job Prestige Range"),
        dcc.Graph(figure=fig),

    ],
    style={'backgroundColor' :'#87CEFA', 'color':'#DA70D6', 'padding' : 10}
)

if __name__ == '__main__':
    app.run_server(debug=True,
                   use_reloader=False,
                   port=8050)





