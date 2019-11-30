from sec_san import *
client = MongoClient()
db = init_db(client)
u = {
            'name' : 'Kirill Ryzhikov1', 
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
register(u, db.users)