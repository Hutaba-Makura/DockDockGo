<<<<<<< HEAD
FROM nginx:alpine
=======
# ビルドステージ
FROM node:18-alpine AS builder
>>>>>>> origin/main

# HTMLファイルをNginxのドキュメントルートにコピー
COPY index.html /usr/share/nginx/html/

# カスタムNginx設定をコピー（オプション）
COPY nginx.conf /etc/nginx/nginx.conf

# ポート80を公開
EXPOSE 80

<<<<<<< HEAD
=======
# 本番用ビルド
RUN npm run build

# 本番ステージ
FROM nginx:alpine

# ビルド結果をnginxにコピー
COPY --from=builder /app/dist /usr/share/nginx/html

# nginx設定ファイルをコピー
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

>>>>>>> origin/main
CMD ["nginx", "-g", "daemon off;"]
