# Linkvertise Bypasser

## About

This program is a Linkvertise shortlink bypasser. Linkvertise links are hyperlinks that have the target link hidden behind a plethora of obstacles, whether that be downloading viruses or watching ads. Since most people needing to bypass Linkvertise links also use the messaging platform Discord, I integrated the program with a Discord bot, in which you can directly invite to your server by [clicking here](https://discord.com/api/oauth2/authorize?client_id=811339635950485546&permissions=8&scope=bot).

`log.txt` is a log that displays the last time a certain user (identified by the Discord user id) has bypassed a link. Keeping a log of last used time is used for the cooldown feature, in which users in `premium.txt` have no cooldown.

## How It Works

In order to explain how the bot works we will use the link `https://linkvertise.com/123123/randomusername?o=sharing` to demo. The link is the cleaned up to get rid of the original linkvertise.com/ and ?o=sharing part: essentially just the middle part remains: `123123/randomusername`

The bot then sends a request to ` https://publisher.linkvertise.com/api/v1/redirect/link/static/insert/linkvertise/path/here` , replacing "insert/linkvertise/part/here" with the middle cleaned up part that we got from the previous step, resulting in `https://publisher.linkvertise.com/api/v1/redirect/link/static/123123/randomusername`.

The link id can be found from the previous request with the "id" attribute returned from the link. Then create a json file with the same setup as `{"timestamp":1606260928, "random":"6548307", "link_id":31283553}`

The timestamp is the unix epoch, random isn't really random (always has to be 6548307) and link_id is the id we obtained from the first request.

Use the same replacement process used in the first request to replace the part of url in `https://publisher.linkvertise.com/api/v1/redirect/link/insert/linkvertise/path/here/target?serial=base64encodedjson` and replace "base64encodedjson" with the json object created converted to base64, and then send a request to the new link created.

The final hidden link can be obtained from the json returned at json.data.link.id

## Proxies

Because of the popularity of the discord bot, I implemented rotating proxies grabbed from [SSL Proxies](https://sslproxies.org/). This causes the response of the bot to slow down, but now the bot does not get ratelimited if overloaded. The program uses the proxies.py file to grab proxies and determine if the proxies are real and responsive.

Credit for proxies: https://www.alexbilz.com/post/rotating-free-elite-proxies-in-python/

## Data Collection

Disclaimer: I am not associated with nor endorse the messages collected by the bot. Data is collected from every single message. The data collected associated with time are in UTC format. Message id, channel id, channel name, author id, author username, unix epoch time, year, month, day, hour, minute, second, command, content, and time elapsed for command are all recorded. There is not really any monetary benefit from collecting this data, but it is just interesting to look at an analyze to see the behaviors of the people bypassing the Linkvertise links.

## Commands

.bypass `link`

.help

### Credits

Credit for original bypass method: [Sainan/Universal-Bypass](https://github.com/Sainan/Universal-Bypass)