FROM ruby:3.3-alpine

RUN apk add --no-cache build-base gcc bash cmake

# Install a newer bundler version that's compatible with Ruby 3.3
RUN gem install bundler -v "2.4.22"

EXPOSE 4000

WORKDIR /site

# create new site by setting -e JEKYLL_NEW=true
ENV JEKYLL_NEW=false

# Copy necessary files for the build
COPY Gemfile* ./
COPY _config.yml ./
COPY index.md ./
COPY 404.md ./
COPY search.json ./
COPY sitemap.xml ./
COPY _layouts/ ./_layouts/
COPY _includes/ ./_includes/
COPY _data/ ./_data/
COPY _posts/ ./_posts/
COPY _drafts/ ./_drafts/
COPY pages/ ./pages/
COPY assets/ ./assets/
COPY images/ ./images/
COPY js/ ./js/
COPY css/ ./css/
COPY fonts/ ./fonts/
COPY licenses/ ./licenses/
COPY tools/ ./tools/

COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# on every container start we'll
ENTRYPOINT [ "docker-entrypoint.sh" ]

CMD [ "bundle", "exec", "jekyll", "serve", "--force_polling", "-H", "0.0.0.0", "-P", "4000" ]
