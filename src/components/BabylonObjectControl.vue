<template>

    <div v-if="false" id="containermm" >
        Contenu 3d
    </div>

          
</template>



<script>

import * as BABYLON from "@babylonjs/core";
import  "@babylonjs/inspector";
import * as GUI from "babylonjs-gui";

 export default {
  name: 'BabylonObjectControl',
  data(){
      return{
          largeurCube: 10,
          compo: this.refcomposant.el,

          updateObject: {},
          anims: {},
          
      }
  },
  components:{
    
      
  },
  props: {
      refcomposant: Object,
      isSelected: Boolean,
      x:String,
      y:String,
      repr: {
        type: String,
        default : 'svg'
      },
  },
  created(){
    //console.log("Compo:", this.compo)
    this.refObjects = {}
    this.refObjects[this.compo] = this.compo
    //this.compo.layers.set(1)
          //Compo change materiaux pour etre unique
    var mat = new BABYLON.StandardMaterial("Mat" +  this.compo.name);

    this.myDynamicTexture = new BABYLON.DynamicTexture("dynamic texture", {width:512, height:256}, this.$parent.scene);  
    //Add text to dynamic texture
    this.myDynamicTexture.drawText("Grass", 75, 135, "bold 44px monospace", "green", "white", false, true);
    this.myDynamicTexture.drawText("Yes", 75, 135, "bold 44px monospace", "green", "white", false, true);
    mat.diffuseTexture = this.myDynamicTexture;

    mat.diffuseColor = BABYLON.Color3.Yellow()
    this.compo.material = mat

    //Tesst si children dans compo
    for (const child of this.compo.getChildren()){
      console.log("Child:", child)
      this.refObjects[child.name] = child
      //child.name = this.compo.name
      child.material = this.compo.material
      //child.layerMask = 0x10000000;
    }

    console.log("Created fin - refObject",this.refObjects)


  },
  mounted(){
    //Abonnement au variables
    for (const [key, value] of Object.entries(this.compo.metadata.gltf.extras)) {
        console.log("User data object key: ", key);
        console.log("User data object value: ",  value);
        if (key.substring(0,4) == 'anim'){
          console.log("Animation : ", value);
          var convJson = '{}'
          convJson = value.replaceAll("'", "\"")
          this.anims[key] = JSON.parse(convJson)
          //console.log("Animation :", this.anims)
          this.updateObject[this.anims[key].var.id] = {}
          this.$root.abonnementComposant( this.anims[key].var.id, this.$.uid, this)
          console.log("Update ob:",this.updateObject)
        }
    }

    if (this.refcomposant.typeObject == "temperature"){
      this.createGuiTemperature()
    }



    //this.createGUi()
    



  },
  beforeUnmount(){
    console.log("Unmount")
    
    this.compo.dispose()

  },
  unmounted(){
    // abonnemeent de lobject
    //Abonnement au variables
    for (const [key, value] of Object.entries(this.anims)) {
        console.log("User data object: ", key, value);
  
        this.updateObject[value.var.id] = {}
        this.$root.desabonnementComposant( value.var.id, this.$.uid)
        
    }

  },

  methods:{
    createGuiTemperature: function(){
      var manager = new GUI.GUI3DManager(this.$parent.scene);
      var button = new GUI.Button3D("reset");
      

      this.temperature = new GUI.TextBlock();
      this.temperature.text = "reset";
      this.temperature.color = "white";
      this.temperature.fontSize = 24;
      this.temperature.scaleY = 2
      button.content = this.temperature;     
      manager.addControl(button)
      button.linkToTransformNode(this.compo);
      button.position.z = 1.5;
      button.position.y = 1.5;
      button.scaling = new BABYLON.Vector3(2,1,1)
      button.mesh.material.backFaceCulling = false 
      //button.mesh.rotation = new BABYLON.Vector3(0.0, 180.0 * Math.PI / 180, 0.0);
      button.mesh.scaling.z = -1.0

    },
    createGUi: function(){
      // GUI
        this.Gui = BABYLON.Mesh.CreatePlane("plane", 2);
        this.Gui.parent = this.compo;
        this.Gui.position.y = 2;

        var advancedTexture = GUI.AdvancedDynamicTexture.CreateForMesh(this.Gui);

        var grid = new GUI.Grid();
        grid.addColumnDefinition(1.0);
        //grid.addColumnDefinition(0.5);
        //grid.addRowDefinition(200, true);
        //grid.addRowDefinition(200, true);
        //grid.addRowDefinition(200, true);
        grid.addRowDefinition(0.33);
        grid.addRowDefinition(0.33);
        grid.addRowDefinition(0.33);
        //var panel = new GUI.StackPanel();
        //grid.addControl(panel,0,0)

        this.button1 = GUI.Button.CreateSimpleButton("but1", this.compo.name);
        this.button1.width = 1;
        this.button1.height = 1.0;
        this.button1.color = "white";
        this.button1.fontSize = 50;
        this.button1.background = "green";
        this.button1.onPointerUpObservable.add(function() {
            alert("you did it!");
        });

        var image = new GUI.Image("but", "start_button.png");
        //image.stretch = GUI.Image.STRETCH_FILL;
        //image.width = "128px";
        //image.height = "128px";

        var slider = new GUI.Slider();
        slider.minimum = 0;
        slider.maximum = 2 * Math.PI;
        slider.isThumbClamped = true;
        //slider.isVertical = isVertical;
        slider.displayThumb = true;

        //slider.height = "20px";
        //slider.width = "200px";

        slider.color = "red";
        slider.onValueChangedObservable.add(function(value) {
           console.log( "Y-rotation: " + (BABYLON.Tools.ToDegrees(value) | 0) + " deg")
        });

        //grid.addControl(this.button1,0,0)
        //grid.addControl(this.image,0,1)
        //advancedTexture.addControl(this.button1);
        //panel.addControl(this.button1)
        //panel.addControl(image)
        grid.addControl(image,0,0)
        grid.addControl(this.button1,1,0)
        grid.addControl(slider,2,0)
        advancedTexture.addControl(grid);
        //advancedTexture.addControl(image)

        //3D gui
      // Create the 3D UI manager
        this.Gui3d = new GUI.GUI3DManager(this.$parent.scene);

        var panel = new GUI.PlanePanel();
        panel.margin = 0.2;

        this.Gui3d .addControl(panel);
        panel.linkToTransformNode(this.compo);
        panel.position.z = -1.5;
        // Let's add some buttons!
        var button = new GUI.HolographicButton("orientation");
        panel.addControl(button);
        button.text = "Button #" + panel.children.length;
        panel.blockLayout = true;
        panel.blockLayout = false;
        

    },

  
  },
  computed:{
      
      pValue(){
        console.log("pValue:", this.updateObject)
        var result = []

        for (const anim of Object.values(this.anims)){
          //this.group.getObjectByName(anim.qui).position.x = 3.0
          result.push({'qui': anim.qui, 'quoi': anim.quoi, 'valeur': this.updateObject[anim.var['id']][anim.var['attribut']]})

        }
        return result

      }
  },
  watch:{
      pValue: function (newVal){
          //console.log("Watch !!!!!!!!!! updateObject:", newVal)
          //console.log("Watch !!!!!!!!!! updateObject:", this.refObjects)
          for (const anim of newVal){
            switch (anim.quoi) {
              case 'Couleur':
                console.log("Watch !!!!!!!!!! updateObject: Change color")
                if (anim.valeur == 'ON'){
                  console.log("Anim ref", this.refObjects[anim.qui])
                  this.refObjects[anim.qui].material.alpha =  0.5
                }else{
                  this.refObjects[anim.qui].material.alpha = 1.0
                }
                break;
              case 'Position':
                if (this.temperature){
                  //this.myDynamicTexture.update();
                  //this.temperature.text = anim.valeur
                  this.temperature.text = "TOTT"
                }
                //this.refObjects[anim.qui]['material']['transparent'] = true
                //this.refObjects[anim.qui]['material']['opacity'] = anim.valeur/100.0
                break;
              default:
                break;
            }
          }
          
      },
      isSelected:function(val){
          console.log("isSlected:", val)
          if (val){
            this.myDynamicTexture.drawText("Youp", 75, 135, "bold 44px monospace", "green", "white", false, true);
            this.compo.material.diffuseColor = BABYLON.Color3.Green();
            this.compo.material.albedoColor = BABYLON.Color3.Green();
            this.compo.material.alpha = 0.5;
            this.compo.showBoundingBox = true
            this.createGUi();
            
          }else{
            this.compo.material.diffuseColor = BABYLON.Color3.Gray();
            this.compo.material.albedoColor = BABYLON.Color3.Gray();
            this.compo.material.alpha = 1.0;
            this.compo.showBoundingBox = false
            //this.Gui.setEnabled (false)     
            this.Gui.dispose()   
            this.Gui3d.dispose()    
          }



      },

  }


}
</script>
<style lang="scss" scoped="">

</style>