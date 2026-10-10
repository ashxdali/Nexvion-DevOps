FROM nginx:alpine

LABEL maintainer="Nexvion DevOps Project"
LABEL description="Nexvion static e-commerce website"

# Update installed Alpine packages with available security fixes
RUN apk update && apk upgrade --no-cache

# Remove the default Nginx website
RUN rm -rf /usr/share/nginx/html/*

# Copy the Nexvion application
COPY application/ /usr/share/nginx/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
