# Plot Maps

Public hosting for plot azimuth and profile maps used in ArcGIS Experience Builder and related Innovatree Portal applications.

## Repository structure

Maps are organized first by project and then by map type:

```text
plot-maps/
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

Use lowercase filenames with three-digit, zero-padded plot numbers:

```text
plot-001.png
plot-002.png
plot-010.png
```

Use the same filename for the corresponding azimuth and profile maps. The containing folder identifies the map type.

Avoid spaces, capital letters, and special characters in project, folder, and file names. URLs are case-sensitive.

## Public image URLs

After GitHub Pages is enabled, images can be accessed using:

```text
https://innovatree-portal.github.io/plot-maps/{project}/{map-type}/plot-{number}.png
```

Examples:

```text
https://innovatree-portal.github.io/plot-maps/simpcw/azimuth/plot-001.png
https://innovatree-portal.github.io/plot-maps/simpcw/profile/plot-001.png
https://innovatree-portal.github.io/plot-maps/canim/azimuth/plot-010.png
```

These direct image URLs can be stored in a dataset or constructed dynamically in ArcGIS Experience Builder.

## Adding maps

1. Create the project folder if it does not already exist.
2. Add `azimuth` and `profile` subfolders.
3. Export maps using the established dimensions and image format.
4. Name each image using the corresponding zero-padded plot number.
5. Upload the images to the correct folders.
6. Confirm that the public GitHub Pages URLs load before adding them to the Portal.

## GitHub Pages

Configure GitHub Pages to deploy from the root of the `main` branch:

1. Open the repository **Settings**.
2. Select **Pages**.
3. Under **Build and deployment**, select **Deploy from a branch**.
4. Select the `main` branch and `/ (root)` folder.
5. Save the configuration.

No HTML viewer or index is required. The repository is intended to serve the image files directly.

## Image guidance

- Use `.png` when preserving fine text, map labels, and linework is most important.
- Keep image dimensions and export quality consistent within each map type.
- Optimize unusually large images before uploading.
- Avoid committing draft exports or unnecessary duplicate files.
- If an image is replaced, keep its existing filename so Portal links remain valid.

