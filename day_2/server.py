import socket

# 创建一个 TCP socket（IPv4 + 流式传输）
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 绑定到本地的 12345 端口
server_socket.bind(('localhost', 12345))
# 开始监听，最多允许 1 个待处理连接
server_socket.listen(1)
# 打印等待连接的提示
print('Waiting for a connection...')
# 阻塞等待客户端连接，返回客户端 socket 和地址
client_socket, client_addr = server_socket.accept()
# 打印客户端的地址信息
print('Connection from:', client_addr)
# 进入循环，持续从客户端接收消息并回复
try:
    while True:
        # 接收客户端发来的数据（最多 1024 字节）
        data = client_socket.recv(1024)
        # 空数据表示客户端已断开连接
        if not data:
            print('客户端已关闭连接。')
            break

        # 解码接收到的字节数据为字符串
        message = data.decode()
        # 打印客户端发送的消息
        print('客户端:', message)

        # 获取服务器端的回复输入
        reply = input('请输入回复（输入 exit 关闭连接）：')
        # 输入 exit 则通知客户端并断开
        if reply.lower() == 'exit':
            client_socket.send('服务器已断开连接。'.encode())
            break

        # 将回复编码为字节后发送给客户端
        client_socket.send(reply.encode())
finally:
    # 确保关闭客户端和服务器 socket，释放资源
    client_socket.close()
    server_socket.close()