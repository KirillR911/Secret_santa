import pymongo
from pymongo import MongoClient

def _get_null_user():
    return {
            'name' : 'Kirill Ryzhikov', 
            'vk_link' : 'vk.com/kirizhik',
            'photo_link' : 'sum9....',
            'wish_list' : 'Gift name, this, and this ',
            'location' : {
                'faculcy' : 'CMS', 
                'year' : 1, 
                'group' : 123, 
                'main_building' : '2-Gum'
            },
            'status' : 0 ,
            'target' : None,
            'santa' : None
        }

def create_data(name: str, photo_link: str, location: dict, wish_list: str, vk_link: str) -> dict:
    
    """
        gets name: string, vk_link: string, photo_link: string, location: dict
        wish_list: string, status: int 
        example: 
        {
            _id : 0,
            name : 'Kirill Ryzhikov', 
            vk_link : 'vk.com/kirizhik',
            photo_link : 'sum9....',
            wish_list : 'Gift name, this, and this ',
            location : {
                faculcy : 'CMS', 
                year : 1, 
                group : 123, 
                main_building : '2-Gum'
            }
            status : 0,
            target : id,
            santa : id,
            status codes: 0 -  Registered, not in Game 
                          1 - In game, has target
                          2 - In game, has santa
                          3 - In game, has santa and target
                          4 - In game, delivered gift
                          5 - In game, got gift
                          6 - In game, got gift and delivered
        }
    """
    d = {}
    d ['name'] = name 
    d ['vk_link']  = vk_link
    d ['photo_link'] = photo_link
    d ['location'] = location
    d ['wish_list'] = wish_list
    d ['status'] = 0
    d ['santa'] = None 
    d ['target'] = None
    return d

def register(data, collection):
    collection.insert_one(data)

def _get_null_result():
    return {
            'santa' : None,
            'target' : None,
            'status' : 0,
            'description' : {
                    'gift_name' : None,
                    'photo' : None
            }
    }
    

def init_db(client):
    client.drop_database('sant_db')
    db = client.sant_db
    users_col = db.users
    users_col.insert_one(_get_null_user())
    db.users.create_index([('name', pymongo.ASCENDING)],
                                   unique=True)
    result_col = db.result
    result_col.insert_one(_get_null_result())
    result_col.create_index([('santa', pymongo.ASCENDING), ('target', pymongo.ASCENDING)],
                                unique=True)
    return db

def set_santa(user1: str, user2: str, collection: pymongo.collection.Collection, result: pymongo.collection.Collection) :
    """
        Updates db by setting santa for user2 and target for user1 and their statuses to 1 
        user1 : string - name of target
        user2 : string - name of santa
        collection : pymongo.collection.Collection collection of users
    """
    #print(collection.find_one())
    id1 = collection.find_one({'name' : user1})['_id']
    id2 = collection.find_one({'name' : user2})['_id']
    collection.update_one({'_id' : id1}, {'$set' : {'santa' : id2}})
    collection.update_one({'_id' : id2}, {'$set' : {'target' : id1}})
    collection.update_one({'_id' : id1}, {'$set' : {'status' : 2 if collection.find_one({'name' : user1})['status'] == 0 else 3}})
    collection.update_one({'_id' : id2}, {'$set' : {'status' : 1 if collection.find_one({'name' : user2})['status'] == 0 else 3}})
    res = {
        'santa':id2,
        'target':id1,
        'status' : 0,
        'description' : {
            'gift' : collection.find_one({'name' : user1})['wish_list'],
            'photo' : None
        }
    }
    result.insert_one(res)
    return id1, id2 

def remind_target(user: str, collection: pymongo.collection.Collection) -> dict:
    """
        reminds target to user
        user : string - name of to remind target
        collection : pymongo.collection.Collection collection of users
    """
    target_id = collection.find_one({'name' : user})['target']
    d = collection.find_one({'_id' : target_id})
    
    del d['santa']
    del d['target']
    return d


def random_target(user: str, collection: pymongo.collection.Collection, result):
    id  = collection.find_one({'name' : user})['_id']
    tar_id = collection.aggregate([{'$match': {'santa' : None, 'name' : {'$ne' : user}}},\
                                    {'$sample' : {'size' : 1}}])
    l = [x for x in tar_id]
    print(l)
    if (len(l)):
        set_santa(l[0]['name'], user, collection, result)
        
        return l[0]['name']
    else:
        return None


