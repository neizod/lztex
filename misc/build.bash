sed -e "s/\\(nightly build: \\)[^\\)]*/\\1`date -R`/" `echo $(git rev-parse --show-toplevel)`/lztex.py
