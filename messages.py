#错误信息 固定好的
class Messages:
    BAD_REQUEST = {'code':1, 'msg':'用户信息错误'}  #错误码要做统一定义；
    USER_EXISTS = {'code':2, 'msg':'用户已存在'}
    INVALID_USERNAME_OR_PASSWORD = {'code':3, 'msg':'用户或密码错误'}