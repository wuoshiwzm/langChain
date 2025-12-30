



# Agent项目



## 安装命令


#### 本地部署大模型
pip install ollama








企业中也般不会使用 LangSmith

1. 安装 LangGraph CLI
```
pip install --upgrade "langgraph-cli[inmem]
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

