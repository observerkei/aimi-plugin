from aimi_plugin.action.type import ActionToolItem


s_action = ActionToolItem(
    # 这个动作的名称, 默认是文件名
    # 在这里只是起到说明作用
    call="",
    # 当前 action 的描述
    # 说明这个action应该怎么使用
    description="打开url链接: 将url打开后以本方式返回, "
    f"如果url写错, 或者网页无法访问, 那么就可能得到异常结果, "
    f"打开url链接能获取内容详情, 更好分析. ",
    # 调用接口的时候填写的参数说明
    request={
        "url": "需要转换的url链接",
    },
    # 这里指明执行类型
    # system: 系统执行, 会有 chat_from 返回值
    # AI:     AI 执行, 没有 chat_from 返回值
    execute="system",
)


# 在这里通过字符串返回这个接口的运算结果
# 如果什么都不返回的话说明没有返回值
# 不需要执行的话, 不需要写 chat_from
# request: 调用方法的时候的传参, 默认 None
def chat_from(request: dict = None):
    import requests 
    from bs4 import BeautifulSoup   

    url = request['url']
    resp = requests.get(url = url)

    # 按照返回的编码解析
    resp.encoding = resp.apparent_encoding
    soup = BeautifulSoup(resp.text, "html.parser")

    # 删除js代码
    for tag in soup.find_all("script"):
        tag.decompose()
        
    # 删除style样式代码
    for tag in soup.find_all("style"):
        tag.decompose()

    # 返回所有文本
    text = ""
    first = True
    limit = 2048
    for tag in soup.find_all():
        if tag.string:
            if first and len(tag.string):
                text += "以下是打开的链接内容, 因为内容没有排版, 可以进行总结: {\n"
                first = False
            text += tag.string
            if len(text) > 2048:
                text += f'\n... ( 因为内容太长(>{limit}), 剩余部分已经省略. 如果没有想要的内容请尝试其他url链接. )\n'
                break
    

    if len(text):
        text += "\n}. "
    
    if not len(text):
        text = 'error: 这个 url 无正常解析, 请替换其他 url 再重新尝试. '

    return text