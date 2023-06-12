
local counter = 1
local threads = {}
local interval = 60000

function setup(thread)
    thread:set("id", counter)
    table.insert(threads, thread)
    counter = counter + 1
end

function init(args)
    cnt = 1
    math.randomseed(id)
end

function request()


    cnt = cnt + 1
    local method = "GET"
    local path = "/hi"
    local headers = {}
    headers["Content-Type"] = "Content-Type: application/json"
    local body =  "{}"

    return wrk.format(method, path, headers, body)

end

