# CTF

These are a few simple CTF challenges.

## Spoilers

You can find the summary in [spoilers.md](spoilers.md). There is also a list of vulnerabilities which might be helpful if teaching a workshop.

## Running

Install Docker: https://docs.docker.com/install/

Install docker-compose: https://docs.docker.com/compose/install/ (note that the version bundled with your system can be too old)

Then just run:

    docker-compose build
    docker-compose up

The application should be served under `localhost:8000`.

## Hosting

Here is an example for nginx:

```
location / {
    proxy_pass http://127.0.0.1:8000/;
    include /etc/nginx/proxy_params;
}
```

The `proxy_params` are important to ensure the application generates the right redirects.

## Adding a new challenge

To add a challenge called `foo`:

* Create `foo/` directory with `app.py` inside. Make a Flask app available under `/foo/...`.
* Add `foo` to the following files:
  * `docker-compose.yml` (Docker container)
  * `main/nginx.conf` (proxy)
  * `main/html/index.html` (link from main page)

You can see that the `base.html` file is shared, and mounted in all containers.

## License

By Paweł Marczewski <pwmarcz@gmail.com>.

Licensed under MIT. See LICENSE for details.
