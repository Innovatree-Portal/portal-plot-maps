# Plot Maps

Public hosting for plot azimuth and profile maps used in ArcGIS Experience Builder and related Innovatree Portal applications.

## Repository structure

Maps are organized first by project and then by map type:

```text
portal-plot-maps/
├── README.md
├── gitanyow/
│   ├── azimuth/
│   └── profile/
├── simpcw/
│   ├── azimuth/
│   └── profile/
└── canim/
    ├── azimuth/
    └── profile/
```

New projects should follow the same structure:

```text
project-name/
├── azimuth/
└── profile/
```

## File naming

Retain the established export filenames for each map type:

```text
Azimuth: Plot{plot-number}_azimuth_map.png
Profile: Plot{plot-number}_profile.png
```

Examples:

```text
Plot2_azimuth_map.png
Plot2_profile.png
```

Do not add download suffixes such as `(1)` to repository filenames. Capitalization must remain consistent because URLs are case-sensitive.

## Public image URLs

Use the raw GitHub URL when embedding a map in the Portal or ArcGIS Experience Builder. A raw URL returns the image itself rather than the GitHub file page.

General format:

```text
https://raw.githubusercontent.com/Innovatree-Portal/portal-plot-maps/main/{project}/{map-type}/{filename}
```

Azimuth-map format:

```text
https://raw.githubusercontent.com/Innovatree-Portal/portal-plot-maps/main/{project}/azimuth/Plot{plot-number}_azimuth_map.png
```

Profile-map format:

```text
https://raw.githubusercontent.com/Innovatree-Portal/portal-plot-maps/main/{project}/profile/Plot{plot-number}_profile.png
```

Examples for Simpcw Plot 2:

```text
Azimuth:
https://raw.githubusercontent.com/Innovatree-Portal/portal-plot-maps/main/simpcw/azimuth/Plot2_azimuth_map.png

Profile:
https://raw.githubusercontent.com/Innovatree-Portal/portal-plot-maps/main/simpcw/profile/Plot2_profile.png
```

Do not use the following type of URL for an embed:

```text
https://github.com/Innovatree-Portal/portal-plot-maps/blob/main/...
```

The `/blob/` URL opens the GitHub webpage surrounding the file. Raw URLs display only the image and can be stored directly in a dataset or constructed dynamically in Experience Builder.

## Adding maps

1. Create the project folder if it does not already exist.
2. Add `azimuth` and `profile` subfolders.
3. Export maps using the established dimensions and image format.
4. Keep the established filename for each map type.
5. Upload the images to the correct folders.
6. Open the raw GitHub URL and confirm that it displays only the image before adding it to the Portal.

GitHub Pages, an HTML viewer, and an index page are not required for this repository.

## Image guidance

- Use `.png` when preserving fine text, map labels, and linework is most important.
- Keep image dimensions and export quality consistent within each map type.
- Optimize unusually large images before uploading.
- Avoid committing draft exports or unnecessary duplicate files.
- If an image is replaced, keep its existing filename so Portal links remain valid.
