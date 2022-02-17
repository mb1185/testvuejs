<template>

    <input type="range" v-model="largeurCube"  />
    <button class="btn btn-primary" width="100px"  v-on:click="fcSousEnsemble()">Voir Sous Ensembre</button>

    <div class="position-relative">
    <div class="position-absolute top-50 end-0" id="info">
        <ul class="list-group">
            <li class="list-group-item"> Description {{fichierGltf}} </li>
            <li class="list-group-item"> Selection : {{selectedName}} </li>
            <li class="list-group-item"> HMMl </li>
        </ul>
        <canvas ref="canvasTexture" width="100" height="100" />
    </div>
    </div>
    <div   class="virtual" id="container" > <!-- style="min-height: 300px;min-width: 600px;" -->
    </div>
    <div class="container fill"> {{ fichierGltf}} </div>

    <VrCube  v-for="(value, name) in listComposant" :key="name" :refcomposant="value" :isSelected="value.selected" :selectedName="selectedName" :scene="this.scene" />

          
</template>



<script>

import * as Three from 'three'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'
import { VRButton } from 'three/examples/jsm/webxr/VRButton.js';

import { XRControllerModelFactory } from 'three/examples/jsm/webxr/XRControllerModelFactory.js';
import { XRHandModelFactory } from 'three/examples/jsm/webxr/XRHandModelFactory.js';

import  VrCube  from './VrCube.vue'

//Three mesh ui
import ThreeMeshUI from 'three-mesh-ui'

const handModels = {
    left: null,
    right: null
};



