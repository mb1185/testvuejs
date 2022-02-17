<template>
  <div>
    <div class="position-relative">
      <div class="position-absolute top-50 end-0" id="info">
          <ul class="list-group">
              <li class="list-group-item"> Description {{fichierGltf}} </li>
              <li class="list-group-item">  {{fps}} </li>
              <li class="list-group-item"> 
                 <button class="btn btn-primary" width="100px"  v-on:click="zoom()">Zoom</button>
              </li>
              <li class="list-group-item"> 
                 <button class="btn btn-primary" width="100px"  v-on:click="fcSousEnsemble()">SousEnsemble</button>
              </li>
          </ul>
      </div>
    </div>
    <canvas class="virtual" ref="bjsCanvas"  />
    <babylon-object-control  v-for="(value, name) in listComposant" :key="name" :refcomposant="value" :isSelected="value.isSelected" />
  </div>
</template>

<script>

//import { Engine, Scene, ArcRotateCamera, Vector3, MeshBuilder, StandardMaterial, Color3, HemisphericLight, SceneLoader } from "@babylonjs/core";
import * as BABYLON from "@babylonjs/core";
import  "@babylonjs/inspector";
//import * as GUI from "babylonjs-gui";
import BabylonObjectControl from "./BabylonObjectControl.vue"

import * as axios from "axios"
//import {BABYLON} from "babylonjs-loaders"
//import { BABYLON } from "@babylonjs/loaders"

