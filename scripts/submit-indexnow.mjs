import { readFile } from "node:fs/promises";

const host = "carsalestrackerpro.com";
const origin = `https://${host}`;
const key = "f94f86596256e1597287ad38cee3f9cf";
const keyLocation = `${origin}/${key}.txt`;

const sitemap = await readFile(new URL("../sitemap.xml", import.meta.url), "utf8");
const urlList = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map((match) => match[1]);

if (!urlList.length || urlList.some((url) => !url.startsWith(`${origin}/`))) {
  throw new Error("The sitemap did not contain a valid same-origin URL list.");
}

const keyResponse = await fetch(`${keyLocation}?check=${Date.now()}`, {
  headers: { "user-agent": "CarSales-Tracker-Pro-IndexNow/1.0" },
});
const servedKey = (await keyResponse.text()).trim();

if (!keyResponse.ok || servedKey !== key) {
  throw new Error(`IndexNow ownership key is not live yet (HTTP ${keyResponse.status}).`);
}

const response = await fetch("https://api.indexnow.org/indexnow", {
  method: "POST",
  headers: { "content-type": "application/json; charset=utf-8" },
  body: JSON.stringify({ host, key, keyLocation, urlList }),
});

if (![200, 202].includes(response.status)) {
  throw new Error(`IndexNow rejected the submission (HTTP ${response.status}).`);
}

console.log(`IndexNow accepted ${urlList.length} canonical URLs (HTTP ${response.status}).`);
