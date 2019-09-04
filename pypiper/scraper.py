import facebook

token = {"DQVJ2YVlQUlJ4VkF5ZAlJnQi13eVo2U01kbXNBSTBhU19WbEIwQXJiZAzdXWVdZAeEs0UEV4NkVXSnMtTDBIMGtiN0x5dGFNQmduWnQzeHpxZA3I5VktWRGEzVGl3ZA2toTVhfamU5X2ItYVFVazFTdVBGa1BYbm8yQ3BCeEVPb3RZAdW5VMmxJUjNmNUN2U0N1cUJxN1QxMDJRY3BJZAWVkWllUbWZArNWx5SnFMNmlOcW9JOEk4YnRZASkhEcVp6VXdYbDJ2UXZAMYWFB"}
graph = facebook.GraphAPI(token,version='3.1')

class DataScrape:

    def __init__(self, email_address):
        self.email_address = email_address

    def get_details(self):
        employee_detail = graph.request('%s?fields=name,email,title,department&limit=9999999999' %self.email_address)
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

    def get_reaction_received(self, post_id):
        reactions = graph.request('%s?fields=reactions&limit=99999999' %post_id)
        return reactions

    def reaction_summary(self):
        reactions = [0, 0, 0, 0, 0, 0]
        for i in self.get_post_list():
            try:
                for j in self.get_reaction_received(i)['reactions']['data']:
                    if j['type'] == 'LIKE':
                        reactions[0] += 1
                    elif j['type'] == 'LOVE':
                        reactions[1] += 1
                    elif j['type'] == 'HAHA':
                        reactions[2] += 1
                    elif j['type'] == 'WOW':
                        reactions[3] += 1
                    elif j['type'] == 'SAD':
                        reactions[4] += 1
                    else:
                        reactions[5] += 1
            except KeyError as e:
                print('No reaction')
        return reactions


    def get_user_groups(self):
        group_list = []
        group = graph.request('%s?fields=groups&limit=999999999999' %self.email_address)
        group = group['groups']['data']

        for i in group:
            group_list.append(i['id'])

        print('User has no groups')
        return group_list


    def get_group_feed(self,group_id):
        group_post = graph.request('%s/feed?limit=9999999999' %group_id)

        try:
            group_post = group_post['data']
        except:
            print('Group has no posts')
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
        reactions_given = [0, 0, 0, 0, 0, 0]
        for i in self.get_group_post_list():
            try:
                for j in self.get_reaction_received(i)['reactions']['data']:
                    if j['name'] == (self.get_details()['name']):
                        if j['type'] == 'LIKE':
                            reactions[0] += 1
                        elif j['type'] == 'LOVE':
                            reactions[1] += 1
                        elif j['type'] == 'HAHA':
                            reactions[2] += 1
                        elif j['type'] == 'WOW':
                            reactions[3] += 1
                        elif j['type'] == 'SAD':
                            reactions[4] += 1
                        else:
                            reactions[5] += 1
            except:
                print('No interaction')
        return reactions_given
