#/bin/bash

# would run through all 2016
echo "Running for all entries"
wc -w Journal/2016/*.md | sed -E -e 's/[[:space:]]{2,}//g' -e 's/(\.md)//g' -e '/total$/ d' -e 's/Journal\/[0-9]+\/0//g' | cut -d ' ' -f1,2 | #xargs -n 2 node post-wordcount-to-google-calendar.js
