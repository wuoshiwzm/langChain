# BaseModel 自定义工具
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from pydantic import create_model

from agent.llm import zhipuai_llm

class SearchArgs(BaseModel):
    query: str = Field(..., description='search query')

class MyWebSearchTool(BaseTool):
    name: str = "web_search2"
    description: str = "use to search online"
    # args_schema:Type[BaseModel] = SearchArgs  # 工具参数（第一种写法）

    # 第一种写法
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.args_schema = create_model('SearchInput', query=(str, Field(..., description='online search'))) # 动态创建一个数据模型类 （工具参数 第二种写法）


    def _run(self, query:str) -> str:

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