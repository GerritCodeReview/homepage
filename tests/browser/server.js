// Serve the production build and isolated fixture pages, never the repository.
const http = require("node:http");
const fs = require("node:fs");
const path = require("node:path");
const root = path.resolve(__dirname, "../..");
for (const file of [
  "_site/index.html",
  "_test/site/fixtures/nested/page.html",
]) {
  if (!fs.existsSync(path.join(root, file)))
    throw new Error(`Build ${file} before browser tests`);
}
const types = {
  ".html": "text/html",
  ".css": "text/css",
  ".js": "text/javascript",
  ".json": "application/json",
  ".svg": "image/svg+xml",
  ".png": "image/png",
};
http
  .createServer((request, response) => {
    const url = new URL(request.url, "http://localhost");
    const directory = path.join(
      root,
      url.pathname.startsWith("/fixtures/") ? "_test/site" : "_site",
    );
    let file;
    try {
      file = path.resolve(directory, "." + decodeURIComponent(url.pathname));
    } catch {
      response.writeHead(400).end();
      return;
    }
    if (!file.startsWith(directory + path.sep) && file !== directory) {
      response.writeHead(403).end();
      return;
    }
    if (fs.existsSync(file) && fs.statSync(file).isDirectory())
      file = path.join(file, "index.html");
    if (!fs.existsSync(file) || !fs.statSync(file).isFile()) {
      response.writeHead(404).end("Not found");
      return;
    }
    response.writeHead(200, {
      "Content-Type": types[path.extname(file)] || "application/octet-stream",
    });
    fs.createReadStream(file).pipe(response);
  })
  .listen(Number(process.env.TEST_PORT || 4173), "127.0.0.1");
