// Vercel serverless function: forwards a small, whitelisted set of TMDB requests
// using the server-side key (env var TMDB_API_KEY), so the key never reaches the browser.
const PATHS = [/^search\/movie$/, /^movie\/now_playing$/, /^movie\/\d+$/];
const PARAMS = ['query', 'language', 'region', 'append_to_response', 'include_image_language', 'page'];

module.exports = async (req, res) => {
  const key = process.env.TMDB_API_KEY;
  if (!key) return res.status(500).json({ error: 'TMDB_API_KEY is not configured' });
  const path = String(req.query.path || '');
  if (!PATHS.some(re => re.test(path))) return res.status(400).json({ error: 'path not allowed' });
  const qs = new URLSearchParams({ api_key: key });
  for (const p of PARAMS) if (req.query[p] !== undefined) qs.set(p, String(req.query[p]));
  try {
    const r = await fetch(`https://api.themoviedb.org/3/${path}?${qs}`);
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.setHeader('Cache-Control', 's-maxage=3600, stale-while-revalidate=86400');
    res.status(r.status).send(await r.text());
  } catch (e) {
    res.status(502).json({ error: 'TMDB unreachable' });
  }
};
