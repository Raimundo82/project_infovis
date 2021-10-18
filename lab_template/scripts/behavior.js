var dataSet;

function init() {
    d3.json('data/data.json')
        .then((data) => {
            dataSet = data;
            //createBarChart(data, false);
            //createScatterPlot(data, false);
            //createLineChart(data, false);
            //createBoxPlot(data, false);
            //createPieChart(data, false);
            createBowlFruit();
        })
        .catch((error) => {
            console.log(error);
        });
}

function createBarChart(data, update) {
    width = 400;

    height = 400;

    margin = { top: 20, right: 20, bottom: 20, left: 40 };

    data = data.filter(function(d) {
        if (d.budget > 0) {
            return d;
        }
    });

    x = d3
        .scaleLinear()
        .domain([0, 10])
        .range([margin.left, width - margin.right]);

    y = d3
        .scaleBand()
        .domain(d3.range(data.length))
        .rangeRound([margin.top, height - margin.bottom])
        .padding(0.5);

    function xAxis(g) {
        g.attr('transform', `translate(0,${margin.top})`).call(d3.axisTop(x));
    }

    function yAxis(g) {
        g.attr('transform', `translate(${margin.left},0)`).call(
            d3
            .axisLeft(y)
            .tickFormat((i) => {
                if (data[i].oscar_year % 3 == 0) return data[i].oscar_year;
            })
            .tickSizeOuter(0)
        );
    }

    if (!update) {
        d3.select('div#barChart').append('svg').append('g').attr('class', 'bars');
    }

    const svg = d3
        .select('div#barChart')
        .select('svg')
        .attr('width', width)
        .attr('height', height);

    svg
        .select('g.bars')
        .selectAll('rect')
        .data(data, function(d) {
            return d.oscar_year;
        })
        .join(
            (enter) => {
                return enter
                    .append('rect')
                    .attr('x', x(0))
                    .attr('y', (d, i) => y(i))
                    .attr('width', (d) => x(d.rating) - x(0))
                    .attr('height', y.bandwidth())
                    .style('fill', calculateFill)
                    .on('mouseover', handleMouseOver)
                    .on('mouseleave', handleMouseLeave)
                    .on('click', handleClick)
                    .transition()
                    .duration(2000)
                    .style('opacity', '100%');
            },
            (update) => {
                update
                    .transition()
                    .duration(1000)
                    .attr('width', (d) => x(d.rating) - x(0))
                    .attr('height', y.bandwidth())
                    .style('fill', calculateFill)
                    .attr('x', x(0))
                    .attr('y', (d, i) => y(i));
            },
            (exit) => {
                return exit.remove();
            }
        );

    if (!update) {
        svg.append('g').attr('class', 'xAxis');
        svg.append('g').attr('class', 'yAxis');
    }

    d3.select('g.xAxis').call(xAxis);
    d3.select('g.yAxis').call(yAxis);
}

