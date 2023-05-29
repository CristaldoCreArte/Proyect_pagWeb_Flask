const carrusel = document.querySelector(".carrusel-items");
let intervalo = null;
let velocidad = .5;
let maxScrollLeft = carrusel.scrollWidth - carrusel.clientWidth;

const start = () =>{
    intervalo = setInterval(function(){
        carrusel.scrollLeft = carrusel.scrollLeft + velocidad;
        if (carrusel.scrollLeft  === maxScrollLeft){
            velocidad = -1;
        }else if(carrusel.scrollLeft === 0){
            velocidad = 1;
        }
    },10);
};
start();
const stop = () => {
    clearInterval(intervalo);
};
carrusel.addEventListener('mouseover', () => {
    stop();
})

carrusel.addEventListener('mouseout', () => {
    start();
})
