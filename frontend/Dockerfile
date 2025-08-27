# ビルドステージ
FROM node:18-alpine AS builder

WORKDIR /app

# 依存関係のコピーとインストール
COPY package*.json ./
RUN npm ci

# ソースコードのコピー
COPY . .

# 本番用ビルド
RUN npm run build

# 本番ステージ
FROM nginx:alpine

# ビルド結果をnginxにコピー
COPY --from=builder /app/dist /usr/share/nginx/html

# nginx設定ファイルをコピー
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
