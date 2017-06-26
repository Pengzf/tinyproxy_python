# tinyproxy_python

tinyproxy_for_python项目

读取同目录的tiny.conf用于修改请求头,

支持语法

  [Method]=['GET', 'POST', 'PUT', "DELETE", 'HAVE'] Or 'CONNECT'

  [Url]=http:/github.com/?????

  [Uri]=/??????

  [Version]=HTTP/1.1

  [Host]=github.com:443

  [N]=\n

  [R]=\r

  [T]=\t

  [RN]=\r\n

例如

  [Method] [Url] [Version][RN]Host:[Host]

  CONNECT github.com:443 HTTP/1.1\r\n

  Host:github.com:443

说明:
原项目参考地址:

  https://github.com/915546302/tinyproxy
