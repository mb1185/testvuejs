<template>

    <div v-if="false" id="containermm" >
        Contenu 3d
    </div>
          
</template>



<script>

import * as Three from 'three'
//Three mesh ui
import ThreeMeshUI from 'three-mesh-ui'

import {toRaw} from 'vue'

 export default {
  name: 'VrCube',
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
      scene: Object,
      selectedName: String,
      isSelected: Boolean,
      x:String,
      y:String,
      repr: {
        type: String,
        default : 'svg'
      },
  },
  created(){
    this.refObjects = {}
    this.refObjects[this.compo] = this.compo
    this.compo.layers.set(1)
          //Compo change materiaux pour etre unique
    var mat = new Three.MeshStandardMaterial()
    mat.color.set('red')
    this.compo.material = mat

    //Tesst si children dans compo
    for (const child of this.compo.children){
      //console.log("Child:", child)
      this.refObjects[child.userData.name] = child
      child.name = this.compo.name
      child.material = this.compo.material
      child.layers.set(1)
    }

    //console.log("Created fin - refObject",this.refObjects)


  },
  mounted(){
      //console.log("Ref Compo:", this.compo)
      //Ajout compo a la scene
      this.group = new Three.Object3D();
      this.group.add(toRaw(this.compo))
      //console.log("Group :", this.group)
      this.scene.add(this.group)


    //Abonnement au variables
    for (const [key, value] of Object.entries(this.compo.userData)) {
        //console.log("User data object: ", key, value);
        if (key.substring(0,4) == 'anim'){
          //console.log("Animation : ", value);
          var convJson = '{}'
          convJson = value.replaceAll("'", "\"")
          this.anims[key] = JSON.parse(convJson)
          //console.log("Animation :", this.anims)
          this.updateObject[this.anims[key].var.id] = {}
          this.$root.abonnementComposant( this.anims[key].var.id, this.$.uid, this)
          //console.log("Update ob:",this.updateObject)
        }
    }



    this.chargementMeshUi()
    this.chargementSprite()



  },
  beforeUnmount(){
    console.log("Unmount")
    
    
    this.group.removeFromParent()

    this.group = undefined

    this.sprite = undefined

    this.container = undefined

    this.textUi = undefined

    this.compo = undefined
    //this.group2.removeFromParent()
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
    chargementMeshUi: function(){
        this.container = new ThreeMeshUI.Block({
        width: 3.0,
        height: 1.5,
        padding: 0.1,
        backgroundOpacity: 0.8,
        fontFamily: 'Roboto-msdf.json',
        fontTexture: 'Roboto-msdf.png',
        });

        this.textUi = new ThreeMeshUI.Text({
            content: "Some text to be displayed",
            fontSize: 0.2,
        });

        this.container.add( this.textUi );
        this.container.position.set(this.compo.position.x, this.compo.position.y -2.0, this.compo.position.z)
        this.container.visible = false
        // scene is a THREE.Scene (see three.js)
        this.group.add( this.container );
        //console.log("UI container", container)
        ThreeMeshUI.update();

        // This is typically done in the render loop :
        

    },
    chargementSprite: function(){

      //console.log("Chargement Sprite")
      const map = new Three.TextureLoader().load( 'start_button.png' );
      const material = new Three.SpriteMaterial( { map: map } );

      this.sprite = new Three.Sprite( material );
      this.sprite.name = this.compo.name + "Start"
      //sprite.translate(this.compo.position.x,this.compo.position.y, this.compo.position.z -2.0)
      //console.log("Position",this.compo.position)
      //sprite.translateX(this.compo.position.x)
      //sprite.translateY(this.compo.position.y)
      //sprite.translateZ(this.compo.position.z)
      this.sprite.position.set(this.compo.position.x -0.5, this.compo.position.y -1.0, this.compo.position.z)
      this.sprite.layers.set(1)
      this.sprite.visible = false
      //this.group2 = new Three.Object3D();
      
      //this.group2.add( sprite );
      //Ajout group a la scene
      //this.compo.parent.parent.add(this.group2);
      this.group.add(this.sprite);

    
    },
  
  },
  computed:{
      
      pValue(){
        //console.log("pValue:", this.updateObject)
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
                //console.log("Watch !!!!!!!!!! updateObject: Change color")
                if (anim.valeur == 'ON'){
                  this.refObjects[anim.qui].material.emissive.b =  0.0
                }else{
                  this.refObjects[anim.qui].material.emissive.b = 1.0
                }
                break;
              case 'Position':
                this.refObjects[anim.qui]['material']['transparent'] = true
                this.refObjects[anim.qui]['material']['opacity'] = anim.valeur/100.0
                var strText = this.compo.name + ': ' +  anim.valeur.toString()
                //console.log(strText)
                this.textUi.set({content : strText})
                break;
              default:
                break;
            }
          }
          
      },
      isSelected:function(val){
          console.log("isSlected:", val)
          if (val){
            this.textUi.set({content : this.compo.name})
            this.container.visible = true
            this.compo.material.emissive.b = 0.8
            //this.compo.material.emissive.r = 0.8
          }else{
            this.textUi.set({content : ''})
            this.container.visible = false
            this.compo.material.emissive.b = 0.1
            //this.compo.material.emissive.r = 0.2
          }
          
          //ThreeMeshUI.update();

      },
      selectedName: function(val){
        //console.log("UpdateObject Select", this.updateObject)
        if (val == this.compo.name){
          console.log("Selected Name:", val)
          this.sprite.visible = true
          //this.$parent.clips.forEach( function ( clip ) {
          //  console.log("Play Animation")
          //  this.$parent.mixer.clipAction( clip,this.group ).play();
          //}.bind(this) );
        }else{
          this.sprite.visible = false
          //this.$parent.clips.forEach( function ( clip ) {
          //  console.log("Play Animation")
          //  this.$parent.mixer.clipAction( clip,this.group ).stop();
          //}.bind(this) );
        }
      },
  }


}
</script>
<style lang="scss" scoped="">

</style>