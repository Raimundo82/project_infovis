using DataFrames
using CSV
using Statistics

function explode(df::AbstractDataFrame, col::String; delimeter=",")
    new_df = empty(df)
    for row in eachrow(df)
        items = split(row[col], delimeter)
        for item in items
            arr = Vector{Any}()
            push!(arr, row[1], row[2])
            push!(arr, item)
            push!(arr, row[4:end]...)
            push!(new_df, arr)
        end
    end
    new_df
end

function derived_measures(df, array)
    if length(df) > 0

end

path = "project_datasets/global/"
tracks = DataFrame(CSV.File(path * "global_tracks_2017_2020.csv"))
tracks_metrics = DataFrame(CSV.File(path * "tracks_derived_measures.csv"))
artists = DataFrame(CSV.File(path * "global_artists_2017_2020.csv"))

tracks = explode(tracks, "artist_id")

