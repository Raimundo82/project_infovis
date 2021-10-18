data =
    'https://raw.githubusercontent.com/holtzy/data_to_viz/master/Example_dataset/5_OneCatSevNumOrdered_wide.csv';

function init() {
    d3.csv(data)
        .then((data) => {
            createStack(data);
        })
        .catch((error) => {
            d;
            console.log(error);
        });
}

function createStack(data) {
    var keys = data.columns.slice(1);

    const margin = { top: 20, right: 30, bottom: 30, left: 55 },
        width = 460 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    const svg = d3
        .select('#stack')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left}, ${margin.top})`);

    var x = d3
        .scaleLinear()
        .domain(d3.extent(data, (d) => d.year))
        .range([0, width]);
    svg
        .append('g')
        .attr('transform', `translate(0, ${height})`)
        .call(d3.axisBottom(x).ticks(5));

    var y = d3.scaleLinear().domain([0, 200000]).range([height, 0]);
    svg.append('g').call(d3.axisLeft(y));

    var color = d3
        .scaleOrdinal()
        .domain(keys)
        .range([
            '#e41a1c',
            '#377eb8',
            '#4daf4a',
            '#984ea3',
            '#ff7f00',
            '#ffff33',
            '#a65628',
            '#f781bf',
        ]);

    function areaGen(data) {
        return d3
            .area()
            .x((d, i) => x(d.data.year))
            .y0((d) => y(d[0]))
            .y1((d) => y(d[1]));
    }

    var stackedData = d3.stack().keys(keys)(data);
    svg
        .selectAll('mylayers')
        .data(stackedData)
        .enter()
        .append('path')
        .style('fill', (d) => color(d.key))
        .attr('d', areaGen(data));
}