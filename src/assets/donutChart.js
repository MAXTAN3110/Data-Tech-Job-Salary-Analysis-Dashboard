// assets/donutChart.js
window.dashComponents = window.dashComponents || {};

window.dashComponents.DonutChart = function (props) {
    if (typeof d3 === "undefined") {
        console.error("D3 is not loaded");
        return document.createElement("div");
    }

    const el = document.createElement("div");

    // Extract props with defaults
    const {
        width = 700,
        height = 200,
        data = [],
        centerText,
        padAngle = 0.02,
        inflextionPadding = 20,
    } = props;

    const MARGIN_X = 100;
    const MARGIN_Y = 20;
    const radius = Math.min(width - 2 * MARGIN_X, height - 2 * MARGIN_Y) / 2;
    const innerRadius = radius * 0.9;
    const outerRadius = radius;

    // Create SVG
    const svg = d3
        .select(el)
        .append("svg")
        .attr("height", "100%")
        .attr("width", "100%")
        .attr("viewBox", `0 0 ${width} ${height}`)
        .attr("preserveAspectRatio", "xMinYMin meet")
        .append("g")
        .attr("transform", `translate(${width / 2},${height / 2 - 10})`);

    // Color scale
    const color = d3
        .scaleOrdinal()
        .domain(data.map((d) => d.label))
        .range(d3.schemeCategory10);

    // Create pie layout
    const pie = d3
        .pie()
        .value((d) => d.value)
        .sort(null)
        .padAngle(padAngle);

    // Create arc generator
    const arc = d3.arc().innerRadius(innerRadius).outerRadius(outerRadius);

    const sliceGroups = svg
        .selectAll("g.slice")
        .data(pie(data))
        .enter()
        .append("g")
        .attr("class", "slice");

    // Add slices
    const slices = sliceGroups
        .append("path")
        .attr("d", arc)
        .attr("fill", (d) => color(d.data.label))
        .style("transition", "all 0.3s")
        .style("cursor", "pointer");

    // Add the labels and lines
    sliceGroups.each(function (d) {
        const group = d3.select(this);
        const centroid = arc.centroid(d);

        // Calculate inflexion point
        const inflexionArc = d3
            .arc()
            .innerRadius(radius + inflextionPadding)
            .outerRadius(radius + inflextionPadding);
        const inflexionPoint = inflexionArc.centroid(d);

        // Determine if label should be on right or left
        const isRightLabel = inflexionPoint[0] > 0;
        const labelPosX = inflexionPoint[0] + 1 * (isRightLabel ? 1 : -1);
        const textAnchor = isRightLabel ? "start" : "end";

        // Create lines
        group
            .append("line")
            .attr("x1", centroid[0])
            .attr("y1", centroid[1])
            .attr("x2", inflexionPoint[0])
            .attr("y2", inflexionPoint[1]);

        group
            .append("line")
            .attr("x1", inflexionPoint[0])
            .attr("y1", inflexionPoint[1])
            .attr("x2", labelPosX)
            .attr("y2", inflexionPoint[1]);

        // Add label
        const labelGroup = group
            .append("g")
            .attr(
                "transform",
                `translate(${labelPosX + (isRightLabel ? 2 : -2)}, ${
                    inflexionPoint[1]
                })`
            )
            .style("cursor", "pointer");

        // Add the icon
        labelGroup
            .append("foreignObject")
            .attr("width", "1.5em")
            .attr("height", "2em")
            .attr("x", isRightLabel ? 0 : -20) // Adjust position based on label alignment
            .attr("y", "-1em") // Center vertically
            .html(
                (d) =>
                    `<i class="iconify" data-icon="${
                        d.data.icon || "mdi:folder"
                    }" style="font-size: 1.3em;"></i>`
            );

        // Add the text
        const label = `${d.data.label}`;
        labelGroup
            .append("text")
            .attr("x", isRightLabel ? 25 : -25) // Offset text to make room for icon
            .attr("text-anchor", textAnchor)
            .attr("dominant-baseline", "middle")
            .attr("font-size", "1em")
            .text(label);
    });

    // Add hover effects
    sliceGroups
        .on("mouseover", function (event, d) {
            const slice = d3.select(this).select("path");
            slice.transition().duration(200).attr("d", arc);

            sliceGroups
                .filter((s) => s !== d)
                .transition()
                .duration(200)
                .style("opacity", 0.3);
        })
        .on("mouseout", function (event, d) {
            const slice = d3.select(this).select("path");
            slice.transition().duration(200).attr("d", arc).style("opacity", 1);

            sliceGroups
                .filter((s) => s !== d)
                .transition()
                .duration(200)
                .style("opacity", 1.0);
        })
        .on("click", function (event, d) {
            if (d.data.path) {
                window.location.pathname = d.data.path;
            }
        });

    // Add center text
    const icon = "game-icons:money-stack";
    svg
        .append("foreignObject")
        .attr("x", -40) // Adjust position to center
        .attr("y", -30) // Adjust position to center
        .attr("width", 150)
        .attr("height", 100)
        .append("xhtml:div")
        .style("text-align", "left")
        .style("font-family", "Roboto").html(`
            <span>Key Factors</span> <br>
            <span>of Salary</span>
            <span class="iconify" data-icon="${icon}" style="font-size: 25px; color: #1bab02;"></span>
        `);

    return el;
};
