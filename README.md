# sightline

**See the view before you book.**

Every stadium and cinema is designed around *sightlines*, the line of sight from each seat to the stage. Sightline renders yours: you fly into a live 3D venue, pick your exact seat and see what you'll see from it before you pay.

Three experiences, all real-time 3D in the browser (three.js), priced in ₹ INR:

| | What you can do |
|---|---|
| 🎬 **Movies** (`cinema.html`) | Pick a film, experience (Multiplex · Giant Screen · Gold Lounge), date, showtime and number of seats. Fly into the auditorium, hover Classic / Prime / Recliner, pick seats side by side, see the screen from your seat, upgrade to recliners that actually recline, confirm and get an m-ticket. |
| 🎤 **Concert** (`stadium.html?event=concert`) | Stadium with a stage, LED walls and a standing floor: Front Barricade, Fan Pit and Floor zones on each side, plus a back floor. Closer to the stage costs more. Or pick a seat in the stands or a VIP skybox. |
| ⚽ **Football** (`stadium.html?event=football`) | Park → stand → block → seat, with the exact view from your seat and an upgrade to a leather-armchair skybox. |

## Features

- One continuous camera flight from the sky to your seat, with no cuts
- 48,000 individually bookable stadium seats (instanced, with a high-detail level of detail near the camera)
- Real image-based lighting (HDRI sky), sun shadows that follow the camera, molded clearcoat seats, scanned leather and concrete
- Cinema: a procedural trailer on the screen that lights the hall, a projector beam with dust, velvet curtains, and EXIT / निकास signs
- Live films from TMDB: real posters, backdrops on the big screen, runtimes and Indian certificates
- Adaptive quality: benchmarks your GPU behind the loader and holds a smooth frame rate

## Run locally

```bash
cp .env.example .env.local      # add your free TMDB key (optional)
python3 serve.py                # http://localhost:5173
```

No build step and no dependencies: plain HTML and ES modules loaded from a CDN. Without a TMDB key the cinema uses its built-in films.

Change the film line-up in `tmdb.json`. To use your own posters or stills, see `media/movies.example.json`.

## Deploy (Vercel)

Static site plus one serverless function (`api/tmdb.js`) that keeps the TMDB key on the server.

```bash
vercel --prod
vercel env add TMDB_API_KEY production
```

## Credits

- 3D: [three.js](https://threejs.org) (MIT)
- HDRI sky and PBR textures (leather, concrete, walnut, carpet): [Poly Haven](https://polyhaven.com) (CC0)
- Film data and images: [TMDB](https://www.themoviedb.org). *This product uses the TMDB API but is not endorsed or certified by TMDB.* Posters and stills belong to their respective studios.
- Fonts: Inter and Bebas Neue (Google Fonts, OFL)

Sightline and "Sightline Cinemas" are demo brands. No real tickets are sold.
