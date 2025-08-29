# Gerrit Code Review Homepage

Homepage for [Gerrit Code Review][home].

[home]: https://www.gerritcodereview.com/

## Running Locally

### Prerequisites
- Docker and Docker Compose

### Setup
1. Build and start the container:
   ```bash
   docker compose up --build
   ```

2. Or build and run with Docker directly:
   ```bash
   docker build -t gerritcodereview/homepage .
   docker run -p 4000:4000 -v $(pwd):/site gerritcodereview/homepage
   ```

3. Open your browser and navigate to:
   ```
   http://localhost:4000
   ```

### Development
- The site will automatically reload when you make changes to files

## Publishing

Instructions how to publish the Gerrit documentation can be found at:
https://www.gerritcodereview.com/publishing.html