export default {
  name: "BabylonTest",

  data(){
      return{
          updateObject: {},
          listComposant:{},
          selectedName: '', 
          selectedObject: undefined, 
          largeurCube: 10,
          fps: 10,
      }
  },
  components:{
      BabylonObjectControl
    
      
  },
  props: {
      fichierGltf:{
          type: String,
          default: function(){
              return 'ff'
          },
      },
      repr: {
        type: String,
        default : 'svg'
      },
  },
  mounted() {
    this.bjsCanvas = this.$refs.bjsCanvas;
    if (this.bjsCanvas) {
      this.createScene(this.bjsCanvas);
      this.loadGltf()
    }
  },
  methods:{
      createScene: function(canvas){
        this.engine = new BABYLON.Engine(canvas);
        this.scene = new BABYLON.Scene(this.engine);

        //Physic
        var gravityVector = new BABYLON.Vector3(0,-9.81, 0);

        //var physicsPlugin = new BABYLON.CannonJSPlugin();
        var physicsPlugin = new BABYLON.AmmoJSPlugin();
        this.scene.enablePhysics(gravityVector, physicsPlugin);


        //scene.clearColor = BABYLON.Color3.Blue();
        this.scene.ambientColor = new BABYLON.Color3.Blue();
        //this.scene.useRightHandedSystem = true;

        /*
        BABYLON.SceneOptimizer.OptimizeAsync(this.scene, BABYLON.SceneOptimizerOptions.ModerateDegradationAllowed(),
          function() {
            console.log("Optimisation ok")
          }, function() {
            // FPS target not reached
            console.log("Optimisation Nok")
          });
          */

        //Skybox
        /* 
        var skybox = BABYLON.Mesh.CreateBox("skyBox", 100.0, this.scene);
        var skyboxMaterial = new BABYLON.StandardMaterial("skyBox", this.scene);
        skyboxMaterial.backFaceCulling = false;
        skyboxMaterial.disableLighting = true;
        skybox.material = skyboxMaterial;
        skybox.infiniteDistance = true;
        skyboxMaterial.reflectionTexture = new BABYLON.CubeTexture("skybox", this.scene);
        skyboxMaterial.reflectionTexture.coordinatesMode = BABYLON.Texture.SKYBOX_MODE;
      */

        //const camera = new FreeCamera("camera1", new Vector3(0, 5, -10), scene);
        this.camera = new  BABYLON.ArcRotateCamera("Camera", 3.14/2, 3.14/3, 20, new BABYLON.Vector3(0, 0, 0), this.scene);
        this.camera.setTarget(BABYLON.Vector3.Zero());
        this.camera.attachControl(canvas, true);
        this.camera.angularSensibility = 0.0
        this.camera.wheelPrecision = 10.0

        new BABYLON.HemisphericLight("light", BABYLON.Vector3.Up(), this.scene);
        new BABYLON.PointLight("Omni", new BABYLON.Vector3(0, 100, 100), this.scene);

          // Ground
        //Materials
        var groundMaterial = new BABYLON.StandardMaterial("ground", this.scene);
        groundMaterial.diffuseTexture = new BABYLON.Texture("textures/sol_terre.jpg", this.scene);
        groundMaterial.diffuseTexture.uScale = 20;
        groundMaterial.diffuseTexture.vScale = 20;
        //groundMaterial.specularColor = BABYLON.Color3.Black();
        //groundMaterial.emissiveColor = BABYLON.Color3.Black();
        groundMaterial.diffuseColor = BABYLON.Color3.Gray();
        this.ground = BABYLON.MeshBuilder.CreateGround("ground", {width:100, height:100}, this.scene, false);
        this.ground.position.y = -12.0
        //this.ground.position.z = -12.0
        this.ground.material = groundMaterial;

        this.ground.physicsImpostor = new BABYLON.PhysicsImpostor(this.ground, BABYLON.PhysicsImpostor.BoxImpostor, { mass: 0, restitution: 0.9 }, this.scene);

        //const box = BABYLON.MeshBuilder.CreateBox("box", { size: 2 }, this.scene);
        //const material = new BABYLON.StandardMaterial("box-material", this.scene);
        //material.diffuseColor = BABYLON.Color3.Blue();
        //box.material = material;
        
    
       this.scene.debugLayer.show({
        embedMode: true,
         });

        this.engine.runRenderLoop(() => {
            this.scene.render();
            this.fps = this.engine.getFps().toFixed()
        });

        /*
        SceneLoader.Append("./", "testthreejs.gltf", scene, function (scene) {
            console.log("TOTOT", scene)
            // do something with the scene
        });
        */



      this.scene.onPointerObservable.add((pointerInfo) => {

        switch (pointerInfo.type) {
          case BABYLON.PointerEventTypes.POINTERDOWN:
              if(pointerInfo.pickInfo.hit && pointerInfo.event.button == 0 && pointerInfo.pickInfo.pickedMesh != this.ground) {
                          this.pointerDown(pointerInfo.pickInfo.pickedMesh)
              }
              //Click droit
              if(pointerInfo.event.button == 2){
                this.pointerDown(null)
              }
            break;
          case BABYLON.PointerEventTypes.POINTERUP:
                        this.pointerUp();
            break;
          case BABYLON.PointerEventTypes.POINTERMOVE:          
                        //this.pointerMove();
            break;
          }
      });

      this.scene.onKeyboardObservable.add((kbInfo) => {
        switch (kbInfo.type) {
          case BABYLON.KeyboardEventTypes.KEYDOWN:
            console.log("KEY DOWN: ", kbInfo.event.key);
            break;
          case BABYLON.KeyboardEventTypes.KEYUP:
            console.log("KEY UP: ", kbInfo.event.key);
            if ( kbInfo.event.key == "z"){
              this.zoom()
            }
            break;
        }
      });

      // here we add XR support
      //const env = scene.createDefaultEnvironment();
      this.scene.createDefaultXRExperienceAsync({
        floorMeshes: [this.ground],
      });

    },
    loadGltf: function(){

      BABYLON.SceneLoader.LoadAssetContainer("./", this.fichierGltf, this.scene, function (container) {
          console.log("Container: ", container)
          console.log("Container Node: ", container.getNodes())
          //var meshes = container.meshes;
          var root = container.getNodes()[0]
          //root.rotation = new BABYLON.Vector3(0.0, 0.0 * Math.PI / 180,0.0);
          //root.scaling.z = 1

          for (var ob of root.getChildren()){
            //console.log("Root ob:", ob.name)
            if (ob.name.substring(0,1) != "#"){
              ob.dispose()
            }else{
              //this.listComposant[ob.name] =  { 'el': ob, 'isSelected': false}
            }
          }
          // Adds all elements to the scene
          container.addAllToScene();
          this.loadJson()
          this.testPhysic()
      }.bind (this));
    },
    loadJson: function(){
      console.log("Load Json file", this.fichierGltf)
      //Conv nomfichier.gltf vers nomfichier.json
      var split_nom_fichier = this.fichierGltf.split(".")
      var nom_fichier_json = split_nom_fichier[0] + ".json"
      console.log("Load Json file", nom_fichier_json)
      axios.get(nom_fichier_json).then(result => {
        console.log("Json result :", result)
        for (const [key, value] of Object.entries(result.data)) {
                console.log("Json object: ", key, value);
                console.log("Json object ", this.scene.getNodeByName(key))

                var compo = this.scene.getNodeByName(key)
                if (compo != null){
                  this.listComposant[key] = { 'el': compo, 'isSelected': false, "typeObject": value["typeObject"]}
                }
                
                
            }        
      })


    },
    pointerDown: function(meshSelected){
      if (this.selectedObject != null){
        this.listComposant[this.selectedObject.name]['isSelected'] = false 

      }
      if (meshSelected != null){
        if (meshSelected.name in this.listComposant){
          this.selectedObject = meshSelected
          this.listComposant[this.selectedObject.name]['isSelected'] = true 
        }

      }

    },
    pointerUp: function(){

    },
    pointerMove: function(){

    },
    zoom: function(){
      if (this.selectedObject != null){
        console.log("Zoom", this.selectedObject.position)
        console.log("Postion x", this.selectedObject.position.x)
        //this.camera.focusOn([this.selectedObject], false)
        this.camera.setPosition(new BABYLON.Vector3( -this.selectedObject.position.x, this.selectedObject.position.y, 10.0))

        this.camera.setTarget(new BABYLON.Vector3( -this.selectedObject.position.x,this.selectedObject.position.y, this.selectedObject.position.z));


      }
    },
    fcSousEnsemble: function(){
        console.log("FcSousEnsemble")
        const refSousEnsemble = this.scene.getMeshByName(this.selectedObject.name).metadata.gltf.extras.refSousEnsemble
        console.log("UserData sous ensemble: ", refSousEnsemble)
        //Modification chemin fichier gltf de la prop App.vue
        this.$root.fichierGltf = refSousEnsemble

    },
    testPhysic: function(){
        var sphere = BABYLON.Mesh.CreateSphere("sphere1", 16, 2, this.scene);
        sphere.position.y = 2;
        sphere.physicsImpostor = new BABYLON.PhysicsImpostor(sphere, BABYLON.PhysicsImpostor.SphereImpostor, { mass: 1, restitution: 0.9 }, this.scene);
    }
  },
  watch:{
    fichierGltf: {
        immediate: false,
        handler(val, oldval){
            console.log("Fichier Gltf TT :", val, oldval)
            for (const [key, value] of Object.entries(this.listComposant)) {
                console.log("Suppression object: ", key, value);
                delete this.listComposant[key]
            }
            this.scene.dispose()
            this.engine.dispose()
            this.createScene(this.bjsCanvas
            )
            this.loadGltf()
        }
    },
  },

};
</script>

<style lang="scss" scoped="">
#info {
	//position: absolute;
	//top: 400px;
	//width: 100%;
	text-align: left;
	//z-index: 100;
	//display:block;
}
.fill { 
    min-height: 100%;
    height: 100%;
}
.virtual{
    height: 100%;
    width: 100%;
    min-height: 300px;
    min-width: 600px;  
}
</style>