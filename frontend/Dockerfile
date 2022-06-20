FROM node:14.17-alpine

WORKDIR /frontend

COPY package.json ./

RUN apk add yarn
RUN yarn install
RUN yarn global add serve

COPY ./public ./public
COPY ./src ./src

EXPOSE 5000

CMD yarn build && serve -s build