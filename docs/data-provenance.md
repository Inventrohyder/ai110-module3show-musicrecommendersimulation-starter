# Data provenance and annotation policy

VibeFinder preserves the ten course-provided starter songs and extends that catalog with ten real recordings. The starter entries are fictional classroom simulation data, so they have no release-year or MusicBrainz claim. MusicBrainz recording pages were used to verify the added recordings' artist/title identity and original release year. The catalog does not copy audio, lyrics, cover art, popularity metrics, or proprietary streaming analysis.

`energy`, `mood`, `tempo_bpm`, `valence`, `danceability`, and `acousticness` are student-reviewed **simulation annotations** for every row. They are normalized estimates for explaining this small content-based exercise, not claims about Spotify, YouTube, or MusicBrainz metadata.

| #   | Recording           | Artist            | Catalog source     | Release year | MusicBrainz verification                                                            | Verified   |
| --- | ------------------- | ----------------- | ------------------ | -----------: | ----------------------------------------------------------------------------------- | ---------- |
| 1   | Sunrise City        | Neon Echo         | Course starter CSV |            — | Not applicable: fictional simulation entry                                          | —          |
| 2   | Midnight Coding     | LoRoom            | Course starter CSV |            — | Not applicable: fictional simulation entry                                          | —          |
| 3   | Storm Runner        | Voltline          | Course starter CSV |            — | Not applicable: fictional simulation entry                                          | —          |
| 4   | Library Rain        | Paper Lanterns    | Course starter CSV |            — | Not applicable: fictional simulation entry                                          | —          |
| 5   | Gym Hero            | Max Pulse         | Course starter CSV |            — | Not applicable: fictional simulation entry                                          | —          |
| 6   | Spacewalk Thoughts  | Orbit Bloom       | Course starter CSV |            — | Not applicable: fictional simulation entry                                          | —          |
| 7   | Coffee Shop Stories | Slow Stereo       | Course starter CSV |            — | Not applicable: fictional simulation entry                                          | —          |
| 8   | Night Drive Loop    | Neon Echo         | Course starter CSV |            — | Not applicable: fictional simulation entry                                          | —          |
| 9   | Focus Flow          | LoRoom            | Course starter CSV |            — | Not applicable: fictional simulation entry                                          | —          |
| 10  | Rooftop Lights      | Indigo Parade     | Course starter CSV |            — | Not applicable: fictional simulation entry                                          | —          |
| 11  | Happy               | Pharrell Williams | Added recording    |         2013 | [recording](https://musicbrainz.org/recording/eead98b6-001d-4372-bccb-0efaf533cf80) | 2026-07-22 |
| 12  | Everlong            | Foo Fighters      | Added recording    |         1997 | [recording](https://musicbrainz.org/recording/59636d8a-0ce3-42a3-9a70-c75431ffc2dc) | 2026-07-22 |
| 13  | Enter Sandman       | Metallica         | Added recording    |         1991 | [recording](https://musicbrainz.org/recording/cd3ed501-4798-4423-9113-b9bea2d5df16) | 2026-07-22 |
| 14  | Levels              | Avicii            | Added recording    |         2011 | [recording](https://musicbrainz.org/recording/3e4f95b4-ef7d-467d-9c56-fd898671a4c0) | 2026-07-22 |
| 15  | Strobe              | deadmau5          | Added recording    |         2009 | [recording](https://musicbrainz.org/recording/f772526b-69c9-4170-9022-453289cec63d) | 2026-07-22 |
| 16  | Midnight City       | M83               | Added recording    |         2011 | [recording](https://musicbrainz.org/recording/dd83a741-ffd9-4c9d-a027-9f09b72d1925) | 2026-07-22 |
| 17  | An Ending (Ascent)  | Brian Eno         | Added recording    |         1983 | [recording](https://musicbrainz.org/recording/dadc1cfb-d928-4940-b06a-8f005755be91) | 2026-07-22 |
| 18  | Weightless          | Marconi Union     | Added recording    |         2011 | [recording](https://musicbrainz.org/recording/36cb35d2-3780-414a-9ef9-fec1e56e2eed) | 2026-07-22 |
| 19  | So What             | Miles Davis       | Added recording    |         1959 | [recording](https://musicbrainz.org/recording/cc5cbbc6-e7e7-4ea8-a401-367b3e6699fc) | 2026-07-22 |
| 20  | Blue in Green       | Miles Davis       | Added recording    |         1959 | [recording](https://musicbrainz.org/recording/45a30bdb-407e-48b9-8cab-f8c1e0ce51b5) | 2026-07-22 |

## Annotation rubric

- **Genre and mood:** broad classroom labels used for direct preference matching.
- **Energy, valence, danceability, acousticness:** a 0–1 relative estimate, assigned consistently across this small catalog.
- **Tempo:** approximate beats per minute, used only as a closeness value rather than a claim of beat-tracking precision.
- **Review:** `load_songs` checks every value for range and type validity. The catalog deliberately spans high/low energy, acoustic/electronic texture, and eight genres.
