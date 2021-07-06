import jwt
import time

# headers
#   declare algorithm used
#   jku: 发送JWK的地址；最好用HTTPS来传输
#   jwk: 就是之前说的JWK
#   kid: jwk的ID编号
#   x5u: 指向一组X509公共证书的URL
#   x5c: X509证书链
#   x5t：X509证书的SHA-1指纹
#   x5t#S256: X509证书的SHA-256指纹
#   typ: 在原本未加密的JWT的基础上增加了 JOSE 和 JOSE+ JSON. JOSE序列化后文会说及. 适用于JOSE标头的对象与此JWT混合的情况. 
#   crit: 字符串数组 , 包含声明的名称 , 用作实现定义的扩展 , 必须由 this->JWT的解析器处理. 不常见. 
headers = {
    'alg': 'HS256'
}

key = "hankzhwang"


def jwt_encode(username):
    # payload
    #   iss: issuer 发布者的url地址
    #   sub: subject 该JWT所面向的用户 , 用于处理特定应用 , 不是常用的字段
    #   aud: audience 接受者的url地址
    #   exp: expiration 该jwt销毁的时间；unix时间戳
    #   nbf: not before 该jwt的使用时间不能早于该时间；unix时间戳
    #   iat: issued at 该jwt的发布时间；unix 时间戳
    #   jti: JWT ID 该jwt的唯一ID编号
    token_dict = {
        'iat': time.time(),
        'exp': time.time() + 900,
        'username': username
    }
    jwt_token = jwt.encode(token_dict,  # payload, 有效载体
                           key,  # 进行加密签名的密钥
                           algorithm="HS256",  # 指明签名算法方式, 默认也是HS256
                           headers=headers  # json web token 数据结构包含两部分, payload(有效载体), headers(标头)
                           )
    return str(jwt_token, encoding='utf-8')


def jwt_decode(token):
    print(type(token))
    if type(token) is not bytes:
        token = bytes(token, encoding='utf-8')
    payload = jwt.decode(token, key, algorithms=["HS256"])
    return payload

