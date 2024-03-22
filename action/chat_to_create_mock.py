from aimi_plugin.action.type import ActionToolItem


s_action = ActionToolItem(
    # 这个动作的名称, 默认是文件名
    # 在这里只是起到说明作用
    call="",
    # 当前 action 的描述
    # 说明这个action应该怎么使用
    description="创建模拟对象: 用于生成模拟对象, 可同时生成多个对象. "
    f"请通过逐步分析补全生成对象所需要的信息. "
    f"生成成功后要带上生成对象名称问是否需要保存, 如果需要, 将需要保存的对象分别添加一条note. "
    f"一般而言, 若无特殊说明, 默认生成之后就要对已知对象进行对象模拟. "
    f"这个方法不是模拟对象, 而是创建被模拟对象的信息, "
    f"如果要进行 模拟对象/对象模拟 交互, 请参见 Guidance 中 preset_rule 中有关模拟对象的说明, ",
    # 调用接口的时候填写的参数说明
    request={
        "type": "object",
        "mock": [
            {
                "type": "object",
                "description": "生成的其中一个角色相关信息. ",
                "name": "角色的名称: 用英文命名. 不可和其他人重复",
                "expect": "生成期望: 为了解决什么问题生成这个角色. ",
                "capacity": "能力分布: 这个角色具有什么能力",
                "core": "思考特征: 这个角色思考的时候, 会遵循什么行为模式. ",
            },
        ],
    },
    # 这里指明执行类型
    # system: 系统执行, 会有 chat_from 返回值
    # AI:     AI 执行, 没有 chat_from 返回值
    execute="system",
)


# 在这里通过字符串返回这个接口的运算结果
# 如果什么都不返回的话说明没有返回值
# request: 调用方法的时候的传参, 默认 None
def chat_from(request: dict = None):
    request = request['mock']

    def show_name(name):
        return f'系统消息: 已经生成 {name} , 因为新增了模拟对象, 需要保持之前模拟对象的情况下, 也追加模拟 {name}. '
    res = ''
    if request and isinstance(request, list):
        for mock in request:
            if 'name' in mock:
                res += show_name(mock['name']) + '\n'
    elif isinstance(request, dict) and 'name' in request:
        res = show_name(request['name'])
    #if len(res):
    #    res += "请询问是否需要将新增的角色全部信息添加笔记进行保存. 然后继续. "
    return res
