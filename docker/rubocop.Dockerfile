FROM ruby:3.1-slim

RUN gem install rubocop

ENTRYPOINT ["rubocop"]
