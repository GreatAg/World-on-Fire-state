import psycopg2
from collections import Counter

con = psycopg2.connect(host="", database="", user="", password="=")


def recording_info(user_id, name, username, password):
    cur = con.cursor()
    cur.execute('''UPDATE wof_reg SET esm=%(name)s , username=%(username)s , pass=%(password)s WHERE user_id=%(user_id)s;
       INSERT INTO wof_reg (user_id,esm,username,pass)
       SELECT %(user_id)s , %(name)s , %(username)s , %(password)s
       WHERE NOT EXISTS (SELECT 1 FROM wof_reg WHERE user_id=%(user_id)s);''',
                {'user_id': int(user_id), 'name': str(name), 'username': str(username), 'password': str(password)})
    con.commit()
    cur.close()


def load_information(user_id):
    cur = con.cursor()
    cur.execute('''SELECT esm ,username,pass, towns, achvs  FROM wof_reg
                   WHERE user_id = %(user_id)s''', {'user_id': int(user_id)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    if len(load) == 0:
        return False
    return load[0][0], load[0][1], load[0][2], load[0][3], load[0][4]


def load_info(username):
    cur = con.cursor()
    cur.execute('''SELECT esm ,user_id,pass, towns, achvs  FROM wof_reg
                   WHERE username = %(username)s''', {'username': str(username)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    if len(load) == 0:
        return False
    return load[0][0], load[0][1], load[0][2], load[0][3], load[0][4]


def del_tuple(user_id):
    cur = con.cursor()
    cur.execute('''DELETE FROM wof_reg
    WHERE user_id = %(user_id)s''', {'user_id': int(user_id)})
    con.commit()
    cur.close()


def acceptacc(user_id):
    cur = con.cursor()
    cur.execute(f'''UPDATE wof_reg
                SET isaccept=TRUE 
                 Where user_id = %(user_id)s''', {'user_id': int(user_id)})
    con.commit()
    cur.close()


def load_usernames():
    cur = con.cursor()
    cur.execute('''SELECT username FROM wof_reg''')
    load = cur.fetchall()
    con.commit()
    cur.close()
    user = [i[0] for i in load]
    return user


def load_pass(username):
    cur = con.cursor()
    cur.execute('''SELECT pass FROM wof_reg
    WHERE username = %(username)s''', {'username': str(username)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    pas = [i[0] for i in load]
    return pas


def checkacc(username):
    cur = con.cursor()
    cur.execute('''SELECT isaccept FROM wof_reg
    WHERE username = %(username)s''', {'username': str(username)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    acc = [i[0] for i in load]
    return acc


def checksignup(user_id):
    cur = con.cursor()
    cur.execute('''SELECT user_id FROM wof_reg
    WHERE user_id = %(user_id)s''', {'user_id': str(user_id)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    acc = [i[0] for i in load]
    if len(acc) == 0:
        return False
    else:
        return True


def recordactive(user_id, username):
    cur = con.cursor()
    cur.execute(f'''UPDATE wof_actives SET user_id = %(user_id)s WHERE username = %(username)s;
       INSERT INTO wof_actives (user_id,username)
       SELECT %(user_id)s , %(username)s
       WHERE NOT EXISTS (SELECT 1 FROM wof_actives WHERE username = %(username)s);''',
                {'user_id': int(user_id), 'username': str(username)})
    con.commit()
    cur.close()


def load_uid(username):
    cur = con.cursor()
    cur.execute('''SELECT user_id FROM wof_reg
    WHERE username = %(username)s''', {'username': str(username)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    usr = [i[0] for i in load]
    return usr


def updateuid(usr, username):
    cur = con.cursor()
    cur.execute(f'''UPDATE wof_reg
                SET user_id=%(user_id)s
                Where username = %(username)s''', {'user_id': int(usr), 'username': str(username)})
    con.commit()
    cur.close()


def loadactives():
    cur = con.cursor()
    cur.execute('''SELECT user_id,username FROM wof_actives''')
    load = cur.fetchall()
    con.commit()
    cur.close()
    usrid = [i[0] for i in load]
    usrs = [i[0] for i in load]
    return usrid, usrs


def load_username(user_id):
    cur = con.cursor()
    cur.execute('''SELECT username FROM wof_actives
    WHERE user_id = %(user_id)s''', {'user_id': int(user_id)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    username = [i[0] for i in load]
    return username


def loadxp(username):
    cur = con.cursor()
    cur.execute('''SELECT xp FROM wof_reg
    WHERE username = %(username)s''', {'username': str(username)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    xp = [i[0] for i in load]
    return xp


def add_xp(username, xp):
    cur = con.cursor()
    cur.execute('''UPDATE wof_reg
                SET xp = xp + %(xp)s
                 Where username = %(username)s''',
                {'username': str(username), 'xp': int(xp)})
    con.commit()
    cur.close()


def load_achvs(username):
    cur = con.cursor()
    cur.execute('''SELECT achvs FROM wof_reg
    WHERE username = %(username)s''', {'username': str(username)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    achv = [i[0] for i in load]
    return achv[0]


def add_ach(username, achv):
    cur = con.cursor()
    cur.execute('''UPDATE wof_reg
                SET achvs = %(achv)s
                 Where username = %(username)s''',
                {'username': str(username), 'achv': str(achv)})
    con.commit()
    cur.close()


def load_achive(num):
    cur = con.cursor()
    cur.execute('''SELECT achve FROM wof_achvs
    WHERE ach_id = %(num)s''', {'num': int(num)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    achv = [i[0] for i in load]
    return achv[0]


def load_towns(username):
    cur = con.cursor()
    cur.execute('''SELECT towns FROM wof_reg
    WHERE username = %(username)s''', {'username': str(username)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    achv = [i[0] for i in load]
    return achv[0]


def add_town(username, towns):
    cur = con.cursor()
    cur.execute('''UPDATE wof_reg
                SET towns = %(towns)s
                 Where username = %(username)s''',
                {'username': str(username), 'towns': str(towns)})
    con.commit()
    cur.close()


def check_active(user_id):
    cur = con.cursor()
    cur.execute('''SELECT username FROM wof_actives
    WHERE user_id = %(user_id)s''', {'user_id': str(user_id)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    usr = [i[0] for i in load]
    if len(usr) == 0:
        return False
    else:
        return True


def deactive(user_id):
    cur = con.cursor()
    cur.execute('''DELETE FROM wof_actives
    WHERE user_id = %(user_id)s''', {'user_id': int(user_id)})
    con.commit()
    cur.close()


def record_war(username, att_username, town, att_town, status):
    cur = con.cursor()
    cur.execute(f"""INSERT INTO wof_state (username,attackeduser,town,attackedtown,win) 
               VALUES (%(username)s,%(att_username)s,%(town)s,%(att_town)s,%(status)s )""",
                {'username': str(username), 'att_username': str(att_username), 'town': str(town),
                 'att_town': str(att_town), 'status': status})
    con.commit()
    cur.close()


def ret_usertown(town):
    town = f'%{town}%'
    cur = con.cursor()
    cur.execute('''SELECT username FROM wof_reg
    WHERE towns LIKE %(town)s ''', {'town': str(town)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    town = [i[0] for i in load]
    if len(town) == 0:
        return False
    return town[0]


def load_state(username):
    username = f'%{username}%'
    query = f'''
with attack as (
    SELECT count(username) as attacks
    FROM wof_state
    WHERE username LIKE %(username)s
),
     win as (
         SELECT count(username) as wins
         FROM wof_state
         WHERE username LIKE %(username)s AND win = TRUE 
     ),
     lose as (
         SELECT count(username) as loses
         FROM wof_state
         WHERE username LIKE %(username)s AND win = FALSE 
     ),
     attacked as (
         SELECT count(username) as attackeds
         FROM wof_state
         WHERE attackeduser LIKE %(username)s
     ),
     winattacked as (
         SELECT count(username) as winattackeds
         FROM wof_state
         WHERE attackeduser LIKE %(username)s AND win = FALSE 
     ),
     loseattacked as (
         SELECT count(username) as loseattackeds
         FROM wof_state
         WHERE attackeduser LIKE %(username)s AND win = TRUE 
     )
select *
from attack,
     win,
     lose,
     attacked,
     winattacked,
     loseattacked
'''
    try:
        cur = con.cursor()
        cur.execute(query, {'username': str(username)})
        res = cur.fetchone()
        con.commit()
        cur.close()

        return res[0], res[1], res[2], res[3], res[4], res[5]
    except Exception as e:
        print(e)
        return 0, 0, 0, 0, 0, 0


def get_attackto(username):
    username = f'%{username}%'
    cur = con.cursor()
    cur.execute('''select attackeduser , count (attackeduser) AS attacks from wof_state
    WHERE username LIKE %(username)s
    group by attackeduser
    order by attacks desc limit 5''', {'username': str(username)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    usernames = [i[0] for i in load]
    num = [i[1] for i in load]
    return usernames, num


def get_attackfrom(username):
    cur = con.cursor()
    cur.execute('''select username , count (username) AS attacks from wof_state
    WHERE attackeduser = %(username)s
    group by username
    order by attacks desc limit 5''', {'username': str(username)})
    load = cur.fetchall()
    con.commit()
    cur.close()
    usernames = [i[0] for i in load]
    num = [i[1] for i in load]
    j = 0
    newusers = []
    for number in num:
        newusers.append([usernames[j] for i in range(number)])
        j += 1
    users = []
    for user in newusers:
        for numuser in user:
            for i in numuser.split(','):
                users.append(i)
    duplicate_dict = Counter(users)
    print(duplicate_dict)
    users = list(dict.fromkeys(users))
    num = []
    for i in users:
        num.append(duplicate_dict[i])

    sorteduser = [x for _, x in sorted(zip(num, users), reverse=True)][:5]
    sortednum = [x for x, _ in sorted(zip(num, users), reverse=True)][:5]

    return sorteduser, sortednum


def get_best():
    cur = con.cursor()
    cur.execute('''select username ,xp from wof_reg 
    order by xp desc limit 5''')
    load = cur.fetchall()
    con.commit()
    cur.close()
    usernames = [i[0] for i in load]
    xps = [i[1] for i in load]
    return usernames, xps


def add_admin(user_id):
    cur = con.cursor()
    cur.execute(f"""INSERT INTO wof_admins (user_id) 
               VALUES (%(user_id)s)""", {'user_id': int(user_id)})
    con.commit()
    cur.close()


def rem_admin(user_id):
    cur = con.cursor()
    cur.execute('''DELETE FROM wof_admins
                 WHERE user_id = %(user_id)s''',
                {'user_id': int(user_id)})
    con.commit()
    cur.close()


def load_admins():
    cur = con.cursor()
    cur.execute('''SELECT user_id FROM wof_admins''')
    load = cur.fetchall()
    con.commit()
    cur.close()
    if len(load) == 0:
        return False
    admins = [i[0] for i in load]
    return admins


def load_all():
    cur = con.cursor()
    cur.execute('''SELECT esm, username, user_id, towns, achvs  FROM wof_reg''')
    load = cur.fetchall()
    con.commit()
    cur.close()
    if len(load) == 0:
        return False
    names = [i[0] for i in load]
    usernames = [i[1] for i in load]
    user_ids = [i[2] for i in load]
    towns = [i[3] for i in load]
    achvs = [i[4] for i in load]
    return names, usernames, user_ids, towns, achvs


def update_name(user_id, name):
    cur = con.cursor()
    cur.execute('''UPDATE wof_reg
                SET esm = %(name)s
                Where user_id = %(user_id)s''',
                {'user_id': int(user_id), 'name': str(name)})
    con.commit()
    cur.close()


def update_pass(user_id, password):
    cur = con.cursor()
    cur.execute('''UPDATE wof_reg
                SET pass = %(password)s
                Where user_id = %(user_id)s''',
                {'user_id': int(user_id), 'password': str(password)})
    con.commit()
    cur.close()


def update_username(user_id, username, olduser):
    cur = con.cursor()
    cur.execute('''UPDATE wof_reg
                SET username = %(username)s
                Where user_id = %(user_id)s''',
                {'user_id': int(user_id), 'username': str(username)})

    cur.execute('''UPDATE wof_actives
                SET username = %(username)s
                Where user_id = %(user_id)s''',
                {'user_id': int(user_id), 'username': str(username)})
    cur.execute('''UPDATE wof_state
                SET username = %(username)s
                Where username = %(olduser)s''',
                {'user_id': int(user_id), 'username': str(username), 'olduser': str(olduser)})
    cur.execute('''UPDATE wof_state
                SET attackeduser = %(username)s
                Where attackeduser = %(olduser)s''',
                {'user_id': int(user_id), 'username': str(username), 'olduser': str(olduser)})
    con.commit()
    cur.close()


def del_achvs():
    cur = con.cursor()
    cur.execute('''DELETE FROM wof_achvs''')
    con.commit()
    cur.close()


def add_dailyach(id, dachive, price):
    cur = con.cursor()
    cur.execute('''INSERT INTO wof_achvs (ach_id, achve,price)
                VALUES (%(id)s,%(dachive)s,%(price)s)''', {'id': int(id), 'dachive': str(dachive), 'price': int(price)})
    con.commit()
    cur.close()


def load_ach():
    cur = con.cursor()
    cur.execute('''SELECT ach_id, achve, price FROM wof_achvs''')
    load = cur.fetchall()
    con.commit()
    cur.close()
    ids = [i[0] for i in load]
    achvs = [i[1] for i in load]
    prices = [i[2] for i in load]
    return ids, achvs, prices
