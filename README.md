# xch 

## requirements
    python3, python3-venv
    sqlite, mysql or postgresql (+ the appropriate python sqlalchemy-compatible module)

## installation
    git clone https://github.com/researcx/xch.git
    cd xch
    sh ./run.sh install

## running
`sh ./run.sh http` for a webserver or `sh ./run.sh socket` for an uwsgi socket

## features
- [x] boards
    - [x] board creation (unfinished)
        - [ ] board management
    - [ ] claimable board list
    - [ ] board claiming
    - [ ] catalog view
    - [ ] archive view
    - [x] board description display
    - [x] toggle for displaying poster country flag in posts (only stores ISO 3166-1 alpha-2 code)
    - [ ] toggle for randomized names for anonymous posters
    - [ ] toggle for displaying poster id in posts
- [x] threads
    - [x] seo urls with slug
    - [ ] thread options/moderation (closing, sticky, deletion, archiving)
    - [ ] thread archive toggle and automatic archiving of threads (per certain amount of posts (global or board-specific option)) or after certain time
    - [ ] autorefresh
    - [ ] displaying of sticky threads at top
- [x] posts
    - [x] posting
        - [x] tripcodes and secure tripcodes
        - [x] replying 
            - [ ] (+js elements)
        - [x] reference links
        - [ ] formatting (toggle/switcher between bbcode/markdown?)
            - [ ] quoting
            - [ ] replying
        - [x] uploads
            - [x] board file limit display
            - [x] board file type limit display
            - [x] board file type limits
            - [ ] board file size limits per type
            - [ ] board minimum image dimension limit
        - [x] file thumbnailing:
            - [x] images
            - [x] videos (buggy? (on smaller files?))
            - [ ] misc files
            - [ ] default thumbnails
        - [ ] post reporting
        - [ ] manual post approval system (board toggle)
    - [x] Delete posts
        - [x] via same IP
        - [x] via post password (set in options)
        - [x] via site moderator password (tripcode)
        - [ ] via board owner/moderator password (tripcode)
        - [x] delete files alongside with posts
        - [x] delete files from posts only
        - [x] delete multiple posts/files at once
- [x] ip system
    - [x] option to fully anonymize poster ip throughout site and in database
- [ ] ban status checking
- [x] styleable custom pages that can be easily added into /xch/templates/index/ and be served via http://board_url/index/page (page = name of the html file minus the .html part)
- [ ] global and board-specific word filters (also disallow posting on certain words)
- [ ] group nsfw tag
- [ ] mobile layout
- [ ] themeing
- [ ] static page rendering
    - [x] minimize html
- [x] public ban list
    - [ ] per-board
    - [ ] all bans
- [ ] html toggle for boards
- [ ] moderator panel
    - [ ] find boards by ip
    - [ ] report viewing
    - [ ] bans, per-board public ban list toggle
    - [ ] board approval
    - [ ] post approval
- [ ] site api
- [ ] xml and rss feed
- [ ] federation?
    - [ ] give boards keys which they use to federate w/
- [x] extensive configuration options
    - [ ] support for remote and/or encrypted storage
- [ ] refactor the whole thing
- [ ] 8chan style automatically-updating nerve center page (displays all threads w/ activity)

## things that could be done

- [ ] a lot of renders could be converted to template functions
- [ ] implement better methods of of caching
- [ ] a lot of code could be turned into functions