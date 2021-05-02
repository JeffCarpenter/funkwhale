<template>
    <modal :show.sync="show">
      <h4 class="header">{{ labels.header }}</h4>
      <div class="content">
        
      </div>
      <div v-if="$store.state.auth.authenticated" class="actions">
        <router-link 
          :to="{path: '/logout'}" 
          class="ui danger fluid labeled icon button">
          <i class="sign out alternate icon"></i>
          {{ logout }}
        </router-link>
      </div>
      <div v-else class="actions">
        <router-link :to="{path: '/login', query: { next: this.$route.fullPath }}" class="ui positive labeled icon button"><i class="key icon"></i>
          {{ login }}
        </router-link>
        <router-link v-if="$store.state.instance.settings.users.registration_enabled.value" :to="{path: '/signup'}" class="ui primary labeled icon button"><i class="user icon"></i>
          {{ signup }}
        </router-link>
      </div>
    </modal>
</template>

<script>
import Modal from '@/components/semantic/Modal'

export default {
  props: {
    logout: {type: String},
    login: {type: String},
    signup: {type: String}
  },
  components: {
    Modal,
  },
  data() {
    return {
      show: false,
    }
  },
  computed: {
    labels() {
      return {
        header: this.$pgettext('Popup/Title/Noun', "Options"),
      }
    },
  }
}

</script>
