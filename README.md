# unifonter
unifonter is a filter that tries to make ASCII fancy with the help of Unicode

# quick intro

`unifonter` is meant to be used as a filter, or as a quick lookup /
translation tool. So you can use it either like

    $ man man | unifonter
    𝔐𝔄𝔑(1)                        𝔐𝔞𝔫𝔲𝔞𝔩 𝔭𝔞𝔤𝔢𝔯 𝔲𝔱𝔦𝔩𝔰                        𝔐𝔄𝔑(1)

    𝔑𝔄𝔐𝔈
           𝔪𝔞𝔫 - 𝔞𝔫 𝔦𝔫𝔱𝔢𝔯𝔣𝔞𝔠𝔢 𝔱𝔬 𝔱𝔥𝔢 𝔰𝔶𝔰𝔱𝔢𝔪 𝔯𝔢𝔣𝔢𝔯𝔢𝔫𝔠𝔢 𝔪𝔞𝔫𝔲𝔞𝔩𝔰

    𝔖𝔜𝔑𝔒𝔓𝔖ℑ𝔖
           𝔪𝔞𝔫 [𝔪𝔞𝔫 𝔬𝔭𝔱𝔦𝔬𝔫𝔰] [[𝔰𝔢𝔠𝔱𝔦𝔬𝔫] 𝔭𝔞𝔤𝔢 ...] ...
           𝔪𝔞𝔫 -𝔨 [𝔞𝔭𝔯𝔬𝔭𝔬𝔰 𝔬𝔭𝔱𝔦𝔬𝔫𝔰] 𝔯𝔢𝔤𝔢𝔵𝔭 ...
           𝔪𝔞𝔫 -𝔎 [𝔪𝔞𝔫 𝔬𝔭𝔱𝔦𝔬𝔫𝔰] [𝔰𝔢𝔠𝔱𝔦𝔬𝔫] 𝔱𝔢𝔯𝔪 ...
           𝔪𝔞𝔫 -𝔣 [𝔴𝔥𝔞𝔱𝔦𝔰 𝔬𝔭𝔱𝔦𝔬𝔫𝔰] 𝔭𝔞𝔤𝔢 ...

or

    $ unifonter Hello
    ℍ𝕖𝕝𝕝𝕠

Several different styles are supported; use `-k` followed by a style
combination you want, otherwise one is chosen at random.

Supported styles can be seen via `unifonter -d`:

  Use | To get
-----:|:-----
  `b` | `𝐁𝐨𝐥𝐝`
  `i` | `𝐼𝑡𝑎𝑙𝑖𝑐`
 `bi` | `𝑩𝒐𝒍𝒅 𝑰𝒕𝒂𝒍𝒊𝒄`
  `s` | `𝖲𝖺𝗇𝗌-𝖲𝖾𝗋𝗂𝖿`
 `bs` | `𝗦𝗮𝗻𝘀-𝗦𝗲𝗿𝗶𝗳 𝗕𝗼𝗹𝗱`
 `is` | `𝘚𝘢𝘯𝘴-𝘚𝘦𝘳𝘪𝘧 𝘐𝘵𝘢𝘭𝘪𝘤`
`bis` | `𝙎𝙖𝙣𝙨-𝙎𝙚𝙧𝙞𝙛 𝘽𝙤𝙡𝙙 𝙄𝙩𝙖𝙡𝙞𝙘`
  `c` | `𝒮𝒸𝓇𝒾𝓅𝓉`
 `bc` | `𝓑𝓸𝓵𝓭 𝓢𝓬𝓻𝓲𝓹𝓽`
  `d` | `𝔻𝕠𝕦𝕓𝕝𝕖-𝕊𝕥𝕣𝕦𝕔𝕜`
  `f` | `𝔉𝔯𝔞𝔨𝔱𝔲𝔯`
 `bf` | `𝕭𝖔𝖑𝖉 𝕱𝖗𝖆𝖐𝖙𝖚𝖗`
  `k` | `Sᴍᴀʟʟ-Cᴀᴘꜱ`
  `m` | `𝙼𝚘𝚗𝚘𝚜𝚙𝚊𝚌𝚎`
  `w` | `Ｆｕｌｌｗｉｄｔｈ`

but note the order of the letters doesn't matter (`-k bis` is the same
as `-k sib`), so if you find that you think "fraktur bold" instead of
"bold fraktur", just go with it.

Some other options are supported; see the output of `-h`.
