const START_YEAR = 2015
let containerGraphics = document.querySelector('.graphics');

for (var year = START_YEAR; year <= 2022; year++) {
    const image = document.createElement('img');
    image.src  = `/static/img/histograms/skills${year}.png`;
    image.height = 200;
    image.classList.add('graph');
    image.alt = `График навыков ${year} года`
    containerGraphics.appendChild(image)
}

let pictures = document.querySelectorAll('.graph');
let diagram = document.querySelector('.diagram');
let histogram = document.querySelector('.histogram');

let idGraph = START_YEAR;
function createIDGraph () {
  return idGraph++;
}

const loadDiagram = () => {
    pictures.forEach((picture) => {
        console.log(picture);
        picture.src = `/static/img/pieCharts/skills${createIDGraph()}.png`;
    })
    idGraph = START_YEAR;
};

const loadHistogram = () => {
    pictures.forEach((picture) => {
        console.log(picture);
        picture.src = `/static/img/histograms/skills${createIDGraph()}.png`;
    })
    idGraph = START_YEAR;
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