function createScatterPlot(data, update) {
    width = 400;

    height = 400;

    margin = { top: 20, right: 20, bottom: 20, left: 40 };

    data = data.filter(function(d) {
        if (d.budget > 0) {
            return d;
        }
    });

    x = d3
        .scaleLog()
        .domain([0.1, d3.max(data, (d) => d.budget)])
        .nice()
        .range([margin.left, width - margin.right]);

    y = d3
        .scaleLinear()
        .domain([0, 10])
        .range([height - margin.bottom, margin.top]);

    xAxis = (g) =>
        g
        .attr('transform', `translate(0,${height - margin.bottom})`)
        .call(
            d3
            .axisBottom(x)
            .tickFormat((x) => x / 1000000)
            .ticks(5)
        )
        .call((g) => g.select('.domain').remove());

    yAxis = (g) =>
        g
        .attr('transform', `translate(${margin.left},0)`)
        .call(d3.axisLeft(y))
        .call((g) => g.select('.domain').remove());

    grid = (g) =>
        g
        .attr('stroke', 'currentColor')
        .attr('stroke-opacity', 0.1)
        .call((g) =>
            g
            .append('g')
            .selectAll('line')
            .data(x.ticks())
            .join('line')
            .attr('x1', (d) => 0.5 + x(d))
            .attr('x2', (d) => 0.5 + x(d))
            .attr('y1', margin.top)
            .attr('y2', height - margin.bottom)
        )
        .call((g) =>
            g
            .append('g')
            .selectAll('line')
            .data(y.ticks())
            .join('line')
            .attr('y1', (d) => 0.5 + y(d))
            .attr('y2', (d) => 0.5 + y(d))
            .attr('x1', margin.left)
            .attr('x2', width - margin.right)
        );

    if (!update) {
        d3.select('div#scatterPlot')
            .append('svg')
            .append('g')
            .attr('class', 'circles')
            .style('stroke-width', 1.5);
    }

    const svg = d3
        .select('div#scatterPlot')
        .select('svg')
        .attr('width', width)
        .attr('height', height);

    svg
        .select('g.circles')
        .selectAll('circle')
        .data(data, function(d) {
            return d.oscar_year;
        })
        .join(
            (enter) => {
                return enter
                    .append('circle')
                    .attr('cx', (d) => x(d.budget))
                    .attr('cy', (d) => y(d.rating))
                    .attr('r', calculateRadius)
                    .style('fill', 'steelblue')
                    .on('mouseover', handleMouseOver)
                    .on('mouseleave', handleMouseLeave)
                    .on('click', handleClick)
                    .transition()
                    .duration(1000)
                    .style('opacity', '100%');
            },
            (update) => {
                update
                    .transition()
                    .duration(1000)
                    .attr('cx', (d) => x(d.budget))
                    .attr('cy', (d) => y(d.rating))
                    .attr('r', calculateRadius)
                    .style('fill', 'steelblue');
            },
            (exit) => {
                exit.remove();
            }
        );

    if (!update) {
        svg.append('g').attr('class', 'scatterXAxis');
        svg.append('g').attr('class', 'scatterYAxis');
        svg.append('g').attr('class', 'scatterGrid').call(grid);
    } else {}
    d3.select('g.scatterXAxis').call(xAxis);
    d3.select('g.scatterYAxis').call(yAxis);
}

function createLineChart(data, update) {
    margin = { top: 20, right: 20, bottom: 20, left: 40 };

    data = data.filter(function(d) {
        if (d.budget > 0) {
            return d;
        }
    });

    line = d3
        .line()
        .defined(function(d) {
            return d.budget > 0;
        })
        .x((d) => x(d.year))
        .y((d) => y(d.budget));

    x = d3
        .scaleLinear()
        .domain(d3.extent(data, (d) => d.year))
        .range([margin.left, width - margin.right]);

    y = d3
        .scaleLinear()
        .domain([0, d3.max(data, (d) => d.budget)])
        .range([height - margin.bottom, margin.top]);

    xAxis = (g) =>
        g.attr('transform', `translate(0,${height - margin.bottom})`).call(
            d3
            .axisBottom(x)
            .tickFormat((x) => x)
            .tickSizeOuter(0)
        );

    yAxis = (g) =>
        g
        .attr('transform', `translate(${margin.left},0)`)
        .call(d3.axisLeft(y).tickFormat((x) => x / 1000000))
        .call((g) => g.select('.domain').remove());

    if (!update) {
        d3.select('div#lineChart')
            .append('svg')
            .append('g')
            .attr('class', 'line')
            .append('path');
    }

    const svg = d3
        .select('div#lineChart')
        .select('svg')
        .attr('width', width)
        .attr('height', height);

    if (!update) {
        svg.append('g').attr('class', 'lineXAxis');
        svg.append('g').attr('class', 'lineYAxis');
    }

    svg.select('g.lineXAxis').call(xAxis);

    svg.select('g.lineYAxis').call(yAxis);

    svg
        .select('path')
        .datum(data)
        .attr('fill', 'none')
        .attr('stroke', 'steelblue')
        .attr('stroke-width', 1.5)
        .attr('stroke-linejoin', 'round')
        .attr('stroke-linecap', 'round')
        .transition()
        .duration(1000)
        .attr('d', line);

    svg
        .select('g.line')
        .selectAll('circle')
        .data(data, function(d) {
            return d.oscar_year;
        })
        .join(
            (enter) => {
                return enter
                    .append('circle')
                    .attr('cx', (d) => x(d.year))
                    .attr('cy', (d) => y(d.budget))
                    .attr('r', 3)
                    .style('fill', 'steelblue')
                    .text(function(d) {
                        return d.title;
                    })
                    .on('mouseover', handleMouseOver)
                    .on('mouseleave', handleMouseLeave)
                    .on('click', handleClick)
                    .transition()
                    .duration(1000)
                    .style('opacity', '100%');
            },
            (update) => {
                update
                    .transition()
                    .duration(1000)
                    .attr('cx', (d) => x(d.year))
                    .attr('cy', (d) => y(d.budget))
                    .attr('r', 3)
                    .style('fill', 'steelblue');
            },
            (exit) => {
                exit.remove();
            }
        );
}

