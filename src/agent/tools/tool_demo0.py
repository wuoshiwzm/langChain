from langchain_core.tools import tool
from pydantic import BaseModel, Field
from llm import zhipuai_llm


# ? 注释方法1：写在函数体内
@tool("web_search", description="联网搜索工具")
def web_search(query: str) -> str:
    """联网搜索工具

    Args:
        query: 查询参数
    Returns:
        返回搜索结果
    """
    try:
        # 调用 web_search 对象的 web_search 方法
        response = zhipuai_llm.web_search.web_search(
            search_engine="search_pro",
            search_query=query,
        )
        if response.search_result:
            return "\n\n".join([d.content for d in response.search_result])

        pass
    except Exception as e:
        print(e)
        return f"Error {e}"
    return "no search result"


# ? 注释方法2： 写在 @tool 中
class SearchArgs(BaseModel):
    query: str = Field(..., description="搜索关键词")

@tool("web_search2", parse_docstring=True)
def web_search2(query: str) -> str:
    """
    执行网络搜索并返回结果。

    Args:
        query (str): 搜索关键词

    Returns:
        str: 搜索结果文本
    """
    print(query)
    return "搜索结果示例"



if __name__ == "__main__":
    print(web_search.name)
    print(web_search.description)
    print(web_search.args)
    print(web_search.args_schema.model_json_schema())

    result = web_search.invoke({"query":"what is langchain?"})

