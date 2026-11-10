# Plot Maps

Public hosting for plot azimuth and profile maps used in ArcGIS Experience Builder and related Innovatree Portal applications.

## Repository structure

Maps are organized first by project and then by map type:

```text
portal-plot-maps/
├── README.md
├── pad_plot_images_4x3.py
├── alib/
│   ├── azimuth/
│   ├── profile/
│   └── soil_samples/
├── canim/
│   ├── azimuth/
│   └── profile/
├── simpcw/
│   ├── azimuth/
│   └── profile/
└── sxfn/
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

Capitalization must remain consistent because URLs are case-sensitive.

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
3. Export PNG maps and apply the 4:3 standardization described below.
4. Keep the established filename for each map type.
5. Upload the images to the correct folders.
6. Open the raw GitHub URL and confirm that it displays only the image before adding it to the Portal.

GitHub Pages, an HTML viewer, and an index page are not required for this repository.

## Image guidance

- Use `.png` when preserving fine text, map labels, and linework is most important.
- Keep plot/profile aspect ratios at 4:3 and export quality consistent within each map type.
- Optimize unusually large images before uploading.
- Avoid committing draft exports or unnecessary duplicate files.
- If an image is replaced, keep its existing filename so Portal links remain valid.

## 4:3 standardization

Plot and profile PNGs use a landscape 4:3 aspect ratio for consistent presentation
across project portals. Standardization adds the minimum centered white padding
without cropping, resizing, or changing original pixels or transparency. Odd
padding adds one extra pixel on the right or bottom. Filenames and relative
folder structures are preserved. Soil sample images and soil charts are excluded.

The script recursively selects PNGs under `azimuth` and `profile` folders without
hardcoding projects. It ignores soil-named files/folders, Git metadata, symlinks,
and output/staging folders. Already 4:3 images are skipped without rewriting.

Run from PowerShell with Python 3 and Pillow:

```powershell
py -m pip install Pillow
Set-Location 'C:\Users\Owner\Documents\GitHub\portal-plot-maps'

# Preview only; this is also the default when no mode is given.
py -B .\pad_plot_images_4x3.py --dry-run --expect 66

# Explicitly replace eligible originals; back them up first.
py -B .\pad_plot_images_4x3.py --in-place --expect 66
```

`--expect` is an optional count guard; update or omit it when adding maps.
Only `--in-place` permits overwriting originals. Each changed image is validated
against its original pixels and minimum 4:3 canvas, before and after replacement.
Failures are reported and return a nonzero exit code. Temporary files stay outside
the repository. Repeating the in-place command leaves standardized files unchanged.

Optional staging uses a separate directory; valid existing outputs are retained
and invalid outputs are reported without overwriting. Soil images in an older
staging run are ignored:

```powershell
$stage = 'C:\Users\Owner\Documents\GitHub\portal-plot-maps-4x3-staging'
py -B .\pad_plot_images_4x3.py --output $stage --write --expect 66
py -B .\pad_plot_images_4x3.py --output $stage --validate --expect 66
```
