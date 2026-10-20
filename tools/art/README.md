# Rawuh theme art

Painted illustrations for the invitation themes are rendered with code (no image generator):
`art.py` simulates watercolour (pigment/glaze/knockout), gouache, linocut, gold foil, painted skies and paper.
Each theme has a render script in `themes/<id>.py` with fixed seeds; output goes to
`frontend/public/themes/art/<id>/*.webp`.

    pip install numpy scipy pillow skia-python opensimplex
    python3 -I tools/art/themes/mawar-blush.py

The scripts were written with absolute output paths (`/root/w/frontend/public/...`) and `sys.path` pointing at
`/tmp/pen/art`; adjust those two constants at the top of a script before re-running it locally.
