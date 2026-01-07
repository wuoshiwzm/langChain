



# Agent项目



## 安装命令


#### 本地部署大模型

```
pip install langchain langgraph langchain-openai langchain-deepseek 
pip install dotenv
pip install ollama
pip install zhipuai
```









企业中也般不会使用 LangSmith

1. 安装 LangGraph CLI
```
pip install --upgrade "langgraph-cli[inmem]"
```

2. 配置 LangSmith 的环境变量


3. 创建 LangGraph 配置文件 [langgraph.json](langgraph.json)

```
{
  "dependencies": ["."],
  "graphs": {
    "agent": "./src/agent/agent1.py:agent"  # 这里的 :agent 表示 变量名
  },
  "env": ".env"
}
```

将 src 目录标记为源代码根目录

```

│  .env
│  .gitignore
│  langgraph.json
│  README.md
└─src
        env_utis.py
        main.py
        __init__.py
```

4. 编写AGENT代码


5. 安装依赖项
在 LangGraph 应用的根目录 安装依赖
```
pip install -e .
```

6. 在 studio 中查看代理

根目录执行
```
langgraph dev
```
- 🚀 API: http://127.0.0.1:2024
- 🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
- 📚 API Docs: http://127.0.0.1:2024/docs

> 开始疯狂报错 AttributeError: module 'huggingface_hub' has no attribute 'hf_api' xxx， 后来尝试了各种方法，安装卸载 langchain, langgraph, 最还删除了包 huggingface_hub 才正常运行



装包：
```shell
pip install pyjwt



```


# SQL Agent 项目

### 依赖库
```angular2html
pip install sqlalchemy pymysql loguru
```

# 2. 工具开发

## 2.0 工具创建的方式

所有工具都继承 langchain_core.tools.BaseTool

## 2.1 XXX 工具


## 2.2 XXX 工具


## 2.3 XXX 工具


## 2.4 XXX 工具

## 2.5 要点

运行命令
```
langgraph dev --allow-blocking 允许阻塞 （同步调用， 否则 langgraph 默认采用导步调用）
```

大模型传参时，尽量不要使用太复杂的数据类型
比如将 Optional[List[str]] = None 改为 Optional[str] = None