function createBoxPlot(data, update) {
    width = 400;
    height = 400;

    xCenter = margin.left + (width - margin.left - margin.right) / 2;

    margin = { top: 20, right: 20, bottom: 20, left: 40 };

    ratingData = data.map((o) => o.rating);

    xScale = xCenter;

    const boxStats = computeBoxStats(ratingData);
    const outliers = data.filter(
        (d) => d.rating < boxStats.min || d.rating > boxStats.max
    );

    const yScale = d3
        .scaleLinear()
        .domain([5, 10])
        .range([height - margin.bottom, margin.top]);

    if (!update) {
        d3.select('#boxPlot')
            .append('svg')
            .attr('width', width)
            .attr('height', height)
            .append('g')
            .attr('class', 'box')
            .attr('transform', `translate(${margin.left},0)`);
    }

    const box = d3.select('g.box');

    box.call(d3.axisLeft(yScale));

    // Show the main vertical line
    if (!update) {
        box
            .append('line')
            .attr('x1', xCenter)
            .attr('x2', xCenter)
            .attr('y1', yScale(boxStats.min))
            .attr('y2', yScale(boxStats.max))
            .attr('id', 'lineVertical')
            .attr('stroke', 'black');
    }

    d3.select('#lineVertical')
        .transition()
        .duration(1000)
        .attr('y1', yScale(boxStats.min))
        .attr('y2', yScale(boxStats.max));

    // Show the box
    if (!update) {
        box
            .append('rect')
            .attr('x', xCenter - 50)
            .attr('y', yScale(boxStats.q3))
            .attr('height', yScale(boxStats.q1) - yScale(boxStats.q3))
            .attr('width', 100)
            .attr('stroke', 'black')
            .attr('id', 'rectBox')
            .style('fill', 'steelblue');
    }

    d3.select('#rectBox')
        .transition()
        .duration(1000)
        .attr('y', yScale(boxStats.q3))
        .attr('height', yScale(boxStats.q1) - yScale(boxStats.q3));

    // show median, min and max horizontal lines

    if (!update) {
        box
            .selectAll('toto')
            .data([boxStats.min, boxStats.median, boxStats.max])
            .enter()
            .append('line')
            .attr('class', 'stats')
            .attr('x1', xCenter - 50)
            .attr('x2', xCenter + 50)
            .attr('y1', (d) => yScale(d))
            .attr('y2', (d) => yScale(d))
            .attr('stroke', 'black');
    }

    if (update) {
        i = 0;
        arr = [boxStats.min, boxStats.median, boxStats.max];
        d3.selectAll('.stats').each(function(d) {
            d3.select(this)
                .transition()
                .duration(1000)
                .attr('y1', yScale(arr[i]))
                .attr('y2', yScale(arr[i++]));
        });
    }

    box
        .selectAll('circle')
        .data(outliers, (d) => d.rating)
        .join(
            (enter) => {
                return enter
                    .append('circle')
                    .attr('cy', (d) => yScale(d.rating))
                    .attr('cx', xCenter)
                    .attr('r', 4)
                    .style('fill', 'steelblue')
                    .text((d) => d.title)
                    .on('mouseover', handleMouseOver)
                    .on('mouseleave', handleMouseLeave)
                    .on('click', handleClick)
                    .transition()
                    .duration(1000)
                    .style('opacity', '100%');
            },
            (update) => {
                update
                    .transition()
                    .duration(1000)
                    .attr('cy', (d) => yScale(d.rating))
                    .attr('cx', xCenter)
                    .attr('r', 4)
                    .style('fill', 'steelblue');
            },
            (exit) => {
                exit.remove();
            }
        );
}

