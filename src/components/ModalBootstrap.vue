<template>
    <div>
        <div ref="refSlotTarget">
        <slot name="target" :donnees="donnees_popup"></slot>
        </div>
    </div>
</template>

<script>
  import { Modal } from 'bootstrap'

  export default {
    name: 'ModalBootstrap',
    data(){
      return{

      }
      
    },
    
    props:{
      valeur: String,
      donnees_popup : {},
    },
    mounted(){
        //var trigger =this.$refs.refSlotTrigger.childNodes[1]
        //var target = this.$refs.refSlotTarget.childNodes[1]
        this.ouvrirModal()
    },
    unmounted(){
      console.log("Unmount Modal")
    },
    
    methods: {
      ouvrirModal(){
        var target = this.$refs.refSlotTarget.childNodes[1]
        var theModal = new Modal(target, {})
        theModal.show() 
      },
      close() {
        this.$emit('close');
      },

    },
  };
</script>