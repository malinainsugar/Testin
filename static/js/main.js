
let pictures = document.querySelectorAll('.graph');
let diagram = document.querySelector('.diagram');
let histogram = document.querySelector('.histogram');

let idGraph = 2015;
function createIDGraph () {
  return idGraph++;
}

const loadDiagram = () => {
    pictures.forEach((picture) => {
        console.log(picture);
        picture.src = `/static/img/pieCharts/skills${createIDGraph()}.png`;
    })
    idGraph = 2015;
};

const loadHistogram = () => {
    pictures.forEach((picture) => {
        console.log(picture);
        picture.src = `/static/img/histograms/skills${createIDGraph()}.png`;
    })
    idGraph = 2015;
};

const ready = () => {
    diagram.addEventListener('click', loadDiagram);
    histogram.addEventListener('click', loadHistogram);
};

const closePage = () => {
    diagram.removeEventListener('click', loadDiagram);
    histogram.removeEventListener('click', loadHistogram);
    document.removeEventListener("DOMContentLoaded", ready);
    window.removeEventListener("unload", closePage);
}

document.addEventListener("DOMContentLoaded", ready);
window.addEventListener("unload", closePage);

