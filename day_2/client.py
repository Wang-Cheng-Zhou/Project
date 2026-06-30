import socket
# 创建一个 TCP socket（IPv4 + 流式传输）
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 连接到本地服务器的 12345 端口
client_socket.connect(('localhost', 12345))
# 打印连接成功提示
print('已连接到服务器。')

# 进入循环，持续发送消息并接收服务器回复
try:
    while True:
        # 获取用户输入的消息
        message = input('请输入要发送的文本（输入 exit 退出）：')
        # 输入 exit 则退出循环
        if message.lower() == 'exit':
            print('客户端退出。')
            break

        # 将消息编码为字节后发送给服务器
        client_socket.send(message.encode())
        # 接收服务器返回的数据（最多 1024 字节）
        data = client_socket.recv(1024)
        # 空数据表示服务器已关闭连接
        if not data:
            print('服务器已关闭连接。')
            break

        # 打印服务器的回复消息
        print('服务器回复:', data.decode())
finally:
    # 确保关闭客户端 socket，释放资源
    client_socket.close()