# Пример внедрения Sec_canta







Импортируем нужные библиотеки

```python
from sec_san import *

```

Инициализируем базу данных 

```python
client = MongoClient()
db = init_db(client)
```

В `db.users` хранится информация о пользователях 

В `db.result` хранится информация о результатах взаимдействий санта-цель



Регистрация нового пользователя

```python
register(u, db.users)
```

Где `u` - словарь 

```python
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
```

Словарь `u` можно создать функцией `create_data`

```python
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
    
```

Установить пользователю рандомную цель

```python
random_target('Kirill Ryzhikov', db.users, db.result)
```

В случае успеха делает запись в коллекциях `users` и `result` иначе возвращает None , что значит, что нет доступных пользователей. 

Напомнить пользователю инмформацию

```python
remind_target('Kirill Ryzhikov', db.users)
```




