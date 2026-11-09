# iPhone demo media

The homepage's existing app section is upgraded to one native 16:9 player after
the four commission cards. The media source is configured in `index.html` at
`#iphone-demo-video > source`; no player JavaScript or third-party embed is used.

## Release gate

The production URL is configured as:
`https://media.carsalestrackerpro.com/carsalestrackerpro-sales-earnings-20261109.mp4`.
Domain provisioning and live playback must be verified before publishing. Do not
commit the MP4 to GitHub. Run `python3 scripts/check_iphone_demo.py` before release.
It rejects local or placeholder URLs; `--allow-local-preview` is for preparation only.

Verify the host serves `video/mp4`, supports byte-range requests for seeking, and
returns the unchanged approved file. Check playback again with the final URL.
The captions and poster remain local website assets.

## Approved media identity

- File: `CarSalesTrackerPro-Sales-Earnings-Demo.mp4`
- Size: 4,306,825 bytes
- SHA-256: `3a1e618cef233b6e8d335a36300a7c70ba2258731e9ad68b785cf571f6e799d3`
- Duration: 37.5 seconds (shown as 38 seconds in navigation)
- Picture: 1920 × 1080, H.264; audio: AAC music, no narration

`carsales-iphone-demo-poster.jpg` is the actual 0.2-second video frame, extracted
without additional artwork or altered UI:

```sh
ffmpeg -ss 0.2 -i CarSalesTrackerPro-Sales-Earnings-Demo.mp4 \
  -frames:v 1 -q:v 2 carsales-iphone-demo-poster.jpg
```

The English VTT track describes the visual sequence and music. The HTML details
walkthrough provides the same story without playback, including sample-data and
subscription-tier qualifications. It does not claim a delivered notification.
