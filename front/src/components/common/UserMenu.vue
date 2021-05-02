<template>
  <div class="item">
    <div class="ui user-dropdown dropdown desktop-and-up">
      <img 
        class="ui avatar image"
        alt=""
        v-if="$store.state.auth.authenticated && $store.state.auth.profile.avatar && $store.state.auth.profile.avatar.urls.medium_square_crop"
        :src="$store.getters['instance/absoluteUrl']($store.state.auth.profile.avatar.urls.medium_square_crop)"/>
      <actor-avatar
        v-else-if="$store.state.auth.authenticated"
        :actor="{preferred_username: $store.state.auth.username, full_username: $store.state.auth.username,}"/>
      <i v-else class="cog icon" />
      <div class="ui menu">
        <div class="ui scrolling dropdown item">
          <i class="language icon" />
          {{ labels.language }}
          <i class="dropdown icon" />
          <div id="language-select" class="menu">
            <a :class="[{'active': $language.current === key},'item']" @click="$store.dispatch('ui/currentLanguage', key)" v-for="(language, key) in $language.available" :key="key" :value="key">{{ language }}</a>
          </div>
        </div>
        <div class="ui dropdown item">
          <i class="palette icon" />
          {{ labels.theme }}
          <i class="dropdown icon" />
          <div id="theme-select" class="menu">
            <a :class="[{'active': $store.state.ui.theme === theme.key}, 'item']" @click="$store.dispatch('ui/theme', theme.key)" v-for="theme in themes" :key="theme.key" :value="theme.key">
              <i :class="theme.icon" /> 
              {{ theme.name }}
            </a>
          </div>
        </div>
        <div v-if="$store.state.auth.authenticated" class="divider" />
        <router-link v-if="$store.state.auth.authenticated" class="item" :to="{name: 'profile.overview', params: { username: $store.state.auth.username },}">
          <i class="user icon" />
          {{ labels.profile }}
        </router-link>
        <router-link v-if="$store.state.auth.authenticated" class="item" :to="{ path: '/settings' }">
          <i class="cog icon" />
          {{ labels.settings }}
        </router-link>
        <div class="divider" />
          <div class="ui dropdown item">
            <i class="life ring outline icon" />
            {{ labels.support }}
            <i class="dropdown icon" />
            <div class="menu">
              <a href="https://governance.funkwhale.audio/g/kQgxNq15/funkwhale" class="item" target="_blank">
                <i class="users icon" />
                {{ labels.forum }}
              </a>
              <a href="https://riot.im/app/#/room/#funkwhale-troubleshooting:matrix.org" class="item" target="_blank">
                <i class="comment icon" />
                {{ labels.chat }}
              </a>
              <a href="https://dev.funkwhale.audio/funkwhale/funkwhale/issues" class="item" target="_blank">
                <i class="gitlab icon" />
                {{ labels.git }}
              </a>
            </div>
          </div>
          <a href="https://docs.funkwhale.audio" class="item" target="_blank">
            <i class="book open icon" />
            {{ labels.docs }}
          </a>
          <a href="" class="item" @click.prevent="showShortcuts">
            <i class="keyboard icon" />
            {{ labels.shortcuts }}
          </a>
          <router-link v-if="this.$route.path != '/about'" class="item" to="/about">
            <i class="question circle outline icon" />
            {{ labels.about }}
          </router-link>
        <div class="divider" />
        <router-link v-if="$store.state.auth.authenticated" class="item" style="color: var(--danger-color)!important;" :to="{ name: 'logout' }">
          <i class="sign out alternate icon" />
          {{ labels.logout }}
        </router-link>
        <router-link v-else class="item" :to="{ name: 'signup' }">
          <i class="user icon" />
          {{ labels.signup }}
        </router-link>
      </div>
    </div>
    <div @click="$refs.userModal.show = true" class="ui tablet-and-below">
      <img 
        class="ui avatar image"
        alt=""
        v-if="$store.state.auth.authenticated && $store.state.auth.profile.avatar && $store.state.auth.profile.avatar.urls.medium_square_crop"
        :src="$store.getters['instance/absoluteUrl']($store.state.auth.profile.avatar.urls.medium_square_crop)"/>
      <actor-avatar
        v-else-if="$store.state.auth.authenticated"
        :actor="{preferred_username: $store.state.auth.username, full_username: $store.state.auth.username,}"/>
      <i v-else class="cog icon" />
    </div>
    <user-modal
      ref="userModal"
      class="large"
      :login="labels.login"
      :signup="labels.signup"
      :logout="labels.logout"
      @created="$refs.userModal.show = false;">
    </user-modal>
  </div>
</template>

<script>

import UserModal from '@/components/common/UserModal'

export default {
  components: {
    UserModal
  },
  computed: {
    labels() {
      return {
        profile: this.$pgettext("*/*/*/Noun", "Profile"),
        settings: this.$pgettext("*/*/*/Noun", "Settings"),
        logout: this.$pgettext("Sidebar/Login/List item.Link/Verb", "Logout"),
        about: this.$pgettext("Sidebar/About/List item.Link", "About"),
        shortcuts: this.$pgettext("*/*/*/Noun", "Keyboard shortcuts"),
        support: this.$pgettext("Sidebar/*/Listitem.Link", "Help"),
        forum: this.$pgettext("Sidebar/*/Listitem.Link", "Forum"),
        docs: this.$pgettext("Sidebar/*/Listitem.Link", "Documentation"),
        language: this.$pgettext("Footer/Settings/Dropdown.Label/Short, Verb", "Change language"),
        theme: this.$pgettext("Footer/Settings/Dropdown.Label/Short, Verb", "Change theme"),
        chat: this.$pgettext("Sidebar/*/Listitem.Link", "Chat room"),
        git: this.$pgettext("Footer/*/List item.Link", "Issue tracker"),
        login: this.$pgettext('*/*/Button.Label/Verb', "Log in"),
        signup: this.$pgettext('*/*/Button.Label/Verb', "Sign up"),
      }
    },
    themes () {
      return [
        {
          icon: 'sun icon',
          name: this.$pgettext('Footer/Settings/Dropdown.Label/Theme name', 'Light'),
          key: 'light'
        },
        {
          icon: 'moon icon',
          name: this.$pgettext('Footer/Settings/Dropdown.Label/Theme name', 'Dark'),
          key: 'dark'
        }
      ]
    }
  },
  methods: {
    showShortcuts() 
      { 
        this.$emit('show:shortcuts-modal')
        console.log(this.$store.getters['ui/windowSize'])
      }
  }
}
</script>
