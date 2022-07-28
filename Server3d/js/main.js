import { GLTFLoader } from './GLTFLoader.js';
import { PlaneBufferGeometry } from './three.module.js';

const scene = new THREE.Scene();

let camera = new THREE.PerspectiveCamera(
    75, 
    window.innerWidth/window.innerHeight, 
    0.1, 
    1000
);

let renderer = new THREE.WebGLRenderer({
    antialias: true,
    canvas: document.querySelector('#strip'),
});

renderer.setSize(window.innerWidth,window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio/1);

var loader = new GLTFLoader();

var strip;
loader.load("./glb/lightstrip.glb",function(gltf){
    strip = gltf.scene.children[0];

    strip.scale.set(.4,.4,.4);
    
    scene.add(strip);
});

var light = new THREE.PointLight(0xffffff, .7);
scene.add(light);
light.position.set(-5,1,-5);

var light2 = new THREE.PointLight(0xffffff, .7);
scene.add(light2);
light2.position.set(5,1,-5);

var light3 = new THREE.PointLight(0xffffff, .05);
scene.add(light3);
light3.position.set(1,1,7);

var fill = new THREE.AmbientLight(0xffffff,.9);
scene.add(fill);

const planeGeo = new PlaneBufferGeometry(50,50)
const material = new THREE.MeshStandardMaterial({color: 0xbbbbbb});
let plane = new THREE.Mesh(planeGeo, material);
scene.add(plane)
plane.position.z = -10

//set camera position
camera.position.z= 5;
camera.position.y= -1;
scene.background = new THREE.Color( .7,.7,.7 );
console.log("camera posion", camera.position)

let frame = 0;
function animate(){
    requestAnimationFrame(animate);
    strip.rotation.y = .1*Math.sin(frame);
    strip.position.y = .05*Math.sin(frame*3);
    if (frame > 2*Math.PI){
        frame = 0;
    } 
    //console.log(frame)
    frame += .01;
    renderer.render(scene, camera);    
}
window.addEventListener('resize', onResize=>{
    camera.aspect = window.innerWidth/window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth,window.innerHeight);
});

//stolen idk how it work
function hexToRgb(hex) {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
  }

let box1 = document.getElementById("box1")
let box2 = document.getElementById("box2")

function updateLight(){    
    
    let leftLight = hexToRgb(box1.value)
    let rightLight = hexToRgb(box2.value)
    
    light.color = new THREE.Color(leftLight.r/255,leftLight.g/255,leftLight.b/255)
    light2.color = new THREE.Color(rightLight.r/255,rightLight.g/255,rightLight.b/255)

    let diffs = [(rightLight.r - leftLight.r)/4, (rightLight.g - leftLight.g)/4, (rightLight.b - leftLight.b)/4]
    for (let i = 3; i<8; i++){
        strip.children[i].material.color = new THREE.Color(leftLight.r/255,leftLight.g/255,leftLight.b/255)
        
        leftLight.r += diffs[0]
        leftLight.g += diffs[1]
        leftLight.b += diffs[2]
    
    }
}

box1.addEventListener('input',up=>{
    updateLight()
})

box2.addEventListener('input',up=>{
    updateLight()
})

// let link = document.querySelector("#strip")
// link.addEventListener('click',red=>{
//     for (let i = 3; i<8; i++){
//         strip.children[i].material.color = new THREE.Color( 1,0,0 )
//     }
// })
animate();