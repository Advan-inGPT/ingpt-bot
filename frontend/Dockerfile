# --- Build Stage ---
FROM cirrusci/flutter:stable AS build


FROM ghcr.io/cirruslabs/flutter:stable-web

# Create a non-root user
RUN useradd -m flutteruser
USER flutteruser

# Set working directory
WORKDIR /home/flutteruser/app

# Copy project files
COPY . .

# Get dependencies and build
RUN flutter pub get
RUN flutter build web

# --- Serve Stage ---
FROM nginx:alpine
COPY --from=build /app/build/web /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
