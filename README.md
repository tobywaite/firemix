FireMix
=======

FireMix is a host for lighting pattern generators--small programs known as "presets".  Use FireSim to see the output.

[![Build Status](https://travis-ci.org/cdawzrd/firemix.png)](https://travis-ci.org/cdawzrd/firemix)

Installation / Development
--------------------------

    pip install -r requirements.txt
    python firemix.py [--profile] demo.json

Use the `--profile` option to enable profiling of framerate and function calls.
With profiling enabled, a log message will be printed any time a preset takes
more than 12 ms to render a frame.

Use the `--preset` option to specify a preset (by class name) to play forever.
This is useful for preset development.

Please send pull requests for new presets and changes/additions to the core!