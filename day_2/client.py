import socket
# 创建一个 TCP socket（IPv4 + 流式传输）
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 连接到本地服务器的 12345 端口
client_socket.connect(('localhost', 12345))
print('已连接到服务器。')

try:
    while True:
        message = input('请输入要发送的文本（输入 exit 退出）：')
        if message.lower() == 'exit':
            print('客户端退出。')
            break

        client_socket.send(message.encode())
        data = client_socket.recv(1024)
        if not data:
            print('服务器已关闭连接。')
            break

        print('服务器回复:', data.decode())
finally:
    client_socket.close()