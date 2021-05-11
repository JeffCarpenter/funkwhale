<template>
  <modal
    @update:show="$emit('update:show', $event)"
    :show="show"
    :scrolling="true"
  >
    <div v-if="$store.state.auth.authenticated" class="header">
      <img 
        v-if="$store.state.auth.profile.avatar && $store.state.auth.profile.avatar.urls.medium_square_crop"
        v-lazy="$store.getters['instance/absoluteUrl']($store.state.auth.profile.avatar.urls.medium_square_crop)"
        alt=""
        class="ui centered small circular image">
      <actor-avatar
        v-else
        :actor="{preferred_username: $store.state.auth.username, full_username: $store.state.auth.username,}"/>
      <h3 class="user-modal title">{{ labels.header }}</h3>
    </div>
    <div v-else class="header">
      <h3 class="ui center aligned icon header">
        <i class = "settings icon" />
        {{ labels.header }}
      </h3>
    </div>
    <div class="content">
      <div class="ui one column unstackable grid">
        <template v-if="$store.state.auth.authenticated">
          <div class="row">
            <div class="column" @click.prevent.exact="$router.push({name: 'profile.overview', params: { username: $store.state.auth.username }})">
              <i class="user icon user-modal list-icon" />
              <span class="user-modal list-item">{{ labels.profile }}</span>
            </div>
          </div>
          <div class="row">
            <router-link tag="div" class="column" v-if="$store.state.auth.authenticated" :to="{name: 'notifications'}">
              <i class="user-modal list-icon bell icon"></i>
              <span class="user-modal list-item">{{ labels.notifications }}</span>
            </router-link>
          </div>
          <div class="row">
            <router-link tag="div" class="column" :to="{ path: '/settings' }">
              <i class="user-modal list-icon cog icon" />
              <span class="user-modal list-item">{{ labels.settings }}</span>
            </router-link>
          </div>
        </template>
        <div class="ui divider"></div>
        <div class="row"> 
          <a class="column" href="https://docs.funkwhale.audio" target="_blank">
            <i class="user-modal list-icon book open icon" />
            <span class="user-modal list-item">{{ labels.docs }}</span>
          </a>
        </div>
        <div class="row">
          <router-link tag="div" v-if="this.$route.path != '/about'" class="column" :to="{ name: 'about' }">
            <i class="user-modal list-icon question circle outline icon" />
            <span class="user-modal list-item">{{ labels.about }}</span>
          </router-link>
        </div>
        <div class="divider" />
        <template v-if="$store.state.auth.authenticated && this.$route.path != '/logout'">
          <router-link tag="div" class="column" :to="{ name: 'logout' }">
            <i class="user-modal list-icon sign out alternate icon" />
            <span class="user-modal list-item">{{ labels.logout }}</span>
          </router-link>
        </template>
        <template v-else-if="!$store.state.auth.authenticated && this.$route.path != '/signup'">
          <router-link tag="div" class="column" :to="{ name: 'signup' }">
            <i class="user-modal list-item user icon" />
            <span class="user-modal list-item">{{ labels.signup }}</span>
          </router-link>
        </template>
      </div>
    </div>
  </modal>
</template>

<script>
import Modal from "@/components/semantic/Modal";
import { mapGetters } from "vuex";

export default {
  props: {
    show: { type: Boolean, required: true }
  },
  components: {
    Modal,
  },
    computed: {
    labels() {
      return {
        header: this.$pgettext('Popup/Title/Noun', "Options"),
        profile: this.$pgettext("*/*/*/Noun", "Profile"),
        settings: this.$pgettext("*/*/*/Noun", "Settings"),
        logout: this.$pgettext("Sidebar/Login/List item.Link/Verb", "Logout"),
        about: this.$pgettext("Sidebar/About/List item.Link", "About"),
        shortcuts: this.$pgettext("*/*/*/Noun", "Keyboard shortcuts"),
        support: this.$pgettext("Sidebar/*/Listitem.Link", "Help"),
        forum: this.$pgettext("Sidebar/*/Listitem.Link", "Forum"),
        docs: this.$pgettext("Sidebar/*/Listitem.Link", "Documentation"),
        language: this.$pgettext(
          "Sidebar/Settings/Dropdown.Label/Short, Verb",
          "Change language"
        ),
        theme: this.$pgettext(
          "Sidebar/Settings/Dropdown.Label/Short, Verb",
          "Change theme"
        ),
        chat: this.$pgettext("Sidebar/*/Listitem.Link", "Chat room"),
        git: this.$pgettext("Sidebar/*/List item.Link", "Issue tracker"),
        login: this.$pgettext("*/*/Button.Label/Verb", "Log in"),
        signup: this.$pgettext("*/*/Button.Label/Verb", "Sign up"),
        notifications: this.$pgettext("*/Notifications/*", "Notifications"),
        useOtherInstance: this.$pgettext(
          "Sidebar/*/List item.Link",
          "Use another instance"
        ),
      };
    },
    themes() {
      return [
        {
          icon: "sun icon",
          name: this.$pgettext(
            "Footer/Settings/Dropdown.Label/Theme name",
            "Light"
          ),
          key: "light",
        },
        {
          icon: "moon icon",
          name: this.$pgettext(
            "Footer/Settings/Dropdown.Label/Theme name",
            "Dark"
          ),
          key: "dark",
        },
      ];
    },
    ...mapGetters({
      additionalNotifications: "ui/additionalNotifications",
    }),
  },
};
</script>
