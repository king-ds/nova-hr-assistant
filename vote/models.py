from django.db import models
from gmail_authentication.models import *

class Votes(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    votes = models.IntegerField()
    comment = models.TextField()
    datetime_voted = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return str(self.datetime_voted)


# scratch



    # frame = pd.DataFrame(dept_name_list)
    # frame.columns = ['Department']
    # frame['Votes'] = act_vote_list
    # frame = pd.pivot_table(index='Department',values='Votes',aggfunc=np.mean,data=frame).reset_index()
    # frame['Votes'] = frame['Votes'].apply(math.ceil)
    # print(frame)
    # context = locals()
    # source = frame
    #
    # chart =  alt.Chart(source).mark_bar().encode(
    # x=alt.X('Votes:Q',axis=alt.Axis(values=[1,2,3,4])),
    # color= alt.Color('Votes:O', scale=alt.Scale(domain=[1,2,3,4],range=['red','lightred','orange','lightgreen'])),
    # row='Department:N'
    # ).properties(
    #     height = 50,
    #     width = 1150
    #     )
