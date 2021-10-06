using DataFrames
using CSV
using Statistics

codes = DataFrame(CSV.File("country_codes.csv"))
codes = codes[!,["name", "alpha-2"]]

gdp = DataFrame(CSV.File("gdp_per_capita.csv"))
gdp = gdp[:,Not(:Info)]

years_cols = filter(x -> x !== "Country" ,names(gdp))

for y in years_cols
    replace!(gdp[!,y], ".." => "0")
    replace!(gdp[!,y], "" => "0")
    replace!(gdp[!,y], " " => "0")
    gdp[!,y] = parse.(Int, gdp[!,y])
end
    
insertcols!(gdp,"sum" => sum.(eachrow(gdp[:,2:end])))
years_cols = map(y -> Symbol(y),years_cols)
for s in years_cols
    gdp = gdp[:,Not(s)]
end

gdp
codes

out = innerjoin(codes, gdp, on = [:name => :Country])

out = out[:,Not(:name)]
sort!(out,["alpha-2"])
out = filter(row -> row.sum > 0, out)
CSV.write("out.csv", out)