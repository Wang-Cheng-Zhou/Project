import socket

# 创建一个 TCP socket（IPv4 + 流式传输）
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 绑定到本地的 12345 端口
server_socket.bind(('localhost', 12345))
# 开始监听，最多允许 1 个待处理连接
server_socket.listen(1)
print('Waiting for a connection...')
# 阻塞等待客户端连接，返回客户端 socket 和地址
client_socket, client_addr = server_socket.accept()
print('Connection from:', client_addr)
# 进入循环，持续从客户端接收消息并回复
try:
    while True:
        data = client_socket.recv(1024)
        if not data:
            print('客户端已关闭连接。')
            break

        message = data.decode()
        print('客户端:', message)

        reply = input('请输入回复（输入 exit 关闭连接）：')
        if reply.lower() == 'exit':
            client_socket.send('服务器已断开连接。'.encode())
            break

        client_socket.send(reply.encode())
finally:
    client_socket.close()
    server_socket.close()