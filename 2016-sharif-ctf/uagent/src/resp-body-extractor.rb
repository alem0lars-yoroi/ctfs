#!/usr/bin/ruby

require "base64"
require "pp"

path = "data/response-body-raw.zip"

data = `tshark -r data/ragent.pcap -Y http.response -T fields -e http.response.line -e media.type`

responses = []
data.split("\n").each_slice(9).to_a.each do |response|
  md = response[7].match(/,Content-Range: bytes (?<from>\d+)-(?<to>\d+)/)
  responses << {
    from: Integer(md[:from]),
    to: Integer(md[:to]),
    value: response[8].gsub(/^\t/, "").split(":")
  }
end

responses.sort! do |a, b|
  a[:from] <=> b[:from]
end

zip_content_unpacked = Array.new(responses.last[:to])
responses.each do |response|
  zip_content_unpacked[response[:from]..response[:to]] = response[:value]
end

zip_content = [zip_content_unpacked.join].pack("H*")
File.open(path, "w") { |f| f.write(zip_content) }
