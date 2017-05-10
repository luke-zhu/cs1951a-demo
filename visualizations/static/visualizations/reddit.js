// Dimensions
let margin = { left: 100, right: 100, top: 100, bottom: 100 };
let width = 1000 - margin.left - margin.right;
let height = 500 - margin.top - margin.bottom;

// Scales
let x = d3.scaleBand()
  .rangeRound([0, width])
  .padding(0.1);
let y = d3.scaleLinear()
  .range([height, 0]);

// SVG
let svg = d3.select('#chart')
  .append('svg')
  .attr('width', width + margin.left + margin.right)
  .attr('height', height + margin.top + margin.bottom)
  .append('g')
  .attr('transform', `translate(${margin.left},${margin.top})`);

d3.json('static/visualizations/data.json', (error, data) => {
  if (error) throw error;
  // Scale domains
  x.domain(data.map(d => d[0]))
  y.domain([0, d3.max(data, d => d[1])])
  
  // Data
  svg.selectAll('.bar')
    .data(data)
    .enter()
    .append('g')
    .attr('class', 'bars')
    .append('rect')
    .attr('class', 'bar')
    .attr('x', d => x(d[0]))
    .attr('y', d => y(d[1]))
    .attr('width', x.bandwidth())
    .attr('height', d => height - y(d[1]));
  
  // Axes
  svg.append('g')
    .attr('class', 'x axis')
    .attr('transform', `translate(0, ${height})`)
    .call(d3.axisBottom(x));
  svg.append('g')
    .attr('class', 'y axis')
    .call(d3.axisLeft(y));
   
  // Labels
  svg.append('text')
    .attr('class', 'title label')
    .attr('x', width / 2)
    .attr('y', -margin.left / 2)
    .attr('text-anchor', 'middle')
    .text('TITLE');
  svg.append('text')
    .attr('class', 'x label')
    .attr('x', width / 2)
    .attr('y', height + margin.bottom / 2)
    .attr('text-anchor', 'middle')
    .text('X LABEL');
  svg.append('text')
    .attr('class', 'y label')
    .attr('x', -height / 2)
    .attr('y', -margin.top / 2)
    .attr('transform', `rotate(-90)`)
    .text('Y LABEL');
});
