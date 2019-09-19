from workplace_data.models import Post
from ast import literal_eval
import json
import facebook
import time

token = {"DQVJ2SVdqcklvRTJfV2pjR3NuS05DVFRhZAmVlczNxMVBqZA1NwdWx0c2NPdDFnVmR0aXpYZAm4ySHBFT1Ywcjcyb25Ia09MZAFJIMWNOSWVaV085SlQ2TEF3UmN3dWQwX1JyNWVCajJxVHdIc2tBNVVFSUk0aS1yWjJZAclNNVjNpTDIzdVJrd3BMNXhfeVJvbVRXb2hfUGJhakgxZAzR1WHN0OEk0TTFHWEJOZA1ZAPYnVvS1VsMnN3NEtnLXVTTTNINlR4LUtYeXZAB"}
graph = facebook.GraphAPI(token,version='3.1')

class DataScrape:

    def __init__(self, email_address):
        self.email_address = email_address

    def get_details(self):
        employee_detail = graph.request('%s?fields=id,name,email,title,department&limit=9999999999' %self.email_address)
        return employee_detail

    def get_profile_picture(self):
        employee_detail = self.get_details()
        profile_picture = graph.request('%s/picture?type=large' %employee_detail['id'])['url']
        return profile_picture

    def get_id(self):
        employee_detail = self.get_details()
        try:
            user_id = employee_detail['id']
        except KeyError as e:
            user_id = 'No Id'
        return user_id

    def get_title(self):
        employee_detail = self.get_details()
        try:
            title = employee_detail['title']
        except KeyError as e:
            title = 'No Title'
        return title

    def get_department(self):
        employee_detail = self.get_details()
        try:
            department = employee_detail['department']
        except KeyError as e:
            department = 'No Department'
        return department

    def get_feed(self):
        feed = graph.request('%s?fields=feed&limit=9999999999' %self.email_address)
        try:
            feed = feed['feed']['data']
        except:
            print('No Feed')
        return feed

    def get_post_list(self):
        post_list = list()
        for i in self.get_feed():
            try:
                post_list.append(i['id'])
            except:
                print('No Post')
        return post_list

    def get_reactions_summary(self, post_id):
        reactions = graph.request('%s?fields=reactions&limit=99999999' %post_id)
        return reactions

    def get_reaction_received(self):
        start_time = time.time()
        print(start_time)
        reactions_dict = dict.fromkeys(['LIKE', 'LOVE', 'HAHA', 'WOW', 'SAD', 'ANGRY'], 0)

        for i in self.get_post_list():
            try:
                for j in self.get_reactions_summary(i)['reactions']['data']:
                    if j['type'] == 'LIKE':
                        reactions_dict['LIKE'] += 1
                        print("[INFO] Like received add ~ 1")
                    elif j['type'] == 'LOVE':
                        reactions_dict['LOVE'] += 1
                        print("[INFO] Love received add ~ 1")
                    elif j['type'] == 'HAHA':
                        reactions_dict['HAHA'] += 1
                        print("[INFO] Haha received add ~ 1")
                    elif j['type'] == 'WOW':
                        reactions_dict['WOW'] += 1
                        print("[INFO] Wow received add ~ 1")
                    elif j['type'] == 'SAD':
                        reactions_dict['SAD'] += 1
                        print("[INFO] Sad received add ~ 1")
                    else:
                        reactions[5] += 1
                        print("[INFO] Angry received add ~ 1")
                else:
                    print("[INFO] User's post have no any reactions")
            except KeyError as e:
                print('No reaction')
        print("--- %s seconds ---" % (time.time() - start_time))
        return reactions_dict


    def get_user_groups(self):
        group_list = []
        group = graph.request('%s?fields=groups&limit=999999999999' %self.email_address)
        group = group['groups']['data']

        for i in group:
            group_list.append(i['id'])

        return group_list


    def get_group_feed(self,group_id):
        group_post = graph.request('%s/feed?limit=9999999999' %group_id)

        try:
            group_post = group_post['data']
        except:
            print('[INFO] User is not belong to group '+group_id)
        return group_post


    def get_group_post_list(self):
        group_post_list = []
        for i in (self.get_user_groups()):
            for j in (self.get_group_feed(i)):
                try:
                    group_post_list.append(j['id'])
                except:
                    print('No id')
        return group_post_list

    def get_reaction_given(self, user_id):
        total_reactions = 0
        total_posts = 0
        reactions_dict = dict.fromkeys(['LIKE', 'LOVE', 'HAHA', 'WOW', 'SAD', 'ANGRY'], 0)
        for post in Post.objects.all():
            total_posts += 1
            reaction_summary = literal_eval(post.reactions)
            for key, val in reaction_summary.items():
                if key == user_id:
                    total_reactions += 1
                    reactions_dict[val] += 1

        print("[INFO] %s has %d reactions from %d posts" %(self.email_address, total_reactions, total_posts))
        return reactions_dict