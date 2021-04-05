# History of versions

## sweetheart-0.1.1a

TODO: next steps comming soon

- provide `sweetbook` the documentation of sweetheart
- improve available bash command within /usr/local/bin 
- implement deployment tools for `mongod`,`cherrypy`,`uvicorn`
- re-implement simpleTemplateEngine from bottle module

## sweetheart-0.1.0b

### initial features

- build and run webapps from quick and clean python/html/css code
- provide a `sweet` command line interface including full-featured installer
- provide a `sws` command line tool for simple use of common bash features
- provide built-in powerfull documentation tools
- provide readable and flexible configuration capabilities

### main python objects available within sweet.py

- `_config_`: provide a configuration dict editable as a json file and allowing high flexibility
- `_deepconfig_`: provide a low-level configuration dict for dev purposes
- `subproc`: class leading facilities e.g. mongod, webbrowser, terminal using bash
- `mdbook`: class implementing mdbook (rust crate) within sweet.py
- `ini`: class for initializing sweetheart project with apt,cargo,pip,npm,wget
- `CommandLine`: class for building command line interfaces at the speedlight
- `cli`: the sweet command line interface builder object
- `html`: function for rendering html with ease
- `quickstart`: function for starting a webapp with all required services
- `WebApp`: class for building a webapp quickly
