#!/usr/bin/ruby

require "base64"

path = "data/user-agent-raw.png"

# Reset file.
File.open(path, "w") { |f| f.write("") }

user_agents = `tshark -r data/ragent.pcap -Y http.request -T fields -e http.user_agent`
user_agents.split("\n")
           .map { |user_agent|
             md = user_agent.match(/sctf-app\/(.+)\//)
             md[1]
           }
           .map { |encoded| Base64.decode64(encoded) }
           .map { |decoded| File.open(path, "a") { |f| f.write(decoded) } }
