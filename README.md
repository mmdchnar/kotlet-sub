# Kotlet-sub

## only REALITY support

working with https://github.com/MHSanaei/3x-ui panel (v1.4.6)

## NOTE:
#### After 3x-ui v1.4.6 the API path changed to "/panel/api/inbounds"

### Set your .env like this (create it)
```
PORT=443
INBOUND_ID=2
SNI=mysni.com
SID=b0a2d1sd
PBK=XKhsMM21SCcUbbNITm70mQdRar94_yYA4S_FtdgmHzo

URI=vless://$UUID$@$DOMAIN$:$PORT$?security=reality&encryption=none&pbk=$PBK$&headerType=none&fp=chrome&type=tcp&flow=xtls-rprx-vision&sni=$SNI$&sid=$SID$#$NAME$

PANEL_URL=https://www.mysite.com:2053
API_PATH=/panel/api/inbounds

# this will be a dictionary
DOMAINS_keys=IPv4,IPv6
DOMAINS_values=IPv4.mysite.com,IPv6.mysite.com

# The api username and password
USER=username
PASS=password

DEBUG=0
```
