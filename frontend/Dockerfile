# syntax=docker/dockerfile:1
FROM node:22-alpine AS builder

WORKDIR /app

RUN corepack enable && corepack prepare pnpm@latest --activate

COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./

RUN pnpm install --no-frozen-lockfile

COPY . .

ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}

RUN pnpm build

FROM node:22-alpine AS runtime

RUN npm install -g serve

WORKDIR /app
COPY --from=builder /app/dist .

EXPOSE 80

CMD ["serve", "-s", ".", "-l", "80"]
