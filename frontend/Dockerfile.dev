FROM node:18-alpine

WORKDIR /app

# 依存関係のコピーとインストール
COPY package*.json ./
RUN npm ci

# ソースコードのコピー
COPY . .

# 開発サーバーの起動
EXPOSE 3000
CMD ["npm", "run", "dev"]
