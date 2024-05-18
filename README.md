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
5. 確認與 redis 通訊可以輸入以下指令，沒有測試可以跳過

```
1. 終端機輸入 python3 manage.py shell <-- 會進入 執行環境
2. 輸入 import channels.layers <- 引入 channels.layers 模組
3. 輸入 channel_layer = channels.layers.get_channel_layer() 宣告 channel_layer 用來拿取 ChannelLayer 通道，這個方法可以用來發送跟接收消息
4. 輸入 from asgiref.sync import async_to_sync <- 導入非同步轉入同步函數 
5. 輸入 async_to_sync(channel_layer.send)('test_channel', {'type': 'hello'}) <- 發送訊息到 test_channel 通道
6. 輸入 async_to_sync(channel_layer.receive)('test_channel') <- 從 test_channel 通道接收訊息
7. {'type': 'hello'} <- 在執行環境會看到這則訊息
```