import facebook
import time

token = {"DQVJ0OGdHUlFsalNqRTR2YkNydDZAGTVdCRF81eGQyLXJKMlJ2djdzSFVzbDVSX210cjVQeDE1TU5uTGJadG1ZAejVERmdTQ0Q4TFpuS2dCa2RROWQwOFdPZA0pVdzRjV3llVFN4VXFpYXlNdmZAyNjItVmZAnTVpVVWVmczdZAMnRhY3hUWFFZAeENQc1V6X3dtNzFaT2RuaThZAcHNjUk9hdVQwSEY4OTM3OUhDUWZA6b0pra1NMZAVZAPdHFxVVQzbTFoNHJRcjdacF93"}
graph = facebook.GraphAPI(token,version='3.1')

class DataScrape:

    def __init__(self, email_address):
        self.email_address = email_address

    def get_details(self):
        employee_detail = graph.request('%s?fields=name,email,title,department&limit=1000' %self.email_address)
        return employee_detail

    def get_profile_picture(self):
        employee_detail = self.get_details()
        profile_picture = graph.request('%s/picture?type=large' %employee_detail['id'])['url']
        return profile_picture

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
        feed = graph.request('%s?fields=feed&limit=100' %self.email_address)
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
        reactions = graph.request('%s?fields=reactions&limit=100' %post_id)
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
        group = graph.request('%s?fields=groups&limit=100' %self.email_address)
        group = group['groups']['data']

        for i in group:
            group_list.append(i['id'])

        return group_list


    def get_group_feed(self,group_id):
        group_post = graph.request('%s/feed?limit=100' %group_id)

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


    def get_reaction_given(self):
        start_time = time.time()
        print(start_time)
        reactions_dict = dict.fromkeys(['LIKE', 'LOVE', 'HAHA', 'WOW', 'SAD', 'ANGRY'], 0)
        for i in self.get_group_post_list():
            try:
                for j in self.get_reactions_summary(i)['reactions']['data']:
                    if j['name'] == (self.get_details()['name']):
                        if j['type'] == 'LIKE':
                            reactions_dict['LIKE'] += 1
                            print("[INFO] Like given add ~ 1")
                        elif j['type'] == 'LOVE':
                            reactions_dict['LOVE'] += 1
                            print("[INFO] Love given add ~ 1")
                        elif j['type'] == 'HAHA':
                            reactions_dict['HAHA'] += 1
                            print("[INFO] Haha given add ~ 1")
                        elif j['type'] == 'WOW':
                            reactions_dict['WOW'] += 1
                            print("[INFO] Wow given add ~ 1")
                        elif j['type'] == 'SAD':
                            reactions_dict['SAD'] += 1
                            print("[INFO] Sad given add ~ 1")
                        else:
                            reactions_dict['ANGRY'] += 1
                            print("[INFO] Angry given add ~ 1")
                    else:
                        print("[INFO] User haven't reacted in this post ~ 0")
            except:
                print('No reaction')
        print("--- %s seconds ---" % (time.time() - start_time))
        return reactions_dict
