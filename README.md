# 專案名稱
DisWork

## 介紹


## 功能


## Setup Steps 設定步驟

#### 虛擬環境:
```
$ pip install poetry
$ poetry init -n
$ poetry shell
$ poetry install
```
## Node.js
```
$ install node
$ npm init -y
$ npm run dev
```
```
$ make server
```

### 使用私人聊天設定步驟
1. 到 Docker 官方下載 [Docker](https://www.docker.com/) 
2. $ docker run -p 6379:6379 -d redis:7
3. 再來安裝 channels_redis，以便 Channels 與 Redis 互動。
4. $ poetry add channels_redis

### 成員
