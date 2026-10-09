FROM nginx:alpine

LABEL maintainer="Nexvion DevOps Project"
LABEL description="Nexvion static e-commerce website"

# Remove the default Nginx website
RUN rm -rf /usr/share/nginx/html/*

# Copy the website into the Nginx document root
COPY application/ /usr/share/nginx/html/

# Expose the HTTP port
EXPOSE 80

# Run Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]
