FROM nginx:alpine

# HTMLファイルをNginxのドキュメントルートにコピー
COPY index.html /usr/share/nginx/html/
COPY dock.png /usr/share/nginx/html/

# カスタムNginx設定をコピー（オプション）
COPY nginx.conf /etc/nginx/nginx.conf


CMD ["nginx", "-g", "daemon off;"]
