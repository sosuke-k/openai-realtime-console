import express from "express";
import fs from "fs";
import { createServer as createViteServer } from "vite";
import { execFile } from "child_process";
import "dotenv/config";

const app = express();
const port = process.env.PORT || 3000;

// Configure Vite middleware for React client
const vite = await createViteServer({
  server: { middlewareMode: true },
  appType: "custom",
});
app.use(vite.middlewares);

// API route for token generation using Python script
app.get("/token", (req, res) => {
  execFile("python3", ["token.py"], { env: process.env }, (err, stdout, stderr) => {
    if (err) {
      console.error("Token generation error:", err);
      console.error(stderr);
      res.status(500).json({ error: "Failed to generate token" });
      return;
    }
    try {
      const data = JSON.parse(stdout);
      res.json(data);
    } catch (e) {
      console.error("Token parse error:", e);
      res.status(500).json({ error: "Failed to generate token" });
    }
  });
});

// Render the React client
app.use("*", async (req, res, next) => {
  const url = req.originalUrl;

  try {
    const template = await vite.transformIndexHtml(
      url,
      fs.readFileSync("./client/index.html", "utf-8"),
    );
    const { render } = await vite.ssrLoadModule("./client/entry-server.jsx");
    const appHtml = await render(url);
    const html = template.replace(`<!--ssr-outlet-->`, appHtml?.html);
    res.status(200).set({ "Content-Type": "text/html" }).end(html);
  } catch (e) {
    vite.ssrFixStacktrace(e);
    next(e);
  }
});

app.listen(port, () => {
  console.log(`Express server running on *:${port}`);
});
