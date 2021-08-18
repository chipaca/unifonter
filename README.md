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

Several different styles are supported; use `--kind` (or `-k`) followed by a
style combination you want, otherwise one is chosen at random.

Supported styles can be seen via `unifonter -d`:

  Use              | Or  | To get
-------------------|-----|---------------------------
  bold             | b   | 𝐁𝐨𝐥𝐝
  italic           | i   | 𝐼𝑡𝑎𝑙𝑖𝑐
  bold italic      | bi  | 𝑩𝒐𝒍𝒅 𝑰𝒕𝒂𝒍𝒊𝒄
  sans             | s   | 𝖲𝖺𝗇𝗌-𝖲𝖾𝗋𝗂𝖿
  bold sans        | bs  | 𝗦𝗮𝗻𝘀-𝗦𝗲𝗿𝗶𝗳 𝗕𝗼𝗹𝗱
  italic sans      | is  | 𝘚𝘢𝘯𝘴-𝘚𝘦𝘳𝘪𝘧 𝘐𝘵𝘢𝘭𝘪𝘤
  bold italic sans | bis | 𝙎𝙖𝙣𝙨-𝙎𝙚𝙧𝙞𝙛 𝘽𝙤𝙡𝙙 𝙄𝙩𝙖𝙡𝙞𝙘
  script           | c   | 𝒮𝒸𝓇𝒾𝓅𝓉
  bold script      | bc  | 𝓑𝓸𝓵𝓭 𝓢𝓬𝓻𝓲𝓹𝓽
  double-struck    | d   | 𝔻𝕠𝕦𝕓𝕝𝕖-𝕊𝕥𝕣𝕦𝕔𝕜
  fraktur          | f   | 𝔉𝔯𝔞𝔨𝔱𝔲𝔯
  bold fraktur     | bf  | 𝕭𝖔𝖑𝖉 𝕱𝖗𝖆𝖐𝖙𝖚𝖗
  small-caps       | k   | Sᴍᴀʟʟ-Cᴀᴘꜱ
  mono             | m   | 𝙼𝚘𝚗𝚘𝚜𝚙𝚊𝚌𝚎
  wide             | w   | Ｆｕｌｌｗｉｄｔｈ

For the long forms, separate with whatever is most convenient for you:
spaces, dashes, pluses or underscores.
Order does not matter (`bold fraktur` or `fraktur bold`, `bis` or `sib`).
You can shorten `double-struck` to `double`, `small-caps` to `caps`,
`monospace` to `mono` and `fullwidth` to `wide`, in case the full names
are just too verbose for you. You can also mix short and long forms.
If you hate calling sans-serif `sans`, you can lengthen that one too.

Some other options are supported; see the output of `-h`.
