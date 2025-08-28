FROM nginx:alpine

# HTMLファイルをNginxのドキュメントルートにコピー
COPY index.html /usr/share/nginx/html/

# カスタムNginx設定をコピー（オプション）
COPY nginx.conf /etc/nginx/nginx.conf

# ポート80を公開
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
