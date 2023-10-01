FROM python:3.9-alpine
ENV ACCOUNT_ID=${ACCOUNT_ID}
ENV EMAIL=${EMAIL}
ENV REGION=${REGION}
WORKDIR /cdk
RUN apk add --update nodejs npm
RUN npm install -g aws-cdk
RUN apk add --update zip
RUN apk update \
    && apk --no-cache add curl \
    && apk --no-cache add unzip \
    && curl "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "awscli-bundle.zip" \
    && unzip awscli-bundle.zip \
    && ./awscli-bundle/install -i /usr/local/aws -b /usr/local/bin/aws 
RUN pip install -r requirements.txt
ENTRYPOINT ["/cdk/entrypoint.sh"]

