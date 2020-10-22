import time
import base64
import hmac
from weatherSys import db_handling as db

def authenticate(username, token):
    token_obj=out_token(username,token)

    if token_obj:
        return db.authority_check(username)
    else:
        return False





def get_token(key, expire=7776000):
    '''
    :param key: str (用户给定的key，需要用户保存以便之后验证token,每次产生token时的key 都可以是同一个key)
    :param expire: int(最大有效时间，单位为s)
    :return: token
    '''
    ts_str = str(time.time() + expire)
    ts_byte = ts_str.encode("utf-8")
    sha1_tshexstr  = hmac.new(key.encode("utf-8"),ts_byte,'sha1').hexdigest()
    token = ts_str+':'+sha1_tshexstr
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
    return b64_token.decode("utf-8")


def out_token(key, token):
    '''
    :param key: 服务器给的固定key
    :param token: 前端传过来的token
    :return: true,false
    '''

    # token是前端传过来的token字符串
    try:
        token_str = base64.urlsafe_b64decode(token).decode('utf-8')
        token_list = token_str.split(':')
        if len(token_list) != 2:
            return False
        ts_str = token_list[0]
        if time.time() > float(ts_str):
            return False
        known_sha1_tsstr = token_list[1]
        sha1 = hmac.new(key.encode("utf-8"),ts_str.encode('utf-8'),'sha1')
        calc_sha1_tsstr = sha1.hexdigest()
        if calc_sha1_tsstr != known_sha1_tsstr:
            return False
        return True
    except Exception as e:
        print(e)