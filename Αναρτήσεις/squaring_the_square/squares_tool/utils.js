// window.onload = init();

let plusOrMinus = false;

function init() {
    const formulaItems = 4;
    const formulae = ["$$\\sin x$$", "$$\\cos 2x$$", "$$\\cos 3x$$", "$$2\\sin x$$", "$$-3\\tan x$$", "$$\\sin(x-2)$$", "$$e^{2x}$$", "$$x^3$$", "$$x^5$$", "$$\\sin x$$", "$$\\cos 2x$$", "$$\\cos 3x$$", "$$2\\sin x$$", "$$-3\\tan x$$", "$$\\sin(x-2)$$", "$$e^{2x}$$", "$$x^3$$", "$$x^5$$", "$$\\sin(x-2)$$", "$$e^{2x}$$"];
    plotGraph();
    initFormula(formulaItems);
    initKeyboard(formulae);
}

function initKeyboard(formulae) { // Formulae: list of as many as you may wish
    const keyboardContainer = document.getElementById("keyboard-container");
    for (const formula of formulae) {
        const keyContainer = document.createElement("div");
        keyContainer.setAttribute("class", "key-container");
        const keyFormula = document.createElement("div");
        keyFormula.setAttribute("class", "key");
        keyFormula.innerHTML = formula;
        keyContainer.append(keyFormula);
        keyboardContainer.append(keyContainer);
    }
}

function initFormula(formulaItems) {
    const formulaContainer = document.getElementById("formula-container");
    for (let i=0; i<formulaItems; i++) {
        const formulaItemContainer = document.createElement("div");
        formulaItemContainer.setAttribute("class", "formula-item-container");
        const formulaItem = document.createElement("div");
        formulaItem.setAttribute("class", "formula-item");
        formulaItemContainer.append(formulaItem);
        formulaContainer.append(formulaItemContainer);
        if (i < formulaItems - 1) {
            const plusContainer = document.createElement("div");
            plusContainer.setAttribute("class", "formula-item-container");
            const plusItem = document.createElement("div");
            plusItem.innerHTML = "$$+$$";
            plusContainer.append(plusItem);
            formulaContainer.append(plusContainer);
        }
    }
}

function plotGraph() {
    const oX = 50;
    const oY = 50;
    const xEnd = 600;
    const nPoints = 1000;
    const a = 0;
    const b = 8;
    plotGrid(oX, xEnd, oY, a, b);
    drawAxes(oX, oY);
    drawCurve(testFunction, oX, xEnd, oY, nPoints, a, b);
}

function plotGrid(oX, xEnd, oY, a, b) { // Assumes that 0 <= a < b.
    const graphSvg = document.getElementById("graph-svg");
    const step = (xEnd - oX) / b;
    for (let i=oX+step; i<xEnd; i+=step) {
        addGridLinesX(graphSvg, i);
    }
    for (let i=oX-step; i>0; i-=step) {
        addGridLinesX(graphSvg, i);
    }
    for (let i=oY+step; i<xEnd; i+=step) {
        addGridLinesY(graphSvg, 600 - i);
    }
    for (let i=oY-step; i>0; i-=step) {
        addGridLinesY(graphSvg, 600 - i);
    }
}

function addGridLinesY(svgElement, i) {
    const gridLineY = document.createElementNS("http://www.w3.org/2000/svg", "line"); // y=y_0 lines.
    gridLineY.setAttribute("x1", "0");
    gridLineY.setAttribute("x2", "600");
    gridLineY.setAttribute("y1", i);
    gridLineY.setAttribute("y2", i);
    gridLineY.setAttribute("stroke", "#005f73");
    gridLineY.setAttribute("stroke-width", "0.5");
    svgElement.append(gridLineY);
}

function addGridLinesX(svgElement, i) {
    const gridLineX = document.createElementNS("http://www.w3.org/2000/svg", "line"); // x=x_0 lines.
    gridLineX.setAttribute("x1", i);
    gridLineX.setAttribute("x2", i);
    gridLineX.setAttribute("y1", "0");
    gridLineX.setAttribute("y2", "600");
    gridLineX.setAttribute("stroke", "#005f73");
    gridLineX.setAttribute("stroke-width", "0.5");
    svgElement.append(gridLineX);
}

function drawAxes(oX, oY) {
    const markerEnd = 6;
    const graphSvg = document.getElementById("graph-svg");
    const xAxis = document.createElementNS("http://www.w3.org/2000/svg", "line");
    const yAxis = document.createElementNS("http://www.w3.org/2000/svg", "line");
    xAxis.setAttribute("x1", 0);
    xAxis.setAttribute("x2", 600 - markerEnd);
    xAxis.setAttribute("y1", 600 - oY);
    xAxis.setAttribute("y2", 600 - oY);
    xAxis.setAttribute("stroke", "black");
    xAxis.setAttribute("stroke-width", "1.2");
    xAxis.setAttribute("marker-end", "url(#arrow)");
    yAxis.setAttribute("x1", oX);
    yAxis.setAttribute("x2", oX);
    yAxis.setAttribute("y1", 600);
    yAxis.setAttribute("y2", markerEnd);
    yAxis.setAttribute("stroke", "black");
    yAxis.setAttribute("stroke-width", "1.2");
    yAxis.setAttribute("marker-end", "url(#arrow)");
    graphSvg.append(xAxis);
    graphSvg.append(yAxis);
}

function drawCurve(f, oX, xEnd, oY, nPoints, a, b) { // Assumes that 0 <= a < b.
    const lambda = b / (xEnd - oX);
    const graphSvg = document.getElementById("graph-svg");
    const step = (xEnd - oX - a / lambda) / nPoints;
    let x, y;
    let points = "";
    for (let i=oX + a / lambda; i<xEnd; i+=step) {
        x = i - oX;
        y = 600 - oY - f(x * lambda) / lambda;
        points += i + "," + y + " ";
    }
    const plot = document.createElementNS("http://www.w3.org/2000/svg", "polyline");
    plot.setAttribute("points", points);
    plot.setAttribute("stroke", "#9b2226");
    plot.setAttribute("fill", "none");
    plot.setAttribute("stroke-width", "2");
    graphSvg.append(plot);
}

function testFunction(x) {
    return Math.sqrt(x)*Math.sin(x) + 2;
}