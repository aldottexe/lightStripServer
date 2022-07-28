//site colors :)

colors = ["#f72585","#9B15F4","#6a83f1","#8EDEF6"]
mids = ["#7E106E","#3A0872","#3F37C9","#1060BC"]
darks = ["#5B0B4F","#4D0B99","#322CA0","0C4D97"]


let rand = Math.floor(Math.random()*4)
console.log(rand)

let heading = document.getElementsByTagName("h1")[0]
let sub = document.getElementsByTagName("h2")[0]
let body = document.getElementsByTagName("body")[0]
let section = document.getElementsByTagName("section")[0]
let button = document.querySelector('input[type="submit"]')

heading.style.color = colors[rand]
sub.style.color = colors[rand]
body.style.backgroundColor = mids[rand]
section.style.backgroundColor = darks[rand]
button.style.backgroundColor = mids[rand]

//setting ls colors

//stolen idk how it work
function hexToRgb(hex) {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
  }

function updateLight(){    
    
    let leftLight = hexToRgb(box1.value)
    let rightLight = hexToRgb(box2.value)
    
    console.log(leftLight)

    let diffs = [(rightLight.r - leftLight.r)/4, (rightLight.g - leftLight.g)/4, (rightLight.b - leftLight.b)/4]
    for (let i = 0; i<5; i++){
    //     strip.children[i].material.color = new THREE.Color(leftLight.r/255,leftLight.g/255,leftLight.b/255)
        lights[i].style.fill = 'rgb('+leftLight.r+','+leftLight.g+','+leftLight.b+')'
        
        leftLight.r += diffs[0]
        leftLight.g += diffs[1]
        leftLight.b += diffs[2]
    
    }
}

let box1 = document.getElementById("color1")
let box2 = document.getElementById("color2")

let lights = []
for(let i = 0; i<5; i++){
    lights.push(document.querySelector('#L'+(i+1)))
}
console.log(lights)

box1.addEventListener('input',up=>{
    updateLight()
})

box2.addEventListener('input',up=>{
    updateLight()
})