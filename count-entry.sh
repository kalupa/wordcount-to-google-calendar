#!/usr/local/bin/zsh

wc -w "$1" |
    sed -E -e 's/[[:space:]]{2,}//g' \
        -e 's/(\.md)//g' -e '/total$/ d' \
        -e 's/Journal\/[0-9]+\/0//g' |
    cut -d ' ' -f 1,2 |
    xargs -n 2 node app.js