function createPieChart(data, update) {
    const width = 400;
    const height = 400;
    const margin = 20;

    const radius = width / 2 - margin;

    var svg = d3
        .select('#pieChart')
        .append('svg')
        .attr('width', width)
        .attr('height', height)
        .append('g')
        .attr('transform', `translate(${width / 2}, ${height / 2})`);

    const lower = data.filter((d) => d.budget > 0 && d.budget < 5000000).length;
    const upper = data.filter((d) => d.budget > 0 && d.budget >= 5000000).length;
    pieData = [lower, upper];

    var color = d3.scaleOrdinal().domain(pieData).range(['red', 'green']);
    var text = d3
        .scaleOrdinal()
        .domain(pieData)
        .range([
            `< 5000000 =>
            ${Math.round((pieData[0] / (pieData[0] + pieData[1])) * 100)} %`,
            `>= 5000000 => 
            ${Math.round((pieData[1] / (pieData[0] + pieData[1])) * 100)} %`,
        ]);

    const pie = d3.pie();

    const arc = (r) => d3.arc().innerRadius(0).outerRadius(r);

    svg
        .selectAll('whatever')
        .data(pie(pieData))
        .enter()
        .append('path')
        .attr('d', arc(radius))
        .attr('fill', color)
        .attr('stroke', 'black')
        .style('stroke-width', '2px')
        .style('opacity', 0.7);

    svg
        .selectAll('whatever')
        .data(pie(pieData))
        .enter()
        .append('text')
        .text(text)
        .attr('transform', (d) => `translate(${arc(radius).centroid(d)})`)
        .style('text-anchor', 'middle')
        .style('font-size', 17);
}

function createBowlFruit(data, update) {
    width = 500;
    height = 400;
    const svg = d3
        .select('#bowlFruit')
        .append('svg')
        .attr('width', width)
        .attr('height', height);

    const colorScale = d3
        .scaleOrdinal()
        .domain(['apple', 'lemon'])
        .range(['#45cc33', 'yellow']);

    const sizeScale = d3
        .scaleOrdinal()
        .domain(['apple', 'lemon'])
        .range([50, 30]);

    const xPos = (d, i) => i * 100 + 50;

    const render = (selection, { fruits }) => {
        const groups = selection.selectAll('g').data(fruits);

        const groupsEnter = groups.enter().append('g');
        groupsEnter
            .merge(groups)
            .attr('transform', (d, i) => `translate(${i * 100 + 50},${height / 2})`);

        groups.exit().remove();

        groupsEnter
            .append('circle')
            .merge(groups.select('circle'))
            .attr('r', (d) => sizeScale(d.type))
            .style('fill', (d) => colorScale(d.type));

        groupsEnter
            .append('text')
            .merge(groups.select('text'))
            .attr('y', 75)
            .text((d) => d.type);
    };

    const makeFruit = (type) => ({ type, id: Math.random() });

    let fruits = d3.range(5).map(() => makeFruit('apple'));

    render(svg, { fruits });

    setTimeout(() => {
        fruits.pop();
        render(svg, { fruits });
    }, 1000);

    setTimeout(() => {
        fruits[2].type = 'lemon';
        render(svg, { fruits });
    }, 2000);

    setTimeout(() => {
        fruits = fruits.filter((d, i) => i !== 1);
        render(svg, { fruits });
    }, 3000);
}