const intersected = [];
const tempMatrix = new Three.Matrix4();
const pointer = new Three.Vector2();
const taille = new Three.Vector2();
const positionContainer = new Three.Vector2();

 export default {
  name: 'ThreeTest',
  data(){
      return{
          updateObject: {},
          listComposant:{},
          selectedName: '', 
          selectedObject:{}, 
          largeurCube: 10,

  
      }
  },
  components:{
      VrCube
    
      
  },
  props: {
      proprietes: {
          type: Object,
          default: function() {
              return {'Couleur': {'id':'id128', 'attribut': 'T'}, 'Nom':'Toto'}
          }
      },
      fichierGltf:{
          type: String,
          default: function(){
              return 'ff'
          },
      },
      x:String,
      y:String,
      repr: {
        type: String,
        default : 'svg'
      },
  },
  created(){
      
      this.init()
  },

  mounted(){
      console.log ("3D mounted")
      
      this.initscene()

  },
  unmounted(){
      



      
  },
  beforeUnmount(){
      
      this.renderer.domElement.remove()
        this.scene.children.forEach(child => {
            child.traverse(function(obj) {
            if (obj.type === 'Mesh') {
            obj.geometry.dispose();
            obj.material.dispose();
            //obj.texture.dispose();
            }
            })
        });     
      this.listComposant = undefined
       this.scene.clear()
      //console.log("Renderer info", this.renderer.info)
      this.renderer.dispose()
      this.renderer = undefined
      this.scene.clear()
      this.scene.dispose()

      this.group = undefined
      this.scene = undefined
      this.controller1 = undefined
      this.controller2 = undefined
      this.mixer = undefined

    this.loader = undefined
    this.chargementGlb = undefined
    
      //console.log("3D unmounted", this)
      

  },

  computed:{

  },
  watch:{


    fichierGltf: {
        immediate: true,
        handler(val, oldval){
            console.log("Fichier Gltf TT :", val, oldval)
            for (const [key, value] of Object.entries(this.listComposant)) {
                console.log("Suppression object: ", key, value);
                delete this.listComposant[key]
            }
            //Three.Cache.enabled = true
            if (!this.loader){
                this.loader = new GLTFLoader();
            }else{
                console.log("Loader existe deja")
            }
            
            this.loader.load(val, this.chargementGlb)
        }
    },
  },
  methods:{
    init: function(){

        this.mixer = new Three.AnimationMixer(  );
        
        
    },
    initscene: function(){
        let container = document.getElementById('container');

        taille.x = window.innerWidth //container.clientWidth
        taille.y = window.innerHeight//container.clientHeight

        //Camera
        this.camera = new Three.PerspectiveCamera(75, taille.x/taille.y, 0.1, 1000);
        this.camera.position.x = 0;
        this.camera.position.y = 2;
        this.camera.position.z = 10;
        this.camera.layers.enable( 0 ); // enabled by default
		this.camera.layers.enable( 1 );

        //Scene
        this.scene = new Three.Scene();
        this.scene.background = new Three.Color( 0xcccccc )


        this.group = new Three.Group();
        this.scene.add( this.group );

        //Lumiere--------------
        const dirLight1 = new Three.DirectionalLight( 0xffffff );
        dirLight1.position.set( 1, 1, 1 );
        this.scene.add( dirLight1 );

        const dirLight2 = new Three.DirectionalLight( 0x002288 );
        dirLight2.position.set( - 1, - 1, - 1 );
        this.scene.add( dirLight2 );
        const light = new Three.AmbientLight( 0x222222  );
        this.scene.add(light);

        //const helperLight = new Three.DirectionalLightHelper( dirLight2, 5 );
        //this.scene.add( helperLight );

        // Grid helper
        const helper = new Three.GridHelper( 20, 20, 0x303030, 0x303030 );
        helper.position.y = -2.0;
        this.scene.add( helper );

        //axe helper
        const axesHelper = new Three.AxesHelper( 5 );
        axesHelper.layers.set(0);
        this.scene.add( axesHelper );

        //room
        /*
        let room = new Three.LineSegments(
                new BoxLineGeometry( 20, 20, 20, 10, 10, 10 ).translate( 0, 1, 0 ),
                new Three.LineBasicMaterial( { color: 0x808080 } )
            );
        this.scene.add( room );*/
        
        //this.mesh.scale.x = 10;
        //Renderer
        this.renderer = new Three.WebGLRenderer({antialias: true});
        this.renderer.xr.enabled = true;
        this.renderer.setSize(taille.x, taille.y);
        this.renderer.setPixelRatio( window.devicePixelRatio );
        container.appendChild(this.renderer.domElement);



        //VR BUTTON ----------------------------------
        container.appendChild( VRButton.createButton( this.renderer ) );
        //document.body.appendChild( VRButton.createButton( this.renderer ) );

        //--------Controleurs Manettes------------------//
				// controllers

        this.controller1 = this.renderer.xr.getController( 0 );
        this.controller1.addEventListener( 'selectstart', this.onSelectStart );
        this.controller1.addEventListener( 'selectend', this.onSelectEnd );
        this.scene.add( this.controller1 );

        this.controller2 = this.renderer.xr.getController( 1 );
        this.controller2.addEventListener( 'selectstart', this.onSelectStart );
        this.controller2.addEventListener( 'selectend', this.onSelectEnd );
        this.scene.add( this.controller2 );

        const controllerModelFactory = new XRControllerModelFactory();
        const handModelFactory = new XRHandModelFactory();

		// Hand 1
        let controllerGrip1 = this.renderer.xr.getControllerGrip( 0 );
        controllerGrip1.add( controllerModelFactory.createControllerModel( controllerGrip1 ) );
        this.scene.add( controllerGrip1 );

        let hand1 = this.renderer.xr.getHand( 0 );
        hand1.userData.currentHandModel = 0;
        this.scene.add( hand1 );

        handModels.left = [
            handModelFactory.createHandModel( hand1, "boxes" ),
            handModelFactory.createHandModel( hand1, "spheres" ),
            handModelFactory.createHandModel( hand1, "mesh" )
        ];

        for ( let i = 0; i < 3; i ++ ) {

            const model = handModels.left[ i ];
            model.visible = i == 0;
            hand1.add( model );

        }

        hand1.addEventListener( 'pinchend', function() {

            handModels.left[ this.userData.currentHandModel ].visible = false;
            this.userData.currentHandModel = ( this.userData.currentHandModel + 1 ) % 3;
            handModels.left[ this.userData.currentHandModel ].visible = true;

        } );

        // Hand 2

        let controllerGrip2 = this.renderer.xr.getControllerGrip( 1 );
        controllerGrip2.add( controllerModelFactory.createControllerModel( controllerGrip2 ) );
        this.scene.add( controllerGrip2 );

        let hand2 = this.renderer.xr.getHand( 1 );
        hand2.userData.currentHandModel = 0;
        this.scene.add( hand2 );

        handModels.right = [
            handModelFactory.createHandModel( hand2, "boxes" ),
            handModelFactory.createHandModel( hand2, "spheres" ),
            handModelFactory.createHandModel( hand2, "mesh" )
        ];

        for ( let i = 0; i < 3; i ++ ) {

            const model = handModels.right[ i ];
            model.visible = i == 0;
            hand2.add( model );

        }

        hand2.addEventListener( 'pinchend', function () {

            handModels.right[ this.userData.currentHandModel ].visible = false;
            this.userData.currentHandModel = ( this.userData.currentHandModel + 1 ) % 3;
            handModels.right[ this.userData.currentHandModel ].visible = true;

        } );


        const geometry = new Three.BufferGeometry().setFromPoints( [ new Three.Vector3( 0, 0, 0 ), new Three.Vector3( 0, 0, - 1 ) ] );

        const line = new Three.Line( geometry );
        line.name = 'line';
        line.scale.z = 5;

        this.controller1.add( line.clone() );
        this.controller2.add( line.clone() );


        //-------End Controleurs Manetttes--------------
        
        //Raycaster declaration
        this.raycaster = new Three.Raycaster();
        this.raycaster.layers.set(1)

        //Mouse event
        console.log("Position container",container.getBoundingClientRect());
        positionContainer.x = container.getBoundingClientRect().left
        positionContainer.y = container.getBoundingClientRect().top
        //container.addEventListener( 'mousemove', this.onPointerMove );
        container.addEventListener('mousedown', this.onMouseClick);
        window.addEventListener( 'resize', this.onWindowResize );

        //keyborad event
        document.addEventListener( 'keydown', this.clavierPress );
        
        //Orbit control
        this.controls = new OrbitControls( this.camera, this.renderer.domElement );
        //this.controls = new OrbitControls( this.camera, this.labelRenderer.domElement );
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;
        this.controls.update()

        //Animation
        this.animate()
    },
    animate: function() {
        //fonction animation pour webXr
        this.renderer.setAnimationLoop(this.render)
    },
    render: function(){

        this.cleanIntersected();

        this.intersectObjects( this.controller1 );
        this.intersectObjects( this.controller2 );

        this.renderer.render(this.scene,this.camera);
        //this.labelRenderer.render(this.scene,this.camera);
        //this.mesh.rotation.x += 0.01;
        //this.mesh.rotation.y += 0.02;
        this.controls.update();
        //Update Mesh UI
        ThreeMeshUI.update();
        //Animation
        if (this.mixer) this.mixer.update(0.01);
    },
    chargementGlb: function (gltf){
        console.log("Fichier 3d charge!!")


        //console.log("Object:", this.cube)
        var listObject = []
        
        gltf.scene.traverse( function ( child ) {
            //console.log("Fichier 3d charge Object3d: !!", child)
            if (child.name.substring(0,1)== "#"){
                listObject.push(child)
                //console.log("Fichier Mesh Object3d: !!", child)
            }
            }.bind(this));

        
        for (const element of listObject) {
            //console.log(element)

            //element.layers.set(1)
            var convJson = '{}'
            if ('proprietes' in element.userData){
                convJson = (element.userData.proprietes.replaceAll("'", "\""))
            }
            
            //console.log("LogJson:", convJson)
            this.listComposant[element.name] = { 'el': element, 'sp': JSON.parse(convJson), 'selected': false}
            //this.scene.add(element);
        }

        console.log("Chargement gltf terminé")

        // Animations
        //this.mixer = new Three.AnimationMixer(this.listComposant['#LumiereSalin']['el'] );
        //this.mixer = new Three.AnimationMixer(this.listComposant['#moteur']['el'] );
        this.mixer = new Three.AnimationMixer(this.scene );
        //this.scene.add(gltf.scene)
        //console.log("Mixer", this.mixer)
        this.clips = gltf.animations;
        //console.log("Clip", this.clips)
        
        //Test texture canvas
        console.log("Test Canvas", this)
        this.drawingCanvas = this.$refs.canvasTexture
        this.drawingContext = this.drawingCanvas.getContext( '2d' );      
        this.drawingContext.fillStyle = '#FFFFFF';
        this.drawingContext.fillRect( 0, 0, 256, 256 );
        //cercle
        let circle = new Path2D();  // <<< Declaration
        circle.arc(50, 50, 25, 0, 2 * Math.PI, false);

        this.drawingContext.fillStyle = 'blue';
        this.drawingContext.fill(circle); //   <<< pass circle to context

        this.drawingContext.lineWidth = 10;
        this.drawingContext.strokeStyle = '#000066';
        this.drawingContext.stroke(circle);  // <<< pass circle here too

        this.drawingContext.font = '48px serif';
        this.drawingContext.fillText('Hello world', 10, 50);
        

        this.materialTexture = new Three.MeshBasicMaterial();
        this.materialTexture.map = new Three.CanvasTexture( this.drawingCanvas );
        var mesh = new Three.Mesh( new Three.BoxGeometry( 4, 2, 2 ), this.materialTexture );
        mesh.position.x = -2.0
        mesh.position.x = -5.0
		this.scene.add( mesh );


    },


    onSelectStart: function ( event ) {

        const controller = event.target;

        const intersections = this.getIntersections( controller );

        if ( intersections.length > 0 ) {

            const intersection = intersections[ 0 ];

            const object = intersection.object;
            object.material.emissive.b = 1;
            controller.attach( object );

            controller.userData.selected = object;

        }

    },

    onSelectEnd: function ( event ) {

        const controller = event.target;

        if ( controller.userData.selected !== undefined ) {

            const object = controller.userData.selected;
            object.material.emissive.b = 0;
            this.group.attach( object );

            controller.userData.selected = undefined;

        }
    },
    getIntersections :function ( controller ) {

        tempMatrix.identity().extractRotation( controller.matrixWorld );

        this.raycaster.ray.origin.setFromMatrixPosition( controller.matrixWorld );
        this.raycaster.ray.direction.set( 0, 0, - 1 ).applyMatrix4( tempMatrix );

        return this.raycaster.intersectObjects( this.group.children, true );

    },

    intersectObjects : function ( controller ) {

        // Do not highlight when already selected
        
        if ( controller.userData.selected !== undefined ) return;

        

        const line = controller.getObjectByName( 'line' );
        const intersections = this.getIntersections( controller );

        if ( intersections.length > 0 ) {
            
            
            const intersection = intersections[ 0 ];

            const object = intersection.object;
            
            if (object.material.type == "MeshStandardMaterial"){
                console.log("object inters", object)
                object.material.emissive.r = 1;
                intersected.push( object );
            }


            line.scale.z = intersection.distance;

        } else {

            line.scale.z = 5;

        }

    },

    cleanIntersected: function () {

        while ( intersected.length ) {
            
            const object = intersected.pop();
            if (object.material.type == "MeshStandardMaterial"){
                object.material.emissive.r = 0;
            }

        }

    },
    onPointerMove: function(event){
        console.log ("onPointerMove:", event)




    },
    onMouseClick: function( event ){

        if ( this.selectedObject ) {

            //this.selectedObject.material.color.set( '#69f' );
            
            this.selectedObject = null;

        }

        pointer.x = ( (event.clientX-positionContainer.x) / taille.x ) * 2 - 1;
        pointer.y = - ( (event.clientY-positionContainer.y) / taille.y ) * 2 + 1;
        //console.log("Pointer:", pointer)
        //console.log("Pointer: x"+ event.clientX + " y: " +event.clientY)

        this.raycaster.setFromCamera( pointer, this.camera );

        const intersects = this.raycaster.intersectObject( this.scene, true );
        //const intersects = this.raycaster.intersectObject( this.helper, true );

        if ( intersects.length > 0 ) {

            const res = intersects.filter( function ( res ) {

                return res && res.object;

            } )[ 0 ];

            if ( res && res.object ) {

                this.selectedObject = res.object;
                //this.selectedObject.material.color.set( '#f00' );

            }

        }
        console.log("Mouse Click!", event)
        console.log("Mouse Click object select!", this.selectedObject)
        
        if (this.selectedObject != null){
            // deselection object precedent
            if(this.selectedName in this.listComposant){
                this.listComposant[this.selectedName]['selected']= false
            }
            
            this.selectedName = this.selectedObject.name
            if (this.selectedName in this.listComposant){
                this.listComposant[this.selectedName]['selected']= true
                console.log("Selected Name", this.selectedName)
            }

        }else{
            if (this.selectedName != ''){
                if (this.selectedName in this.listComposant){
                    this.listComposant[this.selectedName]['selected']= false
                }
                this.selectedName = ''
            }

        }

    },
    clavierPress: function(keypress){
        console.log("Touche presse:", keypress )
        if (keypress.key == 'z'){
            //const offset = 5.0
            const boundingBox = new Three.Box3();
            boundingBox.setFromObject( this.selectedObject );
            const center = new Three.Vector3();
            boundingBox.getCenter(center);

            this.controls.target = center
  
            this.camera.position.z = this.selectedObject.position.z +4.0;
            this.camera.position.x = this.selectedObject.position.x;
            this.camera.position.y = this.selectedObject.position.y;

            //console.log("OrbitControl:",this.controls)
            //console.log("OrbitControl:",this.camera)
   


        }
    },
    onWindowResize: function() {

        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
        taille.x = window.innerWidth
        taille.y = window.innerHeight
        this.renderer.setSize( taille.x, taille.y  );
    },
    fcSousEnsemble: function(){
        console.log("FcSousEnsemble")
        const refSousEnsemble = this.scene.getObjectByName(this.selectedName).userData.refSousEnsemble
        console.log("UserData sous ensemble: ", refSousEnsemble)
        //Modification chemin fichier gltf de la prop App.vue
        this.$root.fichierGltf = refSousEnsemble

    },

  },


}
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