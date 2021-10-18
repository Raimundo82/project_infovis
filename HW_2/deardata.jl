using DataFrames
using CSV
using Statistics
using Dates

function getDayOfWeek(date::String; dateformat="y-m-d")
    df = DateFormat(dateformat)
    day = dayofweek(Date("2021-10-03", dateformat))
    day, weekdays[day]
end

weekdays = Dict(
    1 => "Mon",
    2 => "Tue",
    3 => "Wed",
    4 => "Thu",
    5 => "Fri",
    6 => "Sat",
    7 => "Sun",
)

day_name(x) = weekdays[x] 

data = DataFrame(CSV.File("project_datasets/global/global_tracks_2017_2020.csv"))

describe(data)