// New Code

function dataChange(value) {
    d3.json('data/data.json')
        .then((data) => {
            newData = data;
            switch (value) {
                case 'new':
                    newData = data.filter(function(d) {
                        if (d.year >= 1972) {
                            return d;
                        }
                    });
                    break;
                case 'old':
                    newData = data.filter(function(d) {
                        if (d.year < 1972) {
                            return d;
                        }
                    });
                    break;
                case 'adj':
                    newData = data;
                    newData.forEach((d) => (d.budget = d.budget_adj));
                    break;
                default:
                    break;
            }
            createBarChart(newData, true);
            createScatterPlot(newData, true);
            createLineChart(newData, true);
            createBoxPlot(newData, true);
        })
        .catch((error) => {
            console.log(error);
        });
}

function handleMouseOver(event, d) {
    barChart = d3.select('div#barChart').select('svg');

    scatterPlot = d3.select('div#scatterPlot').select('svg');

    lineChart = d3.select('div#lineChart').select('svg');

    boxPlot = d3.select('div#boxPlot').select('svg');

    barChart
        .selectAll('rect')
        .filter(function(b) {
            if (d.oscar_year == b.oscar_year) {
                return b;
            }
        })
        .style('fill', 'red');

    scatterPlot
        .selectAll('circle')
        .filter(function(b) {
            if (d.oscar_year == b.oscar_year) {
                return b;
            }
        })
        .style('fill', 'red');

    lineChart
        .selectAll('circle')
        .filter(function(b) {
            if (d.oscar_year == b.oscar_year) {
                return b;
            }
        })
        .style('fill', 'red');

    boxPlot
        .selectAll('circle')
        .filter(function(b) {
            if (d.oscar_year == b.oscar_year) {
                return b;
            }
        })
        .style('fill', 'red');
}

function handleMouseLeave(event, d) {
    d3.select('div#barChart')
        .select('svg')
        .selectAll('rect')
        .style('fill', calculateFill);

    d3.select('div#scatterPlot')
        .select('svg')
        .selectAll('circle')
        .style('fill', 'steelblue');

    d3.select('div#lineChart')
        .select('svg')
        .selectAll('circle')
        .style('fill', 'steelblue');

    d3.select('div#boxPlot')
        .select('svg')
        .selectAll('circle')
        .style('fill', 'steelblue');
}

function handleClick(event, d) {
    window.alert(d.title);
}

function calculateFill(dataItem, i) {
    var scale = d3
        .scaleLinear()
        .domain([1, d3.max(dataSet, (d) => d.budget)])
        .range([0, 1]);
    return d3.interpolateBlues(scale(dataItem.budget));
    // return "steelblue";
}

function calculateRadius(dataItem, i) {
    var scale = d3
        .scaleLinear()
        .domain([d3.min(dataSet, (d) => d.year), d3.max(dataSet, (d) => d.year)])
        .range([0, 10]);
    return scale(dataItem.year);
}

function computeBoxStats(data) {
    const box = {};
    data_sorted = data.sort(d3.ascending);
    box['q1'] = d3.quantile(data_sorted, 0.25);
    box['median'] = d3.quantile(data_sorted, 0.5);
    box['q3'] = d3.quantile(data_sorted, 0.75);
    const interQuantileRange = box.q3 - box.q1;
    box['min'] = box.q1 - 1.5 * interQuantileRange;
    box['max'] = box.q1 + 1.5 * interQuantileRange;
    return box;
}