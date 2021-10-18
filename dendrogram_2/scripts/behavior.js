var width = 960;
var height = 2400;

function init() {
    d3.csv('/project_infovis/dendrogram_2/data/h_data.csv')
        .then(function(data) {
            createTreeMap(data);
        })
        .catch((error) => {
            console.log(error);
        });
}

function createTreeMap(data) {
    const strat = d3
        .stratify()
        .parentId((d) => d.parent)
        .id((d) => d.child);

    const root = tree(strat(data));
    var svg = d3
        .select('#tree')
        .append('svg')
        .attr('width', '100%')
        .attr('height', height);

    svg
        .append('g')
        .attr('fill', 'none')
        .attr('stroke', '#555')
        .attr('stroke-opacity', 0.4)
        .attr('stroke-width', 1.5)
        .selectAll('path')
        .data(root.links())
        .join('path')
        .attr(
            'd',
            (d) => `
            M${d.target.y},${d.target.x}
            C${d.source.y + root.dy / 2},${d.target.x}
             ${d.source.y + root.dy / 2},${d.source.x}
             ${d.source.y},${d.source.x}
          `
        );

    svg
        .append('g')
        .selectAll('circle')
        .data(root.descendants())
        .join('circle')
        .attr('cx', (d) => d.y)
        .attr('cy', (d) => d.x)
        .attr('fill', (d) => (d.children ? '#555' : '#999'))
        .attr('r', 2.5);

    svg
        .append('g')
        .attr('font-family', 'sans-serif')
        .attr('font-size', 10)
        .attr('stroke-linejoin', 'round')
        .attr('stroke-width', 3)
        .selectAll('text')
        .data(root.descendants())
        .join('text')
        .attr('x', (d) => d.y)
        .attr('y', (d) => d.x)
        .attr('dy', '0.31em')
        .attr('dx', (d) => (d.children ? -6 : 6))
        .text((d) => d.data.id)
        .filter((d) => d.children)
        .attr('text-anchor', 'end')
        .clone(true)
        .lower()
        .attr('stroke', 'white');

    svg.attr('viewBox', autoBox);
}

const tree = (data) => {
    const root = d3
        .hierarchy(data)
        .sort(
            (a, b) => d3.descending(a.height, b.height) || d3.ascending(a.id, b.id)
        );
    console.log(root);
    root.dx = 10;
    root.dy = 400;
    return d3.cluster().nodeSize([root.dx, root.dy])(root);
};

function autoBox() {
    const { x, y, width, height } = this.getBBox();
    return [x, y, width, height];
}