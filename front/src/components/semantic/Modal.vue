<template>
  <div :class="additionalClasses.concat(['ui', {'active': show}, {'scrolling': scrolling} ,{'overlay fullscreen': fullscreen && ['phone', 'tablet'].indexOf($store.getters['ui/windowSize']) > -1},'modal'])">
    <i tabindex=0 class="close inside icon"></i>
    <slot v-if="show">

    </slot>
  </div>
</template>

<script>
import $ from 'jquery'
import createFocusTrap from 'focus-trap'

export default {
  props: {
    show: {type: Boolean, required: true},
    fullscreen: {type: Boolean, default: true},
    scrolling: {type: Boolean, required: false, default: false},
    additionalClasses: {type: Array, required: false, default: () => []}
  },
  data () {
    return {
      control: null,
      focusTrap: null,
    }
  },
  mounted () {
    this.focusTrap = createFocusTrap(this.$el)
  },
  beforeDestroy () {
    if (this.control) {
      $(this.$el).modal('hide')
    }
    this.focusTrap.deactivate()
    $(this.$el).remove()
  },
  methods: {
    initModal () {
      this.control = $(this.$el).modal({
        duration: 100,
        onApprove: function () {
          this.$emit('approved')
        }.bind(this),
        onDeny: function () {
          this.$emit('deny')
        }.bind(this),
        onHidden: function () {
          this.$emit('update:show', false)
        }.bind(this),
        onVisible: function () {
          this.focusTrap.activate()
          this.focusTrap.unpause()
        }.bind(this)
      })
    }
  },
  watch: {
    show: {
      handler (newValue) {
        if (newValue) {
          this.initModal()
          this.$emit('show')
          this.control.modal('show')
          this.focusTrap.activate()
          this.focusTrap.unpause()
          document.body.classList.add('scrolling')
        } else {
          if (this.control) {
            this.$emit('hide')
            this.control.modal('hide')
            this.control.remove()
            this.focusTrap.deactivate()
            this.focusTrap.pause()
            document.body.classList.remove('scrolling')
          }
        }
      }
    }
  }

}
</script>
