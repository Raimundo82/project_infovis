function init() {
    d3.csv('data/data.csv').then((data) => {
        data.forEach((d) => {
            d.Year = new Date(d.Year);
            d.Total = +d.Total;
        });
        console.log(data);
        createLineChart(data);
    });
}

function createLineChart(data) {
    const width = 500;
    const height = 500;
    const margin = { top: 20, bottom: 20, right: 20, left: 40 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    const xValue = (d) => d.Year;
    const yValue = (d) => d.Total;

    const xScale = d3
        .scaleTime()
        .domain(d3.extent(data, xValue))
        .range([0, innerWidth]);

    const yScale = d3
        .scaleLinear()
        .domain([0, d3.max(data, yValue)])
        .range([innerHeight, 0])
        .nice();

    const xAxis = d3
        .axisBottom(xScale)
        .tickSize(-height + margin.top + margin.bottom)
        .tickPadding(10);

    const yAxis = d3
        .axisLeft(yScale)
        .tickPadding(10)
        .tickSize(-width + margin.right + margin.left);

    const svg = d3
        .select('#arrestsNW')
        .append('svg')
        .attr('class', 'lineChart')
        .attr('width', width)
        .attr('height', height);

    const g = svg
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    const xAxisG = g
        .append('g')
        .call(xAxis)
        .attr('transform', `translate(0,${innerHeight})`);

    xAxisG.selectAll('.domain').remove();
    xAxisG.selectAll('line').attr('opacity', 0.3);

    const yAxisG = g.append('g').call(yAxis);
    yAxisG.selectAll('line').attr('opacity', 0.3);
    yAxisG.selectAll('.domain').remove();

    line = d3
        .area()
        .x((d) => xScale(xValue(d)))
        .y0(innerHeight)
        .y1((d) => yScale(yValue(d)))
        .curve(d3.curveBasis);

    g.append('path').attr('class', 'line-path').datum(data).attr('d', line);
